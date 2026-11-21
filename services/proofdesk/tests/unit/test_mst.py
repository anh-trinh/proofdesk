import pytest

from proofdesk.validation.mst import is_valid_mst


@pytest.mark.parametrize("mst", ["0100109106", "0312345678-001"], ids=["company", "branch"])
def test_accepts_ten_digits_or_ten_digits_and_a_three_digit_branch(mst: str) -> None:
    assert is_valid_mst(mst)


@pytest.mark.parametrize(
    "mst",
    [
        "",
        "010010910",
        "01001091066",
        "0100109106-",
        "0100109106-01",
        "0100109106-0011",
        "0100109106 001",
        "0100109106_001",
        "-0100109106",
        "010010910a",
        " 0100109106",
        "0100109106\n",
    ],
    ids=[
        "empty",
        "nine digits",
        "eleven digits",
        "dangling hyphen",
        "two digit branch",
        "four digit branch",
        "space instead of hyphen",
        "underscore",
        "leading hyphen",
        "letter",
        "leading space",
        "trailing newline",
    ],
)
def test_rejects_every_other_format(mst: str) -> None:
    assert not is_valid_mst(mst)


@pytest.mark.parametrize(
    "digit",
    ["\N{SUPERSCRIPT TWO}", "\N{ARABIC-INDIC DIGIT FIVE}", "\N{FULLWIDTH DIGIT FIVE}"],
    ids=["superscript two", "arabic-indic five", "fullwidth five"],
)
def test_rejects_digits_that_are_not_0_to_9(digit: str) -> None:
    assert not is_valid_mst(f"010010910{digit}")
    assert not is_valid_mst(f"0100109106-00{digit}")
