# Recipes start with ">" instead of a tab, so copy-paste cannot break the file.
.RECIPEPREFIX = >
PY = services/proofdesk

.PHONY: setup test lint fmt

setup:
> cd $(PY) && uv sync

test:
> cd $(PY) && uv run pytest

lint:
> cd $(PY) && uv run ruff check . && uv run ruff format --check . && uv run mypy src tests

fmt:
> cd $(PY) && uv run ruff check --fix . && uv run ruff format .
