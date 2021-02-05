import numpy as np

from prime_sieve.base import SegmentedPrimeSieve
from prime_sieve.math_utils import smallest_multiple_of_n_geq_m


class PrimeArraySieve(SegmentedPrimeSieve):
    """
    A numpy array implementation of a segmented prime sieve.
    It is relatively fast, but subject to possible overflow if you are working with very many primes.
    """

    def __init__(self, dtype=np.uint64):
        self._primes: np.ndarray = np.array([2, 3, 5, 7], dtype=dtype)
        self.end_segment: int = 1
        self.dtype = dtype
        self.dtype_max = np.iinfo(dtype).max
        self.extend_at_most_n_segments_target: int = 100

    @property
    def primes(self):
        return self._primes

    def _extend_at_most_n_segments(self, n: int) -> None:
        k = self.end_segment
        n = min(n, len(self._primes) - 1 - k)
        p, q = int(self._primes[k]), int(self._primes[k + n])
        segment_min, segment_max = p * p, q * q - 1
        if segment_max > self.dtype_max:
            raise RuntimeError("overflow, use a larger dtype or pure python implementation")

        segment_len = segment_max - segment_min + 1
        is_prime = np.full(shape=segment_len, fill_value=True, dtype=bool)

        for pk in self._primes[:k + n]:
            pk = int(pk)
            start = smallest_multiple_of_n_geq_m(pk, segment_min)
            is_prime[start - segment_min::pk] = False

        segment = np.arange(p * p, q * q, dtype=self.dtype)
        new_primes = segment[is_prime]
        try:
            old_len = len(self._primes)
            self._primes.resize(old_len + len(new_primes))
            self._primes[old_len:] = new_primes
        except ValueError:
            self._primes = np.concatenate((self._primes, new_primes))

        self.end_segment += n

    def _extend(self) -> None:
        self._extend_at_most_n_segments(self.extend_at_most_n_segments_target)
