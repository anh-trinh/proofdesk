# Recipes start with ">" instead of a tab, so copy-paste cannot break the file.
.RECIPEPREFIX = >
PY = services/proofdesk

.PHONY: setup test lint fmt check check-fast

setup:
> cd $(PY) && uv sync

test:
> cd $(PY) && uv run pytest

lint:
> cd $(PY) && uv run ruff check . && uv run ruff format --check . && uv run mypy src tests

fmt:
> cd $(PY) && uv run ruff check --fix . && uv run ruff format .

# The same gate as CI: run it before every push.
check: lint test

# Fast feedback for the Claude Code Stop hook: no coverage gate, stop at the first failure.
check-fast: lint
> cd $(PY) && uv run pytest tests/unit --no-cov -x -q
