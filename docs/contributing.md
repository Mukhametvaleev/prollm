# Contributing

See [CONTRIBUTING.md](https://github.com/Mukhametvaleev/prollm/blob/develop/CONTRIBUTING.md) on
GitHub for the full contributor guide — setup, branching, commit conventions, testing, and release
workflow.

## Quick links

- [Branch naming convention](https://github.com/Mukhametvaleev/prollm/blob/develop/CONTRIBUTING.md#branch-naming)
- [Commit message format](https://github.com/Mukhametvaleev/prollm/blob/develop/CONTRIBUTING.md#commit-messages)
- [Running tests](https://github.com/Mukhametvaleev/prollm/blob/develop/CONTRIBUTING.md#running-checks)
- [Release process](https://github.com/Mukhametvaleev/prollm/blob/develop/CONTRIBUTING.md#releases)

## Building docs locally

```bash
uv sync --group docs
uv run mkdocs serve
```

Then open <http://localhost:8000/>. The site rebuilds live as you edit Markdown or docstrings.
