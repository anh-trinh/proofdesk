# Threat model (first version)

Method: STRIDE on each data flow, plus the OWASP Top 10 for LLM applications for the AI step.
This table grows with every milestone. Each row must name the control and the test that
proves it.

| Asset / flow | Threat | Control | Proving test |
| --- | --- | --- | --- |
| XML upload | XXE, entity expansion (denial of service) | `defusedxml` with DTDs and entities forbidden | `test_xml_with_an_external_entity_is_rejected` |
| File upload | Wrong type, oversized file, disguised executable | Size limit, content sniffing by magic bytes, presigned POST conditions | Milestone 2 |
| Tenant data | One tenant reads another's document (IDOR) | `tenantId` taken from the session, never from the request; 404 on mismatch | Milestone 6 |
| AI extraction | Prompt injection inside a document | Forced tool use, schema validation, output never executed or trusted for authorization | Milestone 3 |
| Logs | Personal data or extracted values leaked into logs | Logger wrapper that accepts only IDs and codes | Milestone 4 |
| Audit trail | A user or admin edits history | Separate table, `PutItem` only, no update or delete in IAM | Milestone 6 |
| Cost | Abuse of the AI step | Per-tenant quota, budget alarms, Haiku model | Milestone 6 and 7 |
| Repository | Secret or real invoice committed | gitleaks in pre-commit and CI, `samples/private/` ignored | Fake key is blocked by the pre-commit hook |
