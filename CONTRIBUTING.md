# Contributing to README SVG Stats Cards Generator

Thanks for taking the time to contribute. Seriously.

This project is intentionally lightweight: a Python/Flask serverless API that renders SVG cards for GitHub READMEs. That means contribution turnaround can be fast, but we still keep a strong quality bar for reliability, maintainability, and predictable output.

## 1. Introduction

If you are here, you are already awesome.

Contributions are welcome in multiple forms:

- Bug fixes
- New card features or params
- Performance improvements
- Documentation upgrades
- Developer-experience improvements (tooling, scripts, validation flow)

Before you open a PR, please read:

- [`README.md`](README.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- This file end to end

## 2. I Have a Question

Please do not use Issues for usage/support questions. The Issue tracker is reserved for actionable engineering work.

Use one of these channels for questions:

- GitHub Discussions (if enabled)
- GitHub profile/community channels linked in `README.md`
- Any thread where reproducible request examples can be shared

When asking, include:

- Exact endpoint URL you called
- Query params
- Expected output vs actual output
- Runtime mode (`python api/stats_index.py` or `vercel dev`)

This keeps support async-friendly and avoids guesswork.

## 3. Reporting Bugs

High-signal bug reports reduce triage time and get fixes merged faster.

### 3.1 Search for duplicates first

Before opening a new bug:

1. Search open Issues.
2. Search closed Issues.
3. Re-test against latest `main`.

### 3.2 Include environment details

At minimum, report:

- OS + version
- Python version (`python --version`)
- Dependency context (`pip freeze` or relevant package versions)
- Runtime mode (`local Flask`, `vercel dev`, or deployed URL)
- Exact URL that reproduces the issue

### 3.3 Steps to reproduce

Use deterministic steps, for example:

1. Start local app with specific command.
2. Call exact endpoint with exact query string.
3. Share rendered/returned SVG behavior.

### 3.4 Expected vs actual behavior

Clearly separate:

- Expected behavior
- Actual behavior

Optional but useful:

- Screenshot of rendered SVG
- Minimal raw SVG snippet demonstrating the issue

## 4. Suggesting Enhancements

Enhancement proposals are welcome, but pitch the problem, not just the idea.

A good enhancement request includes:

- Problem statement (what hurts today)
- Why current behavior is insufficient
- Proposed solution
- API/compatibility impact
- Real use cases

Good examples:

- New visual styles for `/views`
- Better defaults and clamping logic for query params
- More robust live GitHub data collection with safe fallback behavior

## 5. Local Development / Setup

### 5.1 Fork and clone

```bash
# 1) Fork repository on GitHub
# 2) Clone your fork
git clone https://github.com/YOUR_USERNAME/readme-SVG-Stats-Cards-generator.git
cd readme-SVG-Stats-Cards-generator
```

### 5.2 Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate            # Linux/macOS
# .venv\Scripts\activate            # Windows

pip install -r requirements.txt
```

### 5.3 Configure environment variables

Optional but recommended:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxx
```

If you build automation around `process_event.py`, configure the additional CI variables described in `README.md`.

### 5.4 Run locally

```bash
python api/stats_index.py
# or
vercel dev
```

## 6. Pull Request Process

### 6.1 Branch naming strategy

Use these conventions:

- `feature/<short-topic>`
- `bugfix/<short-topic>`
- `docs/<short-topic>`
- `refactor/<short-topic>`
- `chore/<short-topic>`

Examples:

- `feature/new-streak-accent-options`
- `bugfix/views-counter-clamp`
- `docs/readme-usage-refresh`

### 6.2 Commit messages (Conventional Commits)

Use Conventional Commits:

- `feat: add custom accent color override for streak card`
- `fix: clamp invalid border_radius values`
- `docs: rewrite contributing setup section`
- `refactor: extract color normalization helper`

### 6.3 Stay synced with upstream

Before opening or updating a PR:

```bash
git fetch upstream
git rebase upstream/main
```

### 6.4 PR description requirements

Your PR description should include:

- What changed
- Why it changed
- Linked Issue(s) (`Closes #123` when applicable)
- Breaking changes (if any)
- Screenshots for visual card/output changes
- Any migration notes for users

## 7. Styleguides

### 7.1 Python style

- Follow PEP 8 and keep code readable over clever.
- Prefer explicit helpers over repetitive inline parsing.
- Keep endpoint code thin; push rendering logic into renderer modules.

### 7.2 Linting / formatting

Current repository does not enforce mandatory formatter config in-tree.

Recommended tools for contributors:

- `black`
- `ruff` (or `flake8`)

If you introduce tooling configs, keep them minimal and document them.

### 7.3 Architecture guidelines

- Keep request parsing and HTTP concerns in `api/stats_index.py`.
- Keep SVG generation and theme logic in `api/github_stats.py`.
- Avoid coupling route handlers with unrelated automation scripts.

## 8. Testing

New behavior should be validated. If you touch logic, add tests where practical or provide reproducible validation steps.

Typical local checks:

```bash
python -m compileall api process_event.py
python api/stats_index.py
curl -I "http://127.0.0.1:5000/stats?username=octocat"
curl -I "http://127.0.0.1:5000/streak?username=octocat"
curl -I "http://127.0.0.1:5000/graph?username=octocat"
curl -I "http://127.0.0.1:5000/views?username=octocat"
```

If your PR changes card visuals, include before/after images in the PR body.

## 9. Code Review Process

Maintainers review for:

- Correctness
- API compatibility
- Visual/output quality
- Simplicity and maintainability

General flow:

1. PR triage
2. Technical review
3. Feedback round
4. Approval + merge

How to handle review comments:

- Reply with context, not silence
- Push focused follow-up commits
- Resolve threads only after actual changes land
- If you disagree, discuss trade-offs with concrete examples

Thanks again for contributing and helping keep this project sharp.
