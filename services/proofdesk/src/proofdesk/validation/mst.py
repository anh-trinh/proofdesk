"""Vietnamese tax ID (MST) check. Format only: see ADR-0014."""

import re

# 10 digits, optionally followed by a hyphen and a 3 digit branch code.
# [0-9], not \d and not str.isdigit(): those also match digits from other scripts.
_MST = re.compile(r"[0-9]{10}(?:-[0-9]{3})?")


def is_valid_mst(text: str) -> bool:
    """Return True if text looks like a Vietnamese tax ID: 10 digits, or 10 digits-3 digits.

    The check digit is not verified, because no official specification was found.
    Whitespace is not ignored: the parser trims values, and the reviewer sees the rest.
    """
    return _MST.fullmatch(text) is not None
