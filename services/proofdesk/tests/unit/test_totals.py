"""Totals must agree exactly: line amounts, the subtotal and the grand total."""

from decimal import Decimal

import pytest

from proofdesk.validation.issues import ValidationIssue
from proofdesk.validation.totals import check_totals
from tests.factories import ex, make_invoice, make_line


def codes(issues: list[ValidationIssue]) -> list[str]:
    return [issue.code for issue in issues]


def test_correct_totals_give_no_issue() -> None:
    assert check_totals(make_invoice()) == []


@pytest.mark.parametrize(
    ("currency", "line", "subtotal", "tax", "total"),
    [
        ("USD", ("2", "19.99", "39.98"), "39.98", "4.00", "43.98"),
        ("VND", ("3", "100000", "300000"), "300000", "30000", "330000"),
    ],
)
def test_correct_totals_in_each_supported_currency(
    currency: str, line: tuple[str, str, str], subtotal: str, tax: str, total: str
) -> None:
    invoice = make_invoice(
        currency=ex(currency),
        lines=[make_line(quantity=line[0], unit_price=line[1], amount=line[2])],
        subtotal=ex(Decimal(subtotal)),
        tax_total=ex(Decimal(tax)),
        total=ex(Decimal(total)),
    )
    assert check_totals(invoice) == []


def test_grand_total_that_does_not_add_up_is_an_error() -> None:
    invoice = make_invoice(total=ex(Decimal("111.00")))
    assert check_totals(invoice) == [ValidationIssue("total_mismatch", "error", "total")]


def test_subtotal_that_differs_from_the_lines_is_an_error() -> None:
    invoice = make_invoice(subtotal=ex(Decimal("99.00")), total=ex(Decimal("109.00")))
    assert codes(check_totals(invoice)) == ["subtotal_mismatch"]


def test_line_amount_that_differs_from_quantity_times_price_is_an_error() -> None:
    invoice = make_invoice(lines=[make_line(quantity="2", unit_price="50.00", amount="90.00")])
    issues = check_totals(invoice)
    assert ValidationIssue("line_amount_mismatch", "error", "lines[0].amount") in issues


def test_a_cent_of_difference_is_still_a_mismatch() -> None:
    invoice = make_invoice(total=ex(Decimal("110.01")))
    assert codes(check_totals(invoice)) == ["total_mismatch"]


def test_line_amount_is_compared_after_rounding_to_the_currency() -> None:
    line = make_line(quantity="3", unit_price="0.335", amount="1.01")
    invoice = make_invoice(
        lines=[line],
        subtotal=ex(Decimal("1.01")),
        tax_total=ex(Decimal("0.00")),
        total=ex(Decimal("1.01")),
    )
    assert check_totals(invoice) == []


def test_unsupported_currency_is_an_issue_not_an_exception() -> None:
    invoice = make_invoice(currency=ex("EUR"))
    assert check_totals(invoice) == [ValidationIssue("unsupported_currency", "error", "currency")]


def test_missing_currency_is_an_unsupported_currency_issue() -> None:
    invoice = make_invoice(currency=ex(None))
    assert codes(check_totals(invoice)) == ["unsupported_currency"]


def test_unreadable_amounts_are_skipped_rather_than_reported_as_mismatches() -> None:
    invoice = make_invoice(tax_total=ex(None))
    assert check_totals(invoice) == []
