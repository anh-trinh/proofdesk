"""Validation rules for extracted documents."""

from datetime import date

from proofdesk.contracts.invoice import Invoice
from proofdesk.validation.abn import is_valid_abn
from proofdesk.validation.codes import IssueCode
from proofdesk.validation.confidence import check_confidence
from proofdesk.validation.dates import check_dates
from proofdesk.validation.issues import ValidationIssue
from proofdesk.validation.mst import is_valid_mst
from proofdesk.validation.totals import check_totals

__all__ = ["IssueCode", "ValidationIssue", "validate_invoice"]


def _check_seller_tax_id(invoice: Invoice) -> list[ValidationIssue]:
    """The seller ID must be a valid Australian ABN or a Vietnamese MST.

    An unreadable ID is reported by the confidence rule, not here.
    """
    text = invoice.seller_tax_id.value
    if text is None or is_valid_abn(text) or is_valid_mst(text):
        return []
    return [ValidationIssue(IssueCode.SELLER_TAX_ID_INVALID, "error", "seller_tax_id")]


def validate_invoice(invoice: Invoice, today: date) -> list[ValidationIssue]:
    """Run every rule and return all issues, not only the first."""
    return [
        *_check_seller_tax_id(invoice),
        *check_totals(invoice),
        *check_dates(invoice, today),
        *check_confidence(invoice),
    ]
