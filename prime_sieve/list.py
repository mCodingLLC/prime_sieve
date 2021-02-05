from itertools import repeat

from prime_sieve.base import SegmentedPrimeSieve
from prime_sieve.math_utils import smallest_multiple_of_n_geq_m


class PrimeListSieve(SegmentedPrimeSieve):
    """
    A pure Python implementation of a segmented prime sieve.
    It is much slower than the numpy implementation, but has no dependencies and no possibility of overflow.
    """

    def __init__(self):
        self._primes: list[int] = [2, 3, 5, 7]
        self.end_segment: int = 1
        self.extend_at_most_n_segments_target: int = 10

    @property
    def primes(self):
        return self._primes

    def _extend_at_most_n_segments(self, n: int) -> None:
        k = self.end_segment
        n = min(n, len(self._primes) - 1 - k)
        p, q = self._primes[k], self._primes[k + n]
        segment = range(p * p, q * q)
        segment_min = min(segment)
        segment_len = len(segment)
        is_prime = [True] * segment_len

        for i in range(k + n):
            pk = self._primes[i]
            start = smallest_multiple_of_n_geq_m(pk, segment_min)
            is_prime[start - segment_min::pk] = repeat(False, len(range(start - segment_min, segment_len, pk)))

        self._primes.extend([x for x, it_is_prime in zip(segment, is_prime) if it_is_prime])
        self.end_segment += n

    def _extend(self) -> None:
        self._extend_at_most_n_segments(self.extend_at_most_n_segments_target)
