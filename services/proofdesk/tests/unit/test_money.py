from decimal import Decimal, localcontext

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


@pytest.mark.parametrize("bad", ["abc", "", "NaN", "Infinity"])
def test_garbage_and_non_finite_values_are_rejected(bad: str) -> None:
    with pytest.raises(MoneyError):
        to_money(bad, "AUD")


def test_amount_above_limit_is_rejected() -> None:
    with pytest.raises(MoneyError, match="amount_too_large"):
        to_money("1e30", "AUD")


def test_result_does_not_depend_on_caller_decimal_context() -> None:
    with localcontext() as ctx:
        ctx.prec = 50
        with pytest.raises(MoneyError, match="amount_too_large"):
            to_money("1e30", "AUD")
    with localcontext() as ctx:
        ctx.prec = 3
        assert to_money("123456.78", "AUD") == Decimal("123456.78")


def test_error_message_does_not_contain_the_input() -> None:
    with pytest.raises(MoneyError) as exc_info:
        to_money("INV-4711-secret", "AUD")
    assert "INV-4711-secret" not in str(exc_info.value)


@pytest.mark.parametrize(
    ("value", "currency", "expected"),
    [
        (10, "USD", Decimal("10.00")),
        (Decimal("2.5"), "VND", Decimal("3")),
        ("-1.005", "AUD", Decimal("-1.01")),
    ],
)
def test_int_decimal_and_negative_inputs(
    value: str | int | Decimal, currency: str, expected: Decimal
) -> None:
    assert to_money(value, currency) == expected


@pytest.mark.parametrize("currency", ["XXX", "aud"])
def test_unknown_or_lowercase_currency_is_rejected(currency: str) -> None:
    with pytest.raises(MoneyError, match="unsupported_currency"):
        to_money("10", currency)
