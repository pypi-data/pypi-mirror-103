
__all__ = ["modable"]


def modable(n, v):
    """If n can be modulo by v"""
    if n % v:
        return True
    else:
        return False
