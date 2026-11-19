import json
from decimal import Decimal

import pytest
from pydantic import ValidationError

from proofdesk.contracts.invoice import Extracted, Invoice, Number
from tests.factories import make_invoice


def test_confidence_must_be_between_zero_and_one() -> None:
    with pytest.raises(ValidationError):
        Extracted[str](value="x", confidence=Decimal("1.5"))


def test_unreadable_field_is_empty_not_guessed() -> None:
    field = Extracted[str]()
    assert field.value is None
    assert field.confidence == Decimal("0")


def test_money_is_a_string_in_json_never_a_number() -> None:
    data = json.loads(make_invoice().model_dump_json())
    assert data["total"]["value"] == "110.00"


def test_float_is_rejected_for_money() -> None:
    with pytest.raises(ValidationError):
        Extracted[Number](value=0.1, confidence=Decimal("1"))  # type: ignore[arg-type]


@pytest.mark.parametrize("text", ["NaN", "Infinity", "-Infinity", "sNaN"])
def test_non_finite_amounts_are_rejected(text: str) -> None:
    with pytest.raises(ValidationError):
        Extracted[Number].model_validate({"value": text, "confidence": "1"})


def test_json_round_trip_keeps_the_exact_amounts() -> None:
    original = make_invoice()
    again = Invoice.model_validate_json(original.model_dump_json())
    assert again == original


def test_unknown_fields_are_rejected() -> None:
    payload = json.loads(make_invoice().model_dump_json())
    payload["surprise"] = "x"
    with pytest.raises(ValidationError):
        Invoice.model_validate(payload)


def test_invoice_cannot_be_changed_after_creation() -> None:
    invoice = make_invoice()
    with pytest.raises(ValidationError):
        invoice.total = invoice.subtotal
