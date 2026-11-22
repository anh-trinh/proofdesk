"""validate_invoice runs every rule and returns all issues, not only the first."""

from datetime import date
from decimal import Decimal

from proofdesk.validation import IssueCode, validate_invoice
from proofdesk.validation.issues import ValidationIssue
from tests.factories import ex, make_invoice

TODAY = date(2026, 11, 22)


def test_valid_invoice_has_no_issues() -> None:
    assert validate_invoice(make_invoice(), today=TODAY) == []


def test_valid_abn_and_valid_mst_are_both_accepted() -> None:
    mst = make_invoice(seller_tax_id=ex("0123456789-001"))
    assert validate_invoice(mst, today=TODAY) == []


def test_seller_tax_id_that_is_neither_abn_nor_mst_is_an_error() -> None:
    invoice = make_invoice(seller_tax_id=ex("12345"))
    assert validate_invoice(invoice, today=TODAY) == [
        ValidationIssue("seller_tax_id_invalid", "error", "seller_tax_id")
    ]


def test_every_broken_rule_is_reported() -> None:
    invoice = make_invoice(
        seller_tax_id=ex("12345"),
        total=ex(Decimal("999.00")),
        issue_date=ex(date(2027, 1, 1)),
        buyer_name=ex(None),
    )
    codes = {issue.code for issue in validate_invoice(invoice, today=TODAY)}
    assert codes == {
        IssueCode.SELLER_TAX_ID_INVALID,
        IssueCode.TOTAL_MISMATCH,
        IssueCode.ISSUE_DATE_IN_FUTURE,
        IssueCode.MISSING_VALUE,
    }


def test_issue_codes_are_plain_strings_for_the_front_end() -> None:
    assert IssueCode.TOTAL_MISMATCH.value == "total_mismatch"


def test_unreadable_tax_id_is_left_to_the_confidence_rule() -> None:
    issues = validate_invoice(make_invoice(seller_tax_id=ex(None)), today=TODAY)
    assert [issue.code for issue in issues] == [IssueCode.MISSING_VALUE]
