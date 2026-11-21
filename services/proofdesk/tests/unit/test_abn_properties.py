from hypothesis import given
from hypothesis import strategies as st

from proofdesk.validation.abn import is_valid_abn

_WEIGHTS = (10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19)


@st.composite
def valid_abns(draw: st.DrawFn) -> str:
    """Build a valid ABN without guessing and filtering.

    The first two digits carry weights 10 and 1, so the values (d1 - 1) * 10 + d2 cover
    every remainder from 0 to 88. For any nine trailing digits there is a pair that makes
    the weighted sum divisible by 89.
    """
    rest = draw(st.lists(st.integers(0, 9), min_size=9, max_size=9))
    rest_sum = sum(weight * digit for weight, digit in zip(_WEIGHTS[2:], rest, strict=True))
    needed = -rest_sum % 89
    first, second = needed // 10 + 1, needed % 10
    return "".join(str(digit) for digit in [first, second, *rest])


@given(valid_abns())
def test_every_constructed_abn_is_accepted(abn: str) -> None:
    assert is_valid_abn(abn)


@given(valid_abns())
def test_grouping_with_spaces_does_not_change_the_result(abn: str) -> None:
    grouped = f"{abn[:2]} {abn[2:5]} {abn[5:8]} {abn[8:]}"
    assert is_valid_abn(grouped)


@given(abn=valid_abns(), position=st.integers(0, 10), shift=st.integers(1, 9))
def test_changing_one_digit_always_breaks_the_checksum(abn: str, position: int, shift: int) -> None:
    # Each weight is below 89 and 89 is prime, so a single changed digit can never
    # move the weighted sum by a multiple of 89.
    changed = (int(abn[position]) + shift) % 10
    mistyped = abn[:position] + str(changed) + abn[position + 1 :]
    assert not is_valid_abn(mistyped)


@given(st.text())
def test_any_text_gives_a_bool_and_never_raises(text: str) -> None:
    assert isinstance(is_valid_abn(text), bool)
