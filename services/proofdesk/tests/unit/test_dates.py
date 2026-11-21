"""Date rules produce warnings: a reviewer decides, because an odd date can still be real."""

from datetime import date

from proofdesk.validation.dates import check_dates
from proofdesk.validation.issues import ValidationIssue
from tests.factories import ex, make_invoice

TODAY = date(2026, 11, 21)


def test_ordinary_dates_give_no_warning() -> None:
    invoice = make_invoice(due_date=ex(date(2026, 12, 5)))
    assert check_dates(invoice, today=TODAY) == []


def test_issue_date_today_is_not_in_the_future() -> None:
    assert check_dates(make_invoice(issue_date=ex(TODAY)), today=TODAY) == []


def test_future_issue_date_is_a_warning() -> None:
    invoice = make_invoice(issue_date=ex(date(2026, 11, 22)))
    assert check_dates(invoice, today=TODAY) == [
        ValidationIssue("issue_date_in_future", "warning", "issue_date")
    ]


def test_due_date_before_issue_date_is_a_warning() -> None:
    invoice = make_invoice(due_date=ex(date(2026, 11, 4)))
    assert check_dates(invoice, today=TODAY) == [
        ValidationIssue("due_date_before_issue_date", "warning", "due_date")
    ]


def test_due_date_on_the_issue_date_is_fine() -> None:
    assert check_dates(make_invoice(due_date=ex(date(2026, 11, 5))), today=TODAY) == []


def test_unreadable_dates_are_skipped() -> None:
    assert check_dates(make_invoice(issue_date=ex(None)), today=TODAY) == []
