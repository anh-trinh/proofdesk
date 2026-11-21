"""Check that line amounts, the subtotal and the grand total agree exactly."""

from decimal import Decimal

from proofdesk.contracts.invoice import Invoice
from proofdesk.contracts.money import CURRENCY_EXPONENTS, to_money
from proofdesk.validation.issues import ValidationIssue


def _error(code: str, field: str) -> ValidationIssue:
    return ValidationIssue(code=code, severity="error", field=field)


def check_totals(invoice: Invoice) -> list[ValidationIssue]:
    """Return an error for each amount that does not match what it is made of.

    Amounts are compared exactly after rounding to the currency's precision, with
    no tolerance: a cent of difference is a real difference on a tax document.
    An unreadable amount is skipped here, because reporting missing fields is a
    separate rule (confidence).
    """
    currency = invoice.currency.value
    if currency not in CURRENCY_EXPONENTS:
        return [_error("unsupported_currency", "currency")]

    def money(value: Decimal | None) -> Decimal | None:
        return None if value is None else to_money(value, currency)

    issues: list[ValidationIssue] = []
    line_amounts: list[Decimal | None] = []
    for index, line in enumerate(invoice.lines):
        amount = money(line.amount.value)
        line_amounts.append(amount)
        quantity, unit_price = line.quantity.value, line.unit_price.value
        if amount is None or quantity is None or unit_price is None:
            continue
        if to_money(quantity * unit_price, currency) != amount:
            issues.append(_error("line_amount_mismatch", f"lines[{index}].amount"))

    subtotal = money(invoice.subtotal.value)
    known = [a for a in line_amounts if a is not None]
    if subtotal is not None and len(known) == len(line_amounts) and sum(known) != subtotal:
        issues.append(_error("subtotal_mismatch", "subtotal"))

    tax = money(invoice.tax_total.value)
    total = money(invoice.total.value)
    if subtotal is not None and tax is not None and total is not None and subtotal + tax != total:
        issues.append(_error("total_mismatch", "total"))
    return issues
