# Contributing

## 1. Introduction

Thank you for your interest in contributing to this logging library. We appreciate your time, engineering effort, and willingness to improve reliability, observability, and developer experience for the broader community.

This document defines the expected contribution workflow so your changes can be reviewed and merged with minimal friction. Following these guidelines helps maintain predictable release quality, stable APIs, and efficient maintainer review cycles.

## 2. I Have a Question

The GitHub issue tracker is strictly reserved for:
- Reproducible bug reports
- Actionable feature requests

Please do **not** open an issue for usage questions, setup support, architecture brainstorming, or “how do I” requests.

For questions and general discussion, use:
- GitHub Discussions (preferred)
- Stack Overflow (include relevant language/framework tags)
- Any dedicated community channels linked in `README.md`

When asking a question, include enough context to get a useful answer quickly:
- Logging library version
- Runtime version (for example Node.js/Python)
- Framework/integration details
- Minimal code sample
- Error output and what you already tried

## 3. Reporting Bugs

A strong bug report should be deterministic, scoped, and independently reproducible by a maintainer.

### Search Duplicates

Before creating a new issue:
1. Search existing **open issues** for matching symptoms.
2. Search **closed issues** for prior fixes, regressions, or known limitations.
3. If a matching issue exists, add new reproducible evidence there instead of opening a duplicate.

### Environment

Always include a complete environment matrix:
- OS and version (for example Ubuntu 24.04, macOS 14, Windows 11)
- Library version and install source (package registry vs source checkout)
- Language/runtime version (for example Python 3.12, Node.js 20)
- Framework versions (if applicable)
- Execution context (local machine, Docker, CI, serverless, container runtime)

### Steps to Reproduce

Provide a step-by-step algorithm that reproduces the issue from a clean state:
1. Preconditions (configuration, env vars, inputs, external dependencies)
2. Exact commands executed
3. Minimal reproducible code snippet or repository
4. Logs, stack traces, output artifacts, and failure frequency

If behavior is intermittent, include frequency patterns and conditions that increase likelihood.

### Expected vs. Actual Behavior

Clearly separate the two outcomes:
- **Expected behavior**: what should happen according to docs/spec/design
- **Actual behavior**: what happened instead

Also include impact severity (for example crash, data loss, incorrect log serialization, memory regression, performance degradation).

### High-Quality Bug Report Checklist

A complete report should include:
- Clear and searchable title
- Reproduction steps that work on a fresh environment
- Full environment details
- Expected and actual behavior
- Sanitized logs/errors/tracebacks
- Any relevant workaround discovered

## 4. Suggesting Enhancements

Enhancement proposals should describe a real problem, a feasible solution, and practical adoption scenarios.

When suggesting a feature or architectural change, include:
- **Justification**: the specific problem or limitation being solved
- **Use cases**: concrete real-world scenarios and expected outcomes
- **Proposed API/design**: rough interface, configuration shape, and lifecycle impact
- **Alternatives considered**: existing approaches and why they are insufficient
- **Compatibility considerations**: migration path, deprecations, or potential breaking changes

For larger proposals (new transport abstractions, pipeline architecture changes, plugin systems), open a discussion first to align on direction before implementation.

## 5. Local Development / Setup

Follow these steps to prepare a local development environment.

### Fork and Clone

1. Fork the repository to your GitHub account.
2. Clone your fork and enter the project directory:

```bash
git clone https://github.com/<your-username>/readme-SVG-custom-badge-generator.git
cd readme-SVG-custom-badge-generator
```

3. Add upstream and fetch latest references:

```bash
git remote add upstream https://github.com/<upstream-org-or-user>/readme-SVG-custom-badge-generator.git
git fetch upstream
```

### Dependencies

Install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you are working on JavaScript-facing changes, also install Node dependencies when `package.json` is present:

```bash
npm install
```

### Environment Variables

If an environment template exists, initialize local environment variables:

```bash
cp .env.example .env
```

If no `.env.example` exists, define required variables manually and document them in your PR. Never commit secrets.

### Running Locally

Run the local service or scripts used during development:

```bash
python api/stats_index.py
python scripts/refresh_sample_svgs.py
```

Use additional project-specific commands from `README.md` when validating feature-specific paths.

## 6. Pull Request Process

Use the workflow below for all pull requests.

### Branching Strategy

Create branches from `main` using one of these conventions:
- `feature/<short-description>`
- `bugfix/<issue-number-or-short-description>`
- `docs/<scope>`
- `chore/<scope>`

Examples:
- `feature/structured-json-output`
- `bugfix/214-broken-svg-escaping`

### Commit Messages

All commits must follow Conventional Commits:
- `feat: add batched transport flush policy`
- `fix: prevent duplicate logger handlers`
- `docs: clarify configuration precedence`
- `test: add regression coverage for transport retry`
- `chore: update CI workflow`

### Upstream Synchronization

Before opening or updating a PR, sync with latest upstream `main`:

```bash
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git checkout <your-branch>
git rebase main
```

Resolve conflicts locally, then update your branch:

```bash
git push --force-with-lease
```

### PR Description

Every PR body must include:
- Linked issue(s): `Closes #<id>` or `Related to #<id>`
- Problem statement and technical context
- Summary of implementation approach
- Backward-compatibility or migration notes
- Test coverage proof (commands run and results)
- Documentation updates for any user-facing behavior changes

PRs with missing context, missing tests, or unclear scope may be returned for revision before review.

## 7. Styleguides

Contributions must meet repository quality standards for formatting, linting, naming, and architecture.

### Linters and Formatters

Use the following tools:
- `Black` (Python formatting)
- `Flake8` (Python linting)

Run:

```bash
black .
flake8 .
```

If JavaScript code is introduced or modified and tooling is configured, run:

```bash
npm run lint
npm run format
```

### Architectural and Naming Conventions

- Keep endpoint-facing logic in `api/` focused on request parsing and response composition.
- Keep transformation logic deterministic and testable.
- Keep scripts in `scripts/` task-oriented and isolated from request-serving paths.
- Prefer explicit, descriptive names over abbreviations.
- Preserve backward compatibility for public behavior unless an approved breaking change is planned.

## 8. Testing

All bug fixes and new features must include relevant automated tests (unit and/or integration) proportional to change risk.

Minimum local validation commands:

```bash
python api/stats_index.py
python scripts/refresh_sample_svgs.py
```

Recommended quality checks before opening a PR:

```bash
black .
flake8 .
```

If JS tooling/tests are configured, run:

```bash
npm test
```

A pull request is considered review-ready only when tests and checks related to your change pass locally.

## 9. Code Review Process

After a PR is opened, the review lifecycle is:

1. Maintainers perform initial triage for scope, clarity, and baseline readiness.
2. Automated checks (if configured) must pass before merge consideration.
3. At least **one maintainer approval** is required for low-risk changes; larger or higher-risk changes may require **two approvals**.
4. Requested changes must be fully addressed with follow-up commits.
5. After updates, request re-review from previous reviewers.
6. Maintainers may squash-merge to keep history concise and traceable.

Reviewer expectations:
- Keep discussions technical, specific, and outcome-oriented.
- Reply to each substantive review thread with either an implementation update or rationale.
- Mark threads resolved only when code and context are fully addressed.
- Keep PRs focused; unrelated edits should be split into separate PRs.

Thank you again for contributing and helping improve the quality, stability, and maintainability of this logging library.
