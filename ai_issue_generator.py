from __future__ import annotations

import json
import os
import re
import time

import requests
from github import Github, Auth

MODEL_NAME = "Llama-3.3-70B-Instruct"
ENDPOINT = "https://models.inference.ai.azure.com/chat/completions"

BASE_INSTRUCTIONS = """
Return only a raw JSON object with no markdown formatting. The JSON must have these exact keys:

"issue_title": string — include severity prefix like [CRITICAL], [HIGH], [MEDIUM], or [LOW] at the start,
"severity": string — one of: critical, high, medium, low,
"issue_body": string — must include these sections:
  ## Problem
  (clear description with exact file paths and line numbers if known)

  ## Code Reference
  (the exact problematic code snippet)

  ## Suggested Fix
  (concrete code or steps to fix)

  ## Permalink
  (placeholder: PUT_PERMALINK_HERE — will be replaced automatically)

"labels": list of strings — standard GitHub labels plus the severity level,
"affected_file": string — the most relevant filename from the diff (or "" if unknown),
"affected_line": integer — approximate line number of the issue (or 1 if unknown),
"summary": string — 2-3 sentence plain-English summary for the PR comment

The issue_title, issue_body and summary MUST be written entirely in English.
"""

SEVERITY_LABEL_MAP = {
    "critical": "severity: critical",
    "high":     "severity: high",
    "medium":   "severity: medium",
    "low":      "severity: low",
}


def build_prompt(trigger_labels: list[str], event_context: str, diff_text: str) -> str:
    base = f"Context: {event_context}\nChanges: {diff_text}\n{BASE_INSTRUCTIONS}"

    if any(l in trigger_labels for l in ["sec", "security", "audit"]):
        return f"Act as a Strict Security Auditor. Perform a deep security audit (OWASP Top 10). Find real vulnerabilities with exact file/line references.\n{base}"
    if any(l in trigger_labels for l in ["review", "refactor", "code-review"]):
        return f"Act as a Strict Code Reviewer. Analyze code quality (SOLID/DRY). Point to exact lines that violate principles.\n{base}"
    if any(l in trigger_labels for l in ["qa", "test", "testing"]):
        return f"Act as a QA Engineer. Identify edge cases and missing test coverage. Reference exact functions/lines.\n{base}"
    if any(l in trigger_labels for l in ["perf", "performance", "optimize"]):
        return f"Act as a Performance Expert. Analyze bottlenecks and O(n) complexity issues with exact line references.\n{base}"
    if any(l in trigger_labels for l in ["pm", "release", "product"]):
        return f"Act as a Product Manager. Generate user-facing Release Notes with clear impact descriptions.\n{base}"
    if any(l in trigger_labels for l in ["deps", "dependencies"]):
        return f"Act as a Security & Dependency Auditor. Analyze all new or changed dependencies: check for known vulnerabilities (CVEs), license compatibility (MIT/Apache/GPL), package size impact, and whether each dep is actively maintained. Reference exact file and line where dep is added.\n{base}"
    if any(l in trigger_labels for l in ["arch", "architecture"]):
        return f"Act as a Software Architect. Review the code changes for architectural issues: violation of separation of concerns, tight coupling, wrong layer dependencies, anti-patterns (God object, spaghetti logic, magic numbers). Reference exact files and lines.\n{base}"

    return f"""Analyze the following code changes and create a documentation issue summarizing what was changed and why.
IMPORTANT: Do NOT invent security issues, bugs, or problems that do not exist in the diff.
If the changes are trivial (e.g. adding imports, minor refactoring), set severity to LOW and describe only what actually changed.
{base}"""


def call_model(prompt: str, model_token: str, retries: int = 3, delay: int = 5) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {model_token}",
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a professional software auditor. Always return valid JSON only. No markdown, no explanation, just the JSON object."},
            {"role": "user", "content": prompt},
        ],
        "model": MODEL_NAME,
        "temperature": 0.1,
    }

    for attempt in range(retries):
        try:
            resp = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"].strip()
            raw = re.sub(r"^```json\s*|```$", "", raw, flags=re.MULTILINE).strip()
            return json.loads(raw)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)

    print("All attempts failed. Exiting gracefully.")
    raise RuntimeError("Model call failed after all retries.")


def build_permalink(repo_name: str, filename: str, line: int, commit_sha: str) -> str:
    return f"https://github.com/{repo_name}/blob/{commit_sha}/{filename}#L{line}"


def was_already_closed(repo, title_keyword: str) -> bool:
    for issue in repo.get_issues(state="closed"):
        if title_keyword.lower() in (issue.title or "").lower():
            print(f"Similar closed issue found: #{issue.number} — skipping.")
            return True
    return False


def run():
    gh_token    = os.environ["GITHUB_TOKEN"]
    model_token = os.environ["GH_MODELS_TOKEN"]
    repo_name   = os.environ["REPOSITORY"]
    event_name  = os.environ["EVENT_NAME"]
    allowed_users = [u.strip().lower() for u in os.environ.get("ALLOWED_USER", "").split(",")]

    gh   = Github(auth=Auth.Token(gh_token))
    repo = gh.get_repo(repo_name)

    diff_text     = ""
    event_context = ""
    author_login  = ""
    trigger_labels: list[str] = []
    dedup_key     = ""
    commit_sha    = ""
    pr_ref        = None

    if event_name == "push":
        commit_sha = os.environ.get("COMMIT_SHA", "")
        commit = repo.get_commit(commit_sha)

        if len(commit.parents) > 1 or not commit.author:
            return

        author_login = commit.author.login.strip().lower()
        if author_login not in allowed_users:
            return

        dedup_key     = f"commit:{commit_sha[:7]}"
        event_context = f"Commit Message: {commit.commit.message}"
        trigger_labels = [m.lower() for m in re.findall(r"\[(.*?)\]", commit.commit.message)]

        for f in commit.files:
            diff_text += f"File: {f.filename}\nPatch:\n{f.patch}\n\n"
            if len(diff_text) > 10_000:
                diff_text += "\n[Diff truncated...]"
                break

    elif event_name == "pull_request":
        pr_number    = int(os.environ["PR_NUMBER"])
        pr           = repo.get_pull(pr_number)
        author_login = pr.user.login.strip().lower()

        if author_login not in allowed_users:
            return

        pr_ref        = pr
        commit_sha    = pr.head.sha
        dedup_key     = f"PR #{pr_number}"
        event_context = f"PR Title: {pr.title}\nPR Body: {pr.body}"
        trigger_labels = [label.name.lower() for label in pr.labels]

        for f in pr.get_files():
            diff_text += f"File: {f.filename}\nPatch:\n{f.patch}\n\n"
            if len(diff_text) > 80_000:
                diff_text += "\n[Diff truncated...]"
                break
    else:
        return

    if len(diff_text.strip()) < 50:
        print("Diff too small to analyze. Skipping.")
        return

    for issue in repo.get_issues(state="open"):
        if dedup_key in (issue.body or ""):
            print(f"Issue for {dedup_key} already exists (#{issue.number}), skipping.")
            return

    prompt = build_prompt(trigger_labels, event_context, diff_text)
    result = call_model(prompt, model_token)

    title_keyword = result.get("issue_title", "")[:40]
    if was_already_closed(repo, title_keyword):
        return

    affected_file = result.get("affected_file", "")
    affected_line = result.get("affected_line", 1)
    issue_body    = result["issue_body"]

    if affected_file and commit_sha:
        permalink  = build_permalink(repo_name, affected_file, affected_line, commit_sha)
        issue_body = issue_body.replace("PUT_PERMALINK_HERE", permalink)
    else:
        issue_body = issue_body.replace("PUT_PERMALINK_HERE", "_No specific file identified_")

    footer = (
        f"\n\n---\n*Generated automatically from commit {commit_sha[:7]}*"
        if event_name == "push"
        else f"\n\n---\n*Generated automatically from {dedup_key}*"
    )

    severity     = result.get("severity", "medium").lower()
    extra_labels = [SEVERITY_LABEL_MAP.get(severity, "severity: medium")]
    all_labels   = list(set(result.get("labels", []) + extra_labels))

    issue = repo.create_issue(
        title=result["issue_title"],
        body=issue_body + footer,
        labels=all_labels,
    )
    print(f"Created issue #{issue.number}: {issue.title}")

    if pr_ref:
        summary = result.get("summary", "")
        if summary:
            pr_ref.create_issue_comment(
                f"### AI Analysis Summary\n\n"
                f"{summary}\n\n"
                f"**Severity:** `{severity.upper()}`\n\n"
                f"Full details: #{issue.number}"
            )
            print(f"Posted summary comment to PR #{pr_ref.number}")


if __name__ == "__main__":
    run()
