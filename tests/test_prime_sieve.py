#!/usr/bin/env python

"""Tests for `prime_sieve` package."""

import numpy as np
import pytest
from prime_sieve.array import PrimeArraySieve
from prime_sieve.base import SegmentedPrimeSieve
from prime_sieve.list import PrimeListSieve
from prime_sieve.math_utils import smallest_multiple_of_n_geq_m

first_100_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                    89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
                    181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
                    277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
                    383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479,
                    487, 491, 499, 503, 509, 521, 523, 541]


@pytest.fixture(params=[PrimeArraySieve, PrimeListSieve])
def sieve(request) -> SegmentedPrimeSieve:
    return request.param()


@pytest.mark.parametrize("test_input,expected",
                         [((2, 3), 4),
                          ((3, 2), 3),
                          ((2, 4), 4),
                          ((3, 3), 3),
                          ((3, 6), 6),
                          ((3, 7), 9)])
def test_smallest_multiple_of_n_geq_m(test_input, expected):
    assert smallest_multiple_of_n_geq_m(*test_input) == expected


@pytest.mark.parametrize("test_input,expected", enumerate(first_100_primes))
def test_nth_prime(test_input, expected, sieve):
    """
    See for expected answers:
    https://en.wikipedia.org/wiki/List_of_prime_numbers
    """
    assert sieve.nth_prime(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0, False),
                          (1, False),
                          (2, True),
                          (3, True),
                          (4, False),
                          (5, True),
                          (6, False),
                          (97, True),
                          (100, False),
                          (100 * 200, False),
                          (86 * 97, False),
                          (2 ** 11 - 1, False),
                          (2 ** 13 - 1, True)])
def test_is_prime(test_input, expected, sieve):
    assert sieve.is_prime(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [((0, 5), [2, 3]),
                          ((2, 5), [2, 3]),
                          ((2, 6), [2, 3, 5]),
                          ((10, 50), [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]),
                          ((2, 100), first_100_primes[:25])
                          ])
def test_primes_in_range(test_input, expected, sieve):
    assert list(sieve.primes_in_range(*test_input)) == expected


@pytest.mark.parametrize("test_input,expected",
                         [(p, i + 1) for i, p in enumerate(first_100_primes)] +
                         [(12, 5),
                          (13, 6),
                          (14, 6),
                          (15, 6),
                          (16, 6),
                          (17, 7)])
def test_index_of_next_prime_greater_than(test_input, expected, sieve):
    assert sieve.index_of_next_prime_greater_than(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [(0, 2),
                          (1, 2),
                          (2, 3),
                          (3, 5),
                          (4, 5),
                          (100, 101),
                          (104, 107),
                          (107, 109),
                          (7907, 7919)])
def test_next_prime_greater_than(test_input, expected, sieve):
    assert sieve.next_prime_greater_than(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [(12, 4),
                          (13, 4),
                          (14, 5),
                          (15, 5),
                          (16, 5),
                          (17, 5),
                          (18, 6)])
def test_index_of_prev_prime_less_than(test_input, expected, sieve):
    assert sieve.index_of_prev_prime_less_than(test_input) == expected


def test_index_of_prev_prime_less_than_error(sieve):
    with pytest.raises(ValueError):
        sieve.index_of_prev_prime_less_than(2)


@pytest.mark.parametrize("test_input,expected",
                         [(3, 2),
                          (4, 3),
                          (5, 3),
                          (6, 5),
                          (7, 5),
                          (8, 7),
                          (101, 97),
                          (104, 103),
                          (109, 107),
                          (7907, 7901)])
def test_prev_prime_less_than(test_input, expected, sieve):
    assert sieve.prev_prime_less_than(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [(1, 0),
                          (2, 1),
                          (3, 2),
                          (4, 2),
                          (5, 3),
                          (6, 3),
                          (7, 4),
                          (8, 4),
                          (9, 4),
                          (10, 4),
                          (10 ** 2, 25),
                          (10 ** 3, 168),
                          (10 ** 4, 1229),
                          (10 ** 5, 9592),
                          (10 ** 6, 78498),
                          (10 ** 7, 664579)])
def test_count_primes_less_or_equal(test_input, expected, sieve):
    """
    See for expected answers:
    https://en.wikipedia.org/wiki/Prime-counting_function
    """
    assert sieve.count_primes_less_or_equal(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [((4, 3), 0),
                          ((3, 3), 0),
                          ((2, 3), 1),
                          ((2, 4), 2),
                          ((0, 10), 4),
                          ((2, 10), 4),
                          ((3, 10), 3),
                          ((3, 9), 3),
                          ((3, 8), 3),
                          ((3, 7), 2),
                          ((1, 100), 25), ])
def test_count_primes_in_range(test_input, expected, sieve):
    assert sieve.count_primes_in_range(*test_input) == expected


@pytest.mark.parametrize("test_input", [1, 10, 100, 100])
def test_ensure_len_greater_or_equal(test_input, sieve):
    sieve.ensure_len_greater_or_equal(test_input)
    assert len(sieve) >= test_input


@pytest.mark.parametrize("test_input", [1, 10, 100, 1000])
def test_ensure_max_greater_or_equal(test_input, sieve):
    sieve.ensure_max_greater_or_equal(test_input)
    assert sieve[-1] >= test_input


@pytest.mark.parametrize("dtype", [np.int8, np.uint8, np.int16, np.uint16])
def test_numpy_overflow_error(dtype):
    sieve = PrimeArraySieve(dtype)
    max = np.iinfo(dtype).max
    with pytest.raises(RuntimeError):
        sieve.ensure_max_greater_or_equal(max)
