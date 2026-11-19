---
status: accepted
date: 2026-11-05
decision-makers: Anh Trinh
---

# The web backend calls the Python API with Lambda invoke, not a public API

## Context and Problem Statement

The TanStack Start server (the backend for frontend, BFF) needs to call the Python business
logic. Users are already authenticated in the BFF. How should the BFF reach the Python code
without adding cost or a second public entry point?

## Decision Drivers

* Smallest attack surface: no public endpoint that needs its own authentication
* Monthly cost below 5 USD (NFR-03)
* The verified user and tenant must reach the Python side unchanged

## Considered Options

* Direct Lambda invoke from the BFF
* API Gateway with a JWT authoriser
* Lambda Function URL for the Python API

## Decision Outcome

Chosen option: "Direct Lambda invoke", because it adds no public endpoint and no cost. The
`web` Lambda invokes the `api` Lambda with the IAM permission `lambda:InvokeFunction` on
that single function. The `api` Lambda has no URL and no public route.

### Consequences

* Good, because the attack surface is smaller and there is no API Gateway cost.
* Bad, because the BFF must pass the verified `actor` (user, tenant, role) in every call,
  and the Python side trusts it only because nothing else can invoke the function.
* Bad, because Python cannot be called from a browser or a third party. A public API would
  need a new ADR.

### Confirmation

A CDK assertion test checks that the `api` function has no Function URL and that only the
`web` function role holds `lambda:InvokeFunction` on it (Milestone 2).

## Pros and Cons of the Options

### API Gateway with a JWT authoriser

* Good, because it is the conventional public API pattern.
* Bad, because it adds a public endpoint, more moving parts and a monthly cost.

### Lambda Function URL for the Python API

* Good, because it is free and simple.
* Bad, because the URL is public and needs its own authentication layer.
