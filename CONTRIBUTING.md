# Contributing to prollm

Thanks for your interest in contributing. This document covers the development workflow.

## Setup

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Mukhametvaleev/prollm
cd prollm
uv sync --group dev

# Install both pre-commit hook types
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Branching

- `main` — released code only; matches the latest published version
- `develop` — active integration branch; all PRs target this
- Feature branches — short-lived, branch from `develop`

Open PRs against `develop`.

### Branch naming

Branches must follow `<type>/[<issue-number>-]<kebab-topic>`. The `<type>` segment uses the same vocabulary as
[Commit messages](#commit-messages) below — one mental model for both. CI rejects PRs whose source branch does not
match this pattern.

```text
feat/123-streaming-support
fix/anthropic-empty-content
chore/upgrade-pytest
docs/clarify-temperature-bounds
refactor/extract-httpx-builder
```

Rules:

- `<type>` — one of: `feat`, `fix`, `perf`, `refactor`, `revert`, `docs`, `style`, `test`, `build`, `ci`, `chore`
- `<issue-number>` (optional) — include when the branch closes a GitHub issue (e.g. `fix/124-...`)
- `<kebab-topic>` — lowercase letters/digits/hyphens, ~3–5 words, must start and end with `[a-z0-9]`

The regex:

```text
^(feat|fix|perf|refactor|revert|docs|style|test|build|ci|chore)/([0-9]+-)?[a-z0-9][a-z0-9-]*[a-z0-9]$
```

Bot-generated branches (`dependabot/*`, `release-please--*`, `renovate/*`) are exempt.

## Commit messages

This repo enforces [Conventional Commits](https://www.conventionalcommits.org/) at two layers — a local commit-msg hook
and a CI check on PR titles. Use one of these prefixes:

| Type       | When to use                           |
| ---------- | ------------------------------------- |
| `feat`     | New user-facing feature (bumps minor) |
| `fix`      | Bug fix (bumps patch)                 |
| `perf`     | Performance improvement               |
| `refactor` | Code reshape with no behavior change  |
| `revert`   | Revert of an earlier commit           |
| `docs`     | Documentation only                    |
| `style`    | Formatting, no logic change           |
| `test`     | Test changes only                     |
| `build`    | Build system / dependency changes     |
| `ci`       | CI / workflow changes                 |
| `chore`    | Anything else                         |

Optionally include a scope: `feat(openai): add streaming`. For breaking changes use a `!` (`feat!: drop py3.13 support`)
or a `BREAKING CHANGE:` footer.

## Running checks

Before pushing:

```bash
# Lint, format, type-check
uv run pre-commit run --all-files

# Tests with coverage (must stay at 100% or above the configured threshold)
uv run pytest
```

CI runs the same on every PR.

## Coverage

The project enforces a coverage gate via `pytest-cov`. New code without tests will fail CI. If a line genuinely cannot
be tested, add `# pragma: no cover` and explain why in the PR description.

## Style

- **Linting & formatting**: `ruff check` + `ruff format` (config in `pyproject.toml`, `select = ["ALL"]` with documented
  ignores)
- **Type checking**: `mypy --strict` (config in `pyproject.toml`)
- **Docstrings**: Google convention
- **Tests**: pytest + pytest-mock; shared HTTP-response builders live in `tests/_factories.py`

## Releases

The release pipeline is fully automated. End-to-end flow:

1. **Commits land on `develop`** with Conventional Commit messages.
2. **[release-please](https://github.com/googleapis/release-please)** opens (or updates) a Release PR that bumps the
   version in `pyproject.toml`, `__init__.py`, and `.release-please-manifest.json`, plus aggregates a `CHANGELOG.md`
   entry.
3. **Maintainer merges the Release PR.** release-please creates a tagged GitHub Release (e.g. `v0.2.0`).
4. **`Publish` workflow fires** on `release: published`:
   - Builds sdist + wheel with `uv build`
   - Uploads to **TestPyPI** via Trusted Publishing (OIDC, no API tokens)
   - Pauses on the `pypi` environment, requiring **manual reviewer approval**
   - On approval, uploads to **PyPI** with [Sigstore attestations](https://docs.pypi.org/attestations/)
5. **Manually promote `develop` → `main`** so `main` always reflects the latest released version.

You never hand-edit version files or `CHANGELOG.md` — release-please owns those.

### Publishing prerequisites (one-time, for maintainers)

1. Reserve the package name on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/).
2. Configure [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) on both PyPI and TestPyPI:
   - Owner: the GitHub org/user
   - Repository: `prollm`
   - Workflow: `publish.yml`
   - Environment: `pypi` (on PyPI) and `testpypi` (on TestPyPI)
3. Create two GitHub Environments (Repository Settings → Environments):
   - `testpypi` — no protections required
   - `pypi` — add **Required reviewers** (at least one maintainer) so every PyPI publish needs explicit approval

## Reporting bugs

Open a GitHub Issue with:

- Python version and OS
- `prollm` version (`python -c "import prollm; print(prollm.__version__)"`)
- Minimal reproduction
- Expected vs actual behavior
- Full traceback if applicable
