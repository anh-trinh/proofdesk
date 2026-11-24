---
paths:
  - "services/**/*.py"
  - "infra/**/*.py"
---

# Python rules

- Money is `Decimal`, built with `proofdesk.contracts.money.to_money`. Never `float` (ADR-0007).
- Parse XML only with `defusedxml`.
- Log IDs and codes only. Never log extracted values or personal data.
- When re-raising inside `except`, chain the cause: `raise DomainError(...) from exc`.
- No `assert` in `src/`; raise a typed error instead. `assert` belongs in tests.
- Test names describe behaviour, for example `test_rejects_total_that_differs_from_lines`.
- Follow the code design checklist in `CONTRIBUTING.md`.
- An absent value is typed `T | None`. A collection is returned empty, never `None`.
- Adapters are named after their technology (`S3DocumentStore`, not `DocumentStoreImpl`).
- SDK errors become domain errors inside the adapter; no SDK exception reaches the domain.
- Run `make check-fast` before you say the work is finished.
