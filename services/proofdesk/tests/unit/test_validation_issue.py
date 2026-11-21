import dataclasses

import pytest

from proofdesk.validation.issues import ValidationIssue


def test_an_issue_is_a_code_a_severity_and_the_field_it_is_about() -> None:
    issue = ValidationIssue(code="seller_tax_id_invalid", severity="error", field="seller_tax_id")
    assert (issue.code, issue.severity, issue.field) == (
        "seller_tax_id_invalid",
        "error",
        "seller_tax_id",
    )


def test_an_issue_cannot_be_changed_after_creation() -> None:
    issue = ValidationIssue(code="total_mismatch", severity="error", field="total")
    with pytest.raises(dataclasses.FrozenInstanceError):
        issue.code = "other"  # type: ignore[misc]


def test_equal_issues_are_equal_and_can_be_used_in_a_set() -> None:
    first = ValidationIssue(code="total_mismatch", severity="error", field="total")
    second = ValidationIssue(code="total_mismatch", severity="error", field="total")
    assert first == second
    assert len({first, second}) == 1


def test_an_issue_has_no_place_for_the_extracted_value() -> None:
    # Extracted values can be personal data, and logs carry codes and field names only.
    names = {field.name for field in dataclasses.fields(ValidationIssue)}
    assert names == {"code", "severity", "field"}
