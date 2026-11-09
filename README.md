# ProofDesk

Document AI with a human in the loop. Upload invoices and receipts, extract the data,
validate it, let a reviewer approve it, then export a clean CSV.

> Status: work in progress. This README grows with the project.

## What it does

- Reads e-invoice **XML** deterministically (no AI, no cost, 100% exact).
- Reads **PDF and images** with Claude on Amazon Bedrock, with a confidence score per field.
- Validates totals, tax rates and tax IDs (ABN, Vietnamese MST) and flags duplicates.
- Shows the original next to the extracted data so a person can correct and approve.
- Exports approved documents to CSV. Original files are deleted after export.

## Tech

TanStack Start (React), Python 3.13, Pydantic, AWS (Lambda, S3, SQS, DynamoDB, Cognito,
Bedrock, CloudFront), AWS CDK in Python, GitHub Actions.

## Repository layout

| Path | Purpose |
| --- | --- |
| `services/proofdesk/` | Python package: contracts, parsing, validation, extraction |
| `apps/web/` | TanStack Start app (added later) |
| `infra/` | AWS CDK (added later) |
| `docs/` | Requirements, ADRs, threat model |

## Development

```bash
make setup   # install Python dependencies
make test    # run tests with coverage
make lint    # ruff + mypy
```

## Security

See [SECURITY.md](SECURITY.md). Never commit real invoices or secrets.

## License

MIT
