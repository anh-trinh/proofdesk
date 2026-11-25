---
paths:
  - "apps/web/**"
---

# Web app rules

- The actor and `tenantId` come only from the verified session, read in middleware.
  Never take them from the request body, query string or headers.
- The AWS SDK is imported only in server-only modules.
- No `dangerouslySetInnerHTML`.
- Amounts stay strings end to end and are formatted for display with `Intl.NumberFormat`.
