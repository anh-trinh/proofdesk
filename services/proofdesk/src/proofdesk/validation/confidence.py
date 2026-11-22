"""Flag fields the reader was unsure about or could not read."""

from decimal import Decimal

from proofdesk.contracts.invoice import Extracted, Invoice
from proofdesk.validation.issues import ValidationIssue

# Below this the reviewer is asked to check the field.
LOW_CONFIDENCE = Decimal("0.80")

# Fields that may legitimately be absent from a document.
_OPTIONAL_FIELDS = frozenset({"due_date"})


def _check_field(name: str, field: Extracted[object], optional: bool) -> ValidationIssue | None:
    if field.value is None:
        return None if optional else ValidationIssue("missing_value", "warning", name)
    if field.confidence < LOW_CONFIDENCE:
        return ValidationIssue("low_confidence", "warning", name)
    return None


def check_confidence(invoice: Invoice) -> list[ValidationIssue]:
    """Warn about each unreadable required field and each field below the threshold."""
    found: list[ValidationIssue | None] = []
    for name in type(invoice).model_fields:
        value = getattr(invoice, name)
        if isinstance(value, Extracted):
            found.append(_check_field(name, value, name in _OPTIONAL_FIELDS))
    for index, line in enumerate(invoice.lines):
        for name in type(line).model_fields:
            found.append(_check_field(f"lines[{index}].{name}", getattr(line, name), False))
    return [issue for issue in found if issue is not None]
