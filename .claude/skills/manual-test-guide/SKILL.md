---
name: manual-test-guide
description: Write the manual test session for a ProofDesk milestone or feature, then record the results the operator reports.
disable-model-invocation: true
argument-hint: "[milestone-or-feature]"
model: sonnet
effort: medium
---

Write the manual test guide for: $ARGUMENTS

## Read first

1. If `.handbook/` exists, the handbook part that holds the manual test task for
   $ARGUMENTS (find it in `.handbook/INDEX.md`).
2. The user stories and acceptance criteria in `docs/requirements.md` that the milestone or
   feature covers.
3. The code and tests for those stories, so every step names a real command, screen or field.

## Write `docs/testing/manual/<name>.md`

Use a lowercase, dash-separated `<name>` from $ARGUMENTS, for example `m1-domain-core`.
Write in English. Sections, in this order:

1. **Scope:** what is tested, what is not, and the commit under test.
2. **Coverage:** a table that maps every acceptance criterion in scope to at least one case
   ID. A criterion with no case is an error; fix it before you continue.
3. **Setup:** prerequisites, seed commands and reset commands that can be copied and run.
4. **Cases:** one table per feature with the columns ID, Criterion, Steps (numbered),
   Expected, Actual, Pass/Fail. Leave Actual and Pass/Fail empty.
5. **Negative and edge cases:** invalid input, limits, repeated actions, and wrong-tenant
   access where it applies.
6. **Visible security checks:** what the operator can see for themselves, for example an
   error code instead of a stack trace, or no personal data in a log line.
7. **UI checks** (only once there is a UI): keyboard only, visible focus, a screen reader
   pass, and a 375 px phone width.
8. **Where to look in the logs:** for each action, the log group or command and the field
   that proves it happened (IDs and codes only).
9. **Cleanup:** commands that remove what the session created.
10. **Time:** an estimate per case and a total. Split the session by feature if the total
    is over 30 minutes.

## While the operator runs the session

- Guide the operator through each case in Vietnamese, one case at a time.
- Never mark a case as passed yourself. Record only what the operator reports, with the
  date and the commit SHA.
- A failed case becomes a bug issue with the case ID, steps and actual result. Link the
  issue in the Actual column.
