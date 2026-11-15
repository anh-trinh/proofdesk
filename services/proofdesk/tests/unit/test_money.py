from decimal import Decimal

import pytest

from proofdesk.contracts.money import MoneyError, to_money


def test_decimal_strings_add_up_exactly() -> None:
    # With float, 0.1 + 0.2 == 0.30000000000000004. With Decimal it is exact.
    total = to_money("0.1", "AUD") + to_money("0.2", "AUD")
    assert total == to_money("0.3", "AUD")


def test_amount_is_rounded_half_up_to_two_digits_for_aud() -> None:
    assert to_money("1.005", "AUD") == Decimal("1.01")
    assert to_money("1.004", "AUD") == Decimal("1.00")


def test_vnd_has_no_decimal_digits() -> None:
    assert to_money("1500000", "VND") == Decimal("1500000")
    assert to_money("1500000.5", "VND") == Decimal("1500001")


@pytest.mark.parametrize("bad", [0.1, True])
def test_float_and_bool_are_rejected(bad: object) -> None:
    with pytest.raises(MoneyError):
        to_money(bad, "AUD")  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", ["abc", "", "NaN", "Infinity", "1e30"])
def test_garbage_and_non_finite_values_are_rejected(bad: str) -> None:
    with pytest.raises(MoneyError):
        to_money(bad, "AUD")


def test_unknown_currency_is_rejected() -> None:
    with pytest.raises(MoneyError):
        to_money("10", "XXX")
