---
status: accepted
date: 2026-11-21
decision-makers: Anh Trinh
---

# Check the Vietnamese tax ID (MST) by format only

## Context and Problem Statement

The Australian ABN has a published checksum, and ProofDesk verifies it. For the Vietnamese
tax ID (MST) we did not find an official, current specification of a check digit, and the
algorithms on blogs have no clear source. Should the MST check include a checksum?

## Decision Drivers

* A valid invoice must never be rejected because of a wrong rule
* Only rules with an official source belong in validation
* The reviewer always sees the value next to the original document

## Considered Options

* Check the format only
* Copy a checksum from an unofficial source
* Look the MST up in the tax authority's online service

## Decision Outcome

Chosen option: "Check the format only", because a wrong checksum would reject real invoices,
which costs more than letting a mistyped number through to a reviewer. An MST is plausible
when it is 10 digits, or 10 digits, a hyphen and 3 digits (a branch). No check digit is
computed (`proofdesk.validation.mst.is_valid_mst`).

### Consequences

* Good, because no valid invoice is rejected by an unverified rule.
* Bad, because some mistyped MSTs pass validation. The reviewer still sees the value next to
  the original document.
* Bad, because an individual's tax ID can be a 12 digit citizen ID. That is personal data
  and is handled by the PII work in Milestone 4.

### Confirmation

`tests/unit/test_mst.py` and `tests/unit/test_mst_properties.py` fix the accepted format. If
an official check digit rule is found, a new ADR replaces this one and the rule is added
with tests built from published company tax IDs.

## Pros and Cons of the Options

### Copy a checksum from an unofficial source

* Good, because it catches more typing mistakes.
* Bad, because a wrong algorithm rejects valid invoices, and the source cannot be verified.

### Look the MST up in the tax authority's online service

* Good, because it checks that the company exists.
* Bad, because it adds a network dependency, rate limits and terms of use, and it is out of
  scope for v1.0.
