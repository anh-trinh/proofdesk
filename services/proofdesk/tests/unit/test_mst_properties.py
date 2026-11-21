from hypothesis import given
from hypothesis import strategies as st

from proofdesk.validation.mst import is_valid_mst


@given(st.from_regex(r"[0-9]{10}(-[0-9]{3})?", fullmatch=True))
def test_every_ten_digit_number_with_an_optional_branch_is_accepted(mst: str) -> None:
    assert is_valid_mst(mst)


@given(st.text())
def test_any_text_gives_a_bool_and_never_raises(text: str) -> None:
    assert isinstance(is_valid_mst(text), bool)


@given(st.text(alphabet="0123456789-", max_size=20).filter(lambda text: len(text) not in (10, 14)))
def test_a_length_other_than_ten_or_fourteen_is_never_accepted(text: str) -> None:
    assert not is_valid_mst(text)
