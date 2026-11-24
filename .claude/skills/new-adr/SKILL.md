---
name: new-adr
description: Write a new architecture decision record in docs/decisions/ in MADR 4.0.0 format.
disable-model-invocation: true
argument-hint: "[title]"
model: opus
effort: high
---

Write an architecture decision record for: $ARGUMENTS

1. Read `docs/decisions/0000-template.md` and list `docs/decisions/` to find the existing
   numbers. If `.handbook/` exists, check its ADR table for a number reserved for this
   decision and use it; otherwise use the next free number. Never reuse a number.
2. Create `docs/decisions/NNNN-title-with-dashes.md`: four digits, then the title in
   lowercase with dashes.
3. Fill every section of the template in MADR 4.0.0:
   - Context and Problem Statement: the situation, the constraint and the question.
   - Decision Drivers: link each to a requirement or NFR with its number where one exists.
   - Considered Options: at least two real options, including the one rejected.
   - Decision Outcome: the chosen option and the reason, tied to the drivers.
   - Consequences: good and bad, including what is accepted.
   - Confirmation: the test, CI rule or review item that checks the decision holds.
   - Pros and Cons of the Options: one subsection per option.
   - More Information: links to issues, pull requests and related ADRs.
4. Set `status: proposed`, today's date, and `decision-makers` to the operator. The operator
   changes the status to `accepted` in review.
5. Do not invent facts. Mark anything not verified as "Not verified" with what would verify it.
