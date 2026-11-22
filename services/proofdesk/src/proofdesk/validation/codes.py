"""Every issue code validation can return. The front end translates these."""

from enum import StrEnum


class IssueCode(StrEnum):
    """Stable codes. Renaming one is a breaking change for the front end."""

    UNSUPPORTED_CURRENCY = "unsupported_currency"
    LINE_AMOUNT_MISMATCH = "line_amount_mismatch"
    SUBTOTAL_MISMATCH = "subtotal_mismatch"
    TOTAL_MISMATCH = "total_mismatch"
    SELLER_TAX_ID_INVALID = "seller_tax_id_invalid"
    ISSUE_DATE_IN_FUTURE = "issue_date_in_future"
    DUE_DATE_BEFORE_ISSUE_DATE = "due_date_before_issue_date"
    LOW_CONFIDENCE = "low_confidence"
    MISSING_VALUE = "missing_value"
