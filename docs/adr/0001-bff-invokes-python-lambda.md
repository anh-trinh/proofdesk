# ADR-0001: The web backend calls the Python API with Lambda invoke, no public API

- Status: accepted
- Date: 2026-11-05

## Context
The TanStack Start server (BFF) needs to call the Python business logic. A public API
Gateway would add cost and attack surface, and we already authenticate users in the BFF.

## Decision
The `web` Lambda invokes the `api` Lambda directly with IAM permission
`lambda:InvokeFunction` on that single function. The `api` Lambda has no URL and no public
route.

## Consequences
- Smaller attack surface; no API Gateway cost.
- The BFF must pass the verified `actor` (user, tenant, role) in every call. The Python side
  trusts it only because nothing else can invoke the function.
- Python cannot be called from a browser or a third party. If we ever need a public API,
  we add one with its own ADR.

## Alternatives considered
- API Gateway + JWT authorizer: more moving parts, extra cost, public endpoint.
- Lambda Function URL for `api`: public URL, needs its own auth layer.
