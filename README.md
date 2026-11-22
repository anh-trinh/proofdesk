# ProofDesk

[![ci](https://github.com/anh-trinh/proofdesk/actions/workflows/ci.yml/badge.svg)](https://github.com/anh-trinh/proofdesk/actions/workflows/ci.yml)
[![codeql](https://github.com/anh-trinh/proofdesk/actions/workflows/codeql.yml/badge.svg)](https://github.com/anh-trinh/proofdesk/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/anh-trinh/proofdesk/badge)](https://scorecard.dev/viewer/?uri=github.com/anh-trinh/proofdesk)

Document AI with a human in the loop. Upload an invoice, extract the data, validate it,
let a reviewer approve it, then export a clean CSV.

## Status

Milestone 1 (the domain core) is in progress. The pieces below work and are tested. The
rest is design only.

| Area | State |
| --- | --- |
| Invoice contract, with exact money (`Decimal`, never `float`) | Done |
| Tax ID checks: Australian ABN (checksum), Vietnamese MST (format only) | Done |
| Totals, dates, confidence and duplicate-key rules, and `validate_invoice` | Done |
| Safe e-invoice XML parser | Next, waiting on the official tag specification |
| PDF and image reading with Claude on Amazon Bedrock | Roadmap, Milestone 3 |
| AWS infrastructure, review web app, CSV export | Roadmap, Milestones 2 to 7 |

## Why

Extracting invoice data with AI is easy to demo and hard to trust. ProofDesk is built
around that gap:

- **Exact where it can be.** E-invoice XML is parsed deterministically, with no AI.
- **Checked before a person sees it.** Totals, tax IDs and dates are validated, and each
  problem is a stable code, not free text.
- **A person decides.** Every field carries a confidence score, and low ones are flagged.
- **Private by default.** Issues carry codes and field names only, never extracted values.

## Quick start

You need Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
make setup   # install dependencies
make check   # lint, type check and tests with coverage (the CI gate)
```

## Example

```python
from datetime import date
from decimal import Decimal

from proofdesk.contracts.invoice import Extracted, Invoice, LineItem
from proofdesk.validation import validate_invoice


def read(value, confidence="0.95"):
    return Extracted(value=value, confidence=Decimal(confidence))


invoice = Invoice(
    invoice_number=read("0000123"),
    series=read("C26TAA"),
    issue_date=read(date(2026, 11, 5)),
    seller_name=read("Acme Pty Ltd"),
    seller_tax_id=read("51 824 753 556"),
    buyer_name=read("Lan Co"),
    currency=read("AUD"),
    subtotal=read(Decimal("100.00")),
    tax_total=read(Decimal("10.00")),
    total=read(Decimal("111.00")),  # should be 110.00
    lines=[
        LineItem(
            description=read("Consulting"),
            quantity=read(Decimal("1")),
            unit_price=read(Decimal("100.00")),
            amount=read(Decimal("100.00")),
        )
    ],
)

for issue in validate_invoice(invoice, today=date(2026, 11, 22)):
    print(issue)
```

```text
ValidationIssue(code=<IssueCode.TOTAL_MISMATCH: 'total_mismatch'>, severity='error', field='total')
```

The ABN `51 824 753 556` is the worked example published by the Australian Business
Register, not a real business.

## Documentation

- [Architecture](docs/architecture.md): C4 diagrams, processing flow and what exists today.
- [Decisions](docs/decisions/): why money is `Decimal`, why MST is checked by format only,
  why we squash merge. One short record each, in MADR format.
- [AI-assisted workflow](docs/ai-workflow.md): how AI tools are used here, and the
  guardrails around them.
- [Requirements](docs/requirements.md) and [threat model](docs/threat-model.md).

## Repository layout

| Path | Purpose |
| --- | --- |
| `services/proofdesk/` | Python package: contracts and validation (parsing and extraction later) |
| `apps/web/` | TanStack Start app (Milestone 5) |
| `infra/` | AWS CDK in Python (Milestone 2) |
| `docs/` | Architecture, decisions, requirements, threat model |

## Contributing

Work starts from an issue, goes on a short branch, and reaches `main` through a pull
request that is squash merged. Tests come first. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md). Never commit real invoices or secrets.

## License

[MIT](LICENSE)
