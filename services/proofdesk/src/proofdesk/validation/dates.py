"""Date rules. These are warnings: an odd date can still be real, so a reviewer decides."""

from datetime import date

from proofdesk.contracts.invoice import Invoice
from proofdesk.validation.issues import ValidationIssue


def _warning(code: str, field: str) -> ValidationIssue:
    return ValidationIssue(code=code, severity="warning", field=field)


def check_dates(invoice: Invoice, today: date) -> list[ValidationIssue]:
    """Warn about an issue date in the future or a due date before the issue date.

    `today` is passed in, never read from the clock, so the rule is deterministic.
    """
    issued = invoice.issue_date.value
    due = invoice.due_date.value
    issues: list[ValidationIssue] = []
    if issued is not None and issued > today:
        issues.append(_warning("issue_date_in_future", "issue_date"))
    if issued is not None and due is not None and due < issued:
        issues.append(_warning("due_date_before_issue_date", "due_date"))
    return issues
