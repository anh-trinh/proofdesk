"""Money handling. Never use float for money (see ADR-0007)."""

from decimal import ROUND_HALF_UP, Context, Decimal, InvalidOperation, localcontext

# Digits after the decimal point for each currency we support.
CURRENCY_EXPONENTS: dict[str, int] = {"AUD": 2, "USD": 2, "VND": 0}

# Largest absolute amount we accept, in major units. Far above any real invoice.
MAX_AMOUNT = Decimal("1e15")

# Fixed context, so results never depend on the caller's decimal settings.
_MONEY_CONTEXT = Context(prec=34, rounding=ROUND_HALF_UP)


class MoneyError(ValueError):
    """The value cannot be treated as an amount of money.

    The message is a stable code and never contains the input value.
    """


def to_money(value: str | int | Decimal, currency: str) -> Decimal:
    """Convert a value to an exact Decimal rounded to the currency's precision."""
    if isinstance(value, bool | float):
        raise MoneyError("float_not_allowed")
    exponent = CURRENCY_EXPONENTS.get(currency)
    if exponent is None:
        raise MoneyError("unsupported_currency")
    with localcontext(_MONEY_CONTEXT):
        try:
            amount = Decimal(value)
        except InvalidOperation as exc:
            raise MoneyError("invalid_amount") from exc
        if not amount.is_finite():
            raise MoneyError("non_finite_amount")
        if abs(amount) > MAX_AMOUNT:
            raise MoneyError("amount_too_large")
        return amount.quantize(Decimal(1).scaleb(-exponent))
