---
status: accepted
date: 2026-11-19
decision-makers: Anh Trinh
---

# Money is `Decimal` in Python and a string in JSON

## Context and Problem Statement

Invoice totals must match to the smallest unit of the currency (1 cent, 1 dong). Binary
floating point cannot represent most decimal fractions exactly, so `0.1 + 0.2 != 0.3`. The
amounts also cross a boundary to a TypeScript front end, where JSON numbers become floats.
How should amounts be represented in Python and on the wire?

## Decision Drivers

* Totals compare exactly, with no tolerance
* Values survive the JSON boundary to JavaScript unchanged
* The AI model returns amounts as decimal text, not as minor units

## Considered Options

* `Decimal` in Python, string in JSON
* `float` with a tolerance
* Integer minor units (cents)

## Decision Outcome

Chosen option: "`Decimal` in Python, string in JSON", because it is exact in both places and
matches the decimal text the model and the XML provide.

* Amounts are `decimal.Decimal`. A `float`, NaN or infinity passed into a money field is
  rejected (`proofdesk.contracts.invoice.Number`, `proofdesk.contracts.money.to_money`).
* Amounts are rounded with `ROUND_HALF_UP` to the currency's exponent: AUD and USD 2, VND 0.
* In JSON, amounts are strings (`"110.00"`).

### Consequences

* Good, because validation compares totals exactly, without tolerance hacks.
* Bad, because the front end must treat amounts as strings and format them with
  `Intl.NumberFormat` without arithmetic, or use a decimal library if it ever adds them.
* Bad, because an unknown currency is an error until it is added to `CURRENCY_EXPONENTS`.

### Confirmation

Unit tests reject floats and non-finite values (`test_float_is_rejected_for_money`,
`test_non_finite_amounts_are_rejected`) and check that money is a string in JSON. CLAUDE.md
marks a `float` used for money as a High finding in code review.

## Pros and Cons of the Options

### `float` with a tolerance

* Good, because it is the default numeric type in Python and JavaScript.
* Bad, because a tolerance hides real mismatches and makes tests depend on rounding noise.

### Integer minor units (cents)

* Good, because integer arithmetic is exact.
* Bad, because every boundary must convert, and the AI model returns decimal text.
