"""A key that is the same for the same invoice however its fields were formatted."""

import hashlib
import re

from proofdesk.contracts.invoice import Invoice

_NOT_ALPHANUMERIC = re.compile(r"[^0-9a-z]")


def _normalise(text: str) -> str:
    return _NOT_ALPHANUMERIC.sub("", text.casefold())


def duplicate_key(invoice: Invoice) -> str | None:
    """Return a SHA-256 key for seller, series, number and issue date, or None if any is unread.

    Spacing, case and punctuation are ignored. Leading zeros are kept, because
    "0123" and "123" can be two different invoices. The key is a hash so it is safe
    to log and store: the tax ID and invoice number are not recoverable from it.
    """
    seller = invoice.seller_tax_id.value
    series = invoice.series.value
    number = invoice.invoice_number.value
    issued = invoice.issue_date.value
    if seller is None or series is None or number is None or issued is None:
        return None
    parts = (_normalise(seller), _normalise(series), _normalise(number), issued.isoformat())
    return hashlib.sha256("|".join(parts).encode()).hexdigest()
