def bound_float(lower: float, upper: float, value: float) -> float:
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value
