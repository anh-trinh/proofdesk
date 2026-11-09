# Contributing

## Workflow

1. Open or pick an issue.
2. Branch from `main`: `feat/<issue>-<short-name>` (or `fix/`, `docs/`, `chore/`).
3. Write the test first. Commit the failing test (`test:`), then the code (`feat:`).
4. Open a draft pull request. The PR title must follow Conventional Commits because it
   becomes the commit message on `main` (squash merge).
5. Run `make lint` and `make test` before marking the PR ready.

## Conventional Commits

`feat:` new behaviour, `fix:` bug fix, `test:` tests only, `refactor:` no behaviour change,
`docs:` documentation, `ci:` workflows, `chore:` tooling.

## Rules

- No secrets, no real documents, no `float` for money.
- New behaviour needs a test. Coverage must stay at or above 90%.
- Architecture decisions go in `docs/adr/`.
