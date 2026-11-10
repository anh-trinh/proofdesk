# CLAUDE.md

Project rules for Claude Code. Read them before every change.

## Project
ProofDesk: document AI with human review. Python 3.13 core in `services/proofdesk`,
AWS CDK in `infra` (from Milestone 2), TanStack Start web app in `apps/web` (from Milestone 5).

## Commands
- `make setup`: install Python dependencies with uv
- `make test`: all Python tests with coverage (must stay at or above 90%)
- `make lint`: ruff check, ruff format --check, mypy --strict
- One test file: `cd services/proofdesk && uv run pytest tests/unit/test_money.py --no-cov`

## How we work
- Plan first. Propose the plan and wait for approval before editing files.
- TDD: write the test, run it and see it fail, then write the smallest code that passes.
- Small commits with Conventional Commits messages (`test:`, `feat:`, `fix:`, `refactor:`,
  `docs:`, `chore:`, `ci:`).
- Every change reaches `main` through a pull request. Never push to `main`.

## Hard rules
- Never use `float` for money. Use `Decimal` and `proofdesk.contracts.money.to_money` (ADR-0007).
- Parse XML only with `defusedxml` (ADR-0003).
- No `*` in IAM actions or resources.
- `tenantId` comes from the verified session only, never from the request.
- Never log extracted values or personal data. Log IDs and codes only.
- No secrets and no real invoices in the repo. Real samples live in `samples/private/` (git-ignored).
- Code, comments, commit messages and repo docs are in English.

## Never do
- Run `cdk deploy`, delete AWS resources or change GitHub settings.
- Read `.env*` files or anything in `samples/private/`.
