---
paths:
  - "infra/**"
---

# Infrastructure rules

- No `*` in IAM actions or resources. If an AWS API cannot be scoped to a resource,
  add a comment that names the API and links its documentation.
- Prefer the construct's `grant_*` methods over hand-written policy statements.
- Every cdk-nag suppression carries a `reason` that explains why the finding does not apply.
- Set log retention explicitly on every log group and function.
- Never run `cdk deploy` or `cdk bootstrap`. The operator runs them.
