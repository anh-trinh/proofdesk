"""The result of a validation rule: what is wrong, how serious it is, and where."""

from dataclasses import dataclass
from typing import Literal

# An error blocks approval. A warning is shown to the reviewer, who decides.
Severity = Literal["error", "warning"]


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One problem found in a document.

    The code is stable and translated by the front end. There is deliberately no
    message and no value: extracted values can be personal data, so issues carry
    codes and field names only, which are safe to log.
    """

    code: str
    severity: Severity
    field: str
