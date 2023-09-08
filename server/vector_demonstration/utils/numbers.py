from decimal import ROUND_DOWN, Decimal


def round_decimal(value, quantize=".01"):
    """"""
    if value is not None:
        return Decimal(value).quantize(Decimal(quantize), rounding=ROUND_DOWN)
