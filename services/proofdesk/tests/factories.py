"""Test helpers that build valid objects, so each test only states what it cares about."""

from datetime import date
from decimal import Decimal
from typing import Any

from proofdesk.contracts.invoice import Extracted, Invoice, LineItem

ONE = Decimal("1")


def ex[T](value: T | None, confidence: Decimal = ONE) -> Extracted[T]:
    """Wrap a value as a read field. An unreadable field (None) always has confidence 0."""
    return Extracted[T](value=value, confidence=confidence if value is not None else Decimal("0"))


def make_line(
    description: str = "Consulting",
    quantity: str = "1",
    unit_price: str = "100.00",
    amount: str = "100.00",
) -> LineItem:
    return LineItem(
        description=ex(description),
        quantity=ex(Decimal(quantity)),
        unit_price=ex(Decimal(unit_price)),
        amount=ex(Decimal(amount)),
    )


def make_invoice(**overrides: Any) -> Invoice:
    """A valid AUD invoice: one line of 100.00 plus 10.00 GST gives 110.00.

    The ABN 51 824 753 556 is the worked example published by the Australian Business
    Register, not a real business's data.
    """
    fields: dict[str, Any] = {
        "invoice_number": ex("0000123"),
        "series": ex("C26TAA"),
        "issue_date": ex(date(2026, 11, 5)),
        "seller_name": ex("Acme Pty Ltd"),
        "seller_tax_id": ex("51 824 753 556"),
        "buyer_name": ex("Lan Co"),
        "currency": ex("AUD"),
        "subtotal": ex(Decimal("100.00")),
        "tax_total": ex(Decimal("10.00")),
        "total": ex(Decimal("110.00")),
        "lines": [make_line()],
    }
    fields.update(overrides)
    return Invoice(**fields)
