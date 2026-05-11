<!-- Thanks for the PR! Keep the title in Conventional Commits format, e.g. `feat: add streaming`. -->

## Summary

<!-- One or two sentences. What changes and why. -->

## Type of change

<!-- Tick one. Must match the Conventional Commit prefix in the PR title. -->

- [ ] `feat` — New feature
- [ ] `fix` — Bug fix
- [ ] `perf` — Performance
- [ ] `refactor` — Refactor (no behavior change)
- [ ] `docs` — Documentation
- [ ] `test` — Tests
- [ ] `build` / `ci` — Tooling
- [ ] `chore` — Maintenance

## Linked issues

<!-- e.g. Fixes #123, Closes #456. Use "Fixes" / "Closes" so GitHub auto-closes on merge. -->

## Checklist

- [ ] PR title follows Conventional Commits (`feat:`, `fix:`, etc.)
- [ ] Tests added or updated; coverage stays at the configured threshold
- [ ] `uv run pre-commit run --all-files` passes locally
- [ ] `uv run pytest` passes locally
- [ ] Public API changes are reflected in `README.md` / docstrings
- [ ] Breaking changes use `!` in the title or a `BREAKING CHANGE:` footer

## Notes for reviewers

<!-- Anything non-obvious: tradeoffs you considered, what to scrutinize, screenshots, benchmarks. -->
