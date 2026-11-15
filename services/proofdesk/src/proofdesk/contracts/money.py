"""Money handling. Never use float for money (see ADR-0007)."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

# Digits after the decimal point for each currency we support.
CURRENCY_EXPONENTS: dict[str, int] = {"AUD": 2, "USD": 2, "VND": 0}


class MoneyError(ValueError):
    """The value cannot be treated as an amount of money."""


def to_money(value: str | int | Decimal, currency: str) -> Decimal:
    """Convert a value to an exact Decimal rounded to the currency's precision."""
    if isinstance(value, bool | float):
        raise MoneyError("float and bool are not accepted for money")
    exponent = CURRENCY_EXPONENTS.get(currency)
    if exponent is None:
        raise MoneyError(f"unsupported currency: {currency}")
    try:
        amount = Decimal(value)
        if not amount.is_finite():
            raise MoneyError("amount must be a finite number")
        return amount.quantize(Decimal(1).scaleb(-exponent), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise MoneyError(f"not a valid amount: {value!r}") from exc
