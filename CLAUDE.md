# CLAUDE.md

Project rules for Claude Code. Read them before every change.

## Project
ProofDesk: document AI with human review. Python 3.13 core in `services/proofdesk`,
AWS CDK in `infra` (from Milestone 2), TanStack Start web app in `apps/web` (from Milestone 5).

## Commands
- `make setup`: install Python dependencies with uv
- `make test`: all Python tests with coverage (must stay at or above 90%)
- `make lint`: ruff check, ruff format --check, mypy --strict
- `make check`: lint and test, the same gate as CI. Run it before every push.
- `make check-fast`: lint and unit tests without coverage, used by the Stop hook
- One test file: `cd services/proofdesk && uv run pytest tests/unit/test_money.py --no-cov`

## How we work
- Plan first. Propose the plan and wait for approval before editing files.
- TDD: write the test, run it and see it fail, then write the smallest code that passes.
- Small commits with Conventional Commits messages (`test:`, `feat:`, `fix:`, `refactor:`,
  `docs:`, `chore:`, `ci:`).
- Every change reaches `main` through a pull request. Never push to `main`.

## Hard rules
- Never use `float` for money. Use `Decimal` and `proofdesk.contracts.money.to_money` (ADR-0007, `docs/decisions/`).
- Parse XML only with `defusedxml` (ADR-0003).
- No `*` in IAM actions or resources.
- `tenantId` comes from the verified session only, never from the request.
- Never log extracted values or personal data. Log IDs and codes only.
- No secrets and no real invoices in the repo. Real samples live in `samples/private/` (git-ignored).
- Code, comments, commit messages and repo docs are in English.

## Never do
- Run `cdk deploy`, delete AWS resources or change GitHub settings.
- Read `.env*` files or anything in `samples/private/`.

## Code review rules

When reviewing a diff (for example with /code-review):

- Write review comments in English. Be specific: file, line, why it matters, suggested fix.
- Put suggested code in a GitHub suggestion block (```suggestion) anchored to the exact
  lines it replaces, so the author can use "Commit suggestion". Include only the
  replacement lines, with no diff markers and no unrelated changes.
- End every comment that has a suggestion block with one line:
  `Commit message: <type>: <description>`
  Use a Conventional Commits type from "How we work" (`fix:`, `refactor:`, `test:`,
  `docs:`, `chore:`). Lower case, imperative mood, no trailing period, 72 characters max.
  Example: `Commit message: fix: reject float amounts in to_money`
  GitHub cannot pre-fill this, so the author pastes it into the commit dialog.
- When several suggestions belong in one commit, say so and give one shared commit
  message for "Add suggestion to batch".
- Rate each finding High, Medium or Low.
- High: float used for money (must be Decimal), tenantId taken from the request
  instead of the session, IAM policy with "*", XML parsed without defusedxml,
  extracted values or PII written to logs, secrets or real documents in the diff.
- Flag missing tests for new behaviour. New Python code needs a unit test.
- Do not comment on formatting: Ruff enforces it in CI (ESLint will once `apps/web` lands).
- Do not suggest new dependencies without explaining the licence and why the
  standard library is not enough.
