def validate_amount(amount):
    try:
        val = float(amount)
        if val <= 0:
            raise ValueError
        return val
    except ValueError:
        raise ValueError("Amount must be a positive number")