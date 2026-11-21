"""Australian Business Number (ABN) check.

The checksum is published by the Australian Business Register (ABR):
https://abr.business.gov.au/Help/AbnFormat
"""

import re

# Weights from the ABR algorithm, one per digit of the 11 digit number.
_WEIGHTS = (10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19)
_MODULUS = 89

# [0-9], not \d and not str.isdigit(): those also match digits from other scripts
# (such as the superscript two) that int() rejects or that are not ASCII digits.
_ABN_DIGITS = re.compile(r"[0-9]{11}")


def is_valid_abn(text: str) -> bool:
    """Return True if text is an 11 digit ABN with a valid checksum.

    Plain spaces are ignored, so "51 824 753 556" and "51824753556" are both accepted.
    Any other character, including tabs, no-break spaces and hyphens, makes it invalid.
    """
    digits = text.replace(" ", "")
    if _ABN_DIGITS.fullmatch(digits) is None:
        return False
    values = [int(char) for char in digits]
    values[0] -= 1  # the ABR algorithm subtracts 1 from the first digit
    total = sum(weight * value for weight, value in zip(_WEIGHTS, values, strict=True))
    return total % _MODULUS == 0
