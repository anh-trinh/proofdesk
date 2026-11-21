"""Fields the reader was unsure about, or could not read, are flagged for the reviewer."""

from decimal import Decimal

from proofdesk.validation.confidence import LOW_CONFIDENCE, check_confidence
from proofdesk.validation.issues import ValidationIssue
from tests.factories import ex, make_invoice, make_line


def test_confident_invoice_gives_no_warning() -> None:
    assert check_confidence(make_invoice()) == []


def test_field_below_the_threshold_is_a_warning() -> None:
    invoice = make_invoice(seller_name=ex("Acme", Decimal("0.5")))
    assert check_confidence(invoice) == [
        ValidationIssue("low_confidence", "warning", "seller_name")
    ]


def test_field_exactly_at_the_threshold_is_accepted() -> None:
    invoice = make_invoice(seller_name=ex("Acme", LOW_CONFIDENCE))
    assert check_confidence(invoice) == []


def test_unreadable_required_field_is_a_warning() -> None:
    invoice = make_invoice(buyer_name=ex(None))
    assert check_confidence(invoice) == [ValidationIssue("missing_value", "warning", "buyer_name")]


def test_unreadable_due_date_is_fine_because_it_is_optional() -> None:
    assert check_confidence(make_invoice(due_date=ex(None))) == []


def test_low_confidence_on_a_line_names_the_line() -> None:
    line = make_line().model_copy(update={"amount": ex(Decimal("100.00"), Decimal("0.1"))})
    issues = check_confidence(make_invoice(lines=[line]))
    assert issues == [ValidationIssue("low_confidence", "warning", "lines[0].amount")]
