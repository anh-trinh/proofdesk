"""The invoice contract: one model shared by the XML parser, the AI reader and validation."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer


def _reject_float(value: object) -> object:
    """Reject floats before Pydantic converts them, since 0.1 is not exactly 0.1 (ADR-0007)."""
    if isinstance(value, bool | float):
        raise ValueError("float is not accepted; send a string or Decimal")
    return value


# An exact, finite decimal number. Floats are rejected on input; in JSON it is a string.
Number = Annotated[
    Decimal,
    BeforeValidator(_reject_float),
    Field(allow_inf_nan=False),
    PlainSerializer(str, return_type=str, when_used="json"),
]

# How sure the reader is, from 0 (no idea) to 1 (certain).
Confidence = Annotated[Decimal, BeforeValidator(_reject_float), Field(ge=0, le=1)]


class Extracted[T](BaseModel):
    """One extracted field: a value (or None if unreadable) and how sure we are."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    value: T | None = None
    confidence: Confidence = Decimal("0")


class LineItem(BaseModel):
    """One invoice line. Per-line tax rates are added with the extraction schema (Milestone 3)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    description: Extracted[str]
    quantity: Extracted[Number]
    unit_price: Extracted[Number]
    amount: Extracted[Number]


class Invoice(BaseModel):
    """An invoice as read from a document, before validation and human review."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    invoice_number: Extracted[str]
    series: Extracted[str]
    issue_date: Extracted[date]
    seller_name: Extracted[str]
    seller_tax_id: Extracted[str]
    buyer_name: Extracted[str]
    currency: Extracted[str]
    subtotal: Extracted[Number]
    tax_total: Extracted[Number]
    total: Extracted[Number]
    lines: list[LineItem]
