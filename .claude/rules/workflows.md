---
paths:
  - ".github/workflows/**"
---

# GitHub Actions rules

- Set top-level `permissions: contents: read` and widen per job only where needed.
- Pin third-party actions to a full commit SHA with the tag in a comment:
  `uses: owner/action@<40-char-sha> # v1.2.3`.
- Never put `${{ github.event.* }}` inside a `run:` script. Pass it through `env:` instead.
- Never use `pull_request_target`.
