from decimal import Decimal, ROUND_HALF_UP


def decimal_round(num: float) -> float:
    return float(Decimal(num).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
