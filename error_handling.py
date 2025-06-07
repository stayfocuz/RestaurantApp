def is_positive_integer(value):
    """
    Returns True if value is a string representing a positive integer (>=1), else False.
    """
    try:
        num = int(value)
        return num >= 1
    except (ValueError, TypeError):
        return False

def is_non_negative_integer(value):
    """
    Returns True if value is a string representing a non-negative integer (>=0), else False.
    """
    try:
        num = int(value)
        return num >= 0
    except (ValueError, TypeError):
        return False