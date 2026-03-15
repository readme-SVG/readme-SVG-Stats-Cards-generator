# Contributing

## 1. Introduction

Thank you for your interest in contributing to this logging library project. We value thoughtful, well-tested contributions from the community and aim to keep collaboration efficient, respectful, and technically rigorous.

Whether you are fixing a bug, improving documentation, proposing a new logging transport, or optimizing performance, your contributions help keep this library reliable in production environments.

## 2. I Have a Question

Please note that the GitHub issue tracker is reserved for:
- Reproducible bug reports
- Actionable feature requests

The issue tracker is **not** the right channel for general usage questions, troubleshooting one-off local setups, or “how do I” discussions.

For questions, use one of the following channels instead:
- GitHub Discussions (preferred)
- Stack Overflow (tag with relevant language/framework tags and project name)
- Any dedicated community channel linked in the repository README

When asking a question, include:
- Library version
- Runtime and framework context
- Minimal code snippet
- What you already tried

## 3. Reporting Bugs

High-quality bug reports dramatically reduce triage time. A good report should allow a maintainer to reproduce the issue without guessing.

### Search Duplicates First

Before opening a new issue:
1. Search open issues for the same or similar symptoms.
2. Search closed issues for prior fixes or workarounds.
3. If a matching issue exists, add reproducible details there instead of opening a duplicate.

### Required Environment Details

Include complete runtime context:
- Operating system and version (for example, Ubuntu 24.04, macOS 14.6, Windows 11)
- Library version (and whether from PyPI/npm/etc. or source)
- Language runtime version (for example, Python 3.12, Node 20)
- Framework version(s) if applicable
- Deployment context (local dev, Docker, serverless, CI runner)

### Steps to Reproduce

Provide a deterministic reproduction algorithm:
1. Preconditions (configuration, env vars, input payload, external dependencies)
2. Exact command(s) executed
3. Minimal code snippet or repository reproducer
4. Observed output, logs, stack trace, or generated artifacts

Avoid vague descriptions such as “sometimes fails.” If nondeterministic, describe frequency and patterns.

### Expected vs. Actual Behavior

Clearly state:
- **Expected behavior:** What should happen according to docs/spec/design
- **Actual behavior:** What happened instead
- **Impact:** Why this is problematic (data loss, incorrect formatting, crash, performance regression)

### Report Quality Checklist

Before submitting, ensure your issue contains:
- A descriptive title
- Reproduction steps that work from a clean environment
- Environment details
- Expected/actual behavior
- Logs or stack traces (sanitized)

## 4. Suggesting Enhancements

Enhancement proposals should be concrete, scoped, and justified by real-world needs.

### What to Include

When proposing a feature or architectural change, include:
- **Problem statement:** The specific limitation or pain point
- **Justification:** Why current behavior is insufficient
- **Use cases:** Concrete, real-world examples with expected outcomes
- **Proposed API/design:** Suggested interface, configuration, and migration implications
- **Alternatives considered:** Existing workarounds and why they are not adequate

### Scope Expectations

Large architectural proposals (for example, new plugin APIs, lifecycle hooks, or async pipelines) should start as a discussion before implementation. This prevents wasted effort and helps align with roadmap priorities.

## 5. Local Development / Setup

Use the following baseline setup for local development.

### Fork and Clone

1. Fork the repository on GitHub.
2. Clone your fork:

```bash
git clone https://github.com/<your-username>/readme-SVG-custom-badge-generator.git
cd readme-SVG-custom-badge-generator
```

3. Add the canonical upstream remote:

```bash
git remote add upstream https://github.com/<upstream-org-or-user>/readme-SVG-custom-badge-generator.git
git fetch upstream
```

### Dependencies

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

If your change requires environment configuration, create a local environment file:

```bash
cp .env.example .env
```

If `.env.example` does not exist, document required variables in your PR description and keep secrets out of version control.

### Running Locally

Start the local development endpoint:

```bash
python api/stats_index.py
```

Optional maintenance utility for sample SVG updates:

```bash
python scripts/refresh_sample_svgs.py
```

## 6. Pull Request Process

Follow this workflow to keep reviews predictable and fast.

### Branching Strategy

Create branches from the latest `main` using one of these conventions:
- `feature/<short-feature-name>`
- `bugfix/<issue-number-or-short-slug>`
- `docs/<scope>`
- `chore/<scope>`

Examples:
- `feature/json-structured-formatter`
- `bugfix/142-memory-leak-on-flush`

### Commit Messages

Use Conventional Commits:
- `feat: add async batching transport`
- `fix: prevent duplicate handler registration`
- `docs: clarify formatter extension points`
- `test: add regression for dropped records`
- `chore: update CI matrix`

### Upstream Synchronization

Before opening (or updating) a PR:

```bash
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git checkout <your-branch>
git rebase main
```

Resolve conflicts locally, then force-push your branch safely:

```bash
git push --force-with-lease
```

### PR Description Requirements

Every PR should include:
- Linked issue(s): `Closes #123` or `Related to #123`
- Problem context and rationale
- Summary of implementation details
- Risk/compatibility notes (breaking changes, migration guidance)
- Evidence of testing (commands + output snippets)
- Documentation updates when API or behavior changes

PRs without sufficient context or test evidence may be sent back for revision before review.

## 7. Styleguides

Contributions must comply with project style and architecture conventions.

### Formatting and Linting

Use these tools:
- `Black` for Python formatting
- `Flake8` for Python linting

Recommended local commands:

```bash
black .
flake8 .
```

### Code Quality Expectations

- Prefer small, composable functions with explicit inputs/outputs.
- Keep public API behavior stable unless an approved breaking change is intentional.
- Use clear names (`render_badge_svg`, `parse_badge_params`, etc.) over ambiguous abbreviations.
- Avoid hidden side effects and global mutable state where possible.

### Architectural Conventions

- Keep API logic under `api/` focused on request parsing and response composition.
- Keep transformation/rendering logic deterministic and testable.
- Keep scripts under `scripts/` task-oriented and isolated from runtime request paths.
- Update `README.md` when user-facing behavior, parameters, or examples change.

## 8. Testing

All bug fixes and new features must include relevant test coverage (unit and/or integration-level validation appropriate to the change).

At minimum, validate local behavior with:

```bash
python api/stats_index.py
python scripts/refresh_sample_svgs.py
```

If you add automated tests, document how to run them in your PR description and ensure they pass locally before requesting review.

## 9. Code Review Process

After opening a PR:

1. A maintainer performs initial triage (scope, clarity, and CI/readiness checks).
2. At least **1 maintainer approval** is required before merge (larger or higher-risk changes may require 2 approvals).
3. All requested changes must be addressed before merge.
4. After updates, request re-review from prior reviewers.
5. Maintainers may squash-merge to keep commit history clean and searchable.

### Review Expectations

- Respond to reviewer comments with technical rationale and concrete follow-up.
- Mark conversations resolved only after code and context are updated.
- Keep PR scope focused; unrelated changes may be deferred to a separate PR.
- Be open to iterative refinements in API shape, naming, and internal design.

Thank you for helping improve the project’s reliability, maintainability, and developer experience.
