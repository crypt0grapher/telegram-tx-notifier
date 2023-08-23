def safe_bignumber_to_float(value):
    try:
        return float(value) / 10 ** 18
    except ValueError:
        return 0.0
