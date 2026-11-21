import pytest

from proofdesk.validation.abn import is_valid_abn

# Both numbers are worked examples published by the Australian Business Register.
REGISTER_EXAMPLES = ["51 824 753 556", "53 004 085 616"]


@pytest.mark.parametrize("abn", REGISTER_EXAMPLES)
def test_accepts_abn_with_valid_checksum(abn: str) -> None:
    assert is_valid_abn(abn)


@pytest.mark.parametrize("abn", REGISTER_EXAMPLES)
def test_accepts_abn_written_without_spaces(abn: str) -> None:
    assert is_valid_abn(abn.replace(" ", ""))


def test_rejects_abn_with_wrong_check_digit() -> None:
    assert not is_valid_abn("51 824 753 557")


@pytest.mark.parametrize(
    "abn",
    ["", "   ", "51 824 753 55", "51 824 753 5566", "5182475355"],
    ids=["empty", "only spaces", "ten digits", "twelve digits", "ten digits no spaces"],
)
def test_rejects_wrong_length(abn: str) -> None:
    assert not is_valid_abn(abn)


@pytest.mark.parametrize(
    "abn",
    [
        "51-824-753-556",
        "51 824 753 55a",
        "51\t824\t753\t556",
        "51\N{NO-BREAK SPACE}824\N{NO-BREAK SPACE}753\N{NO-BREAK SPACE}556",
        "51 824 753 556\n",
    ],
    ids=["hyphens", "letter", "tabs", "no-break spaces", "trailing newline"],
)
def test_rejects_separators_and_characters_other_than_digits_and_spaces(abn: str) -> None:
    assert not is_valid_abn(abn)


@pytest.mark.parametrize(
    "digit",
    ["\N{SUPERSCRIPT TWO}", "\N{ARABIC-INDIC DIGIT FIVE}", "\N{FULLWIDTH DIGIT FIVE}"],
    ids=["superscript two", "arabic-indic five", "fullwidth five"],
)
def test_rejects_digits_that_look_like_numbers_but_are_not_0_to_9(digit: str) -> None:
    # str.isdigit() accepts all of these, and int() rejects the first one.
    assert not is_valid_abn(f"51 824 753 55{digit}")


def test_rejects_oversized_input_even_when_the_digits_are_valid() -> None:
    assert not is_valid_abn("51 824 753 556" + " " * 1_000)
