def smallest_multiple_of_n_geq_m(n: int, m: int) -> int:
    """
    Returns the smallest multiple of n greater than or equal to m.

    :param n: A strictly positive integer.
    :param m: A non-negative integer.
    :return: The smallest multiple of n that is greater or equal to m.
    """
    return m + ((n - (m % n)) % n)
