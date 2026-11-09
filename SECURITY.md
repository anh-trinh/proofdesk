# Security Policy

## Reporting a vulnerability

Please use GitHub's **Report a vulnerability** button (Security tab) to report privately.
Do not open a public issue for security problems. You can expect a first reply within
7 days.

## Scope and data rules

- This is a demo project. Do not upload real invoices or personal data to any deployment.
- The repository must never contain secrets, real documents, or real personal data.
  Test data is synthetic (see `tools/synth/` once added).
- Secrets live in AWS SSM Parameter Store, never in git.

## Supported versions

Only the latest release on `main` is supported.
