from abc import ABC, abstractmethod
from bisect import bisect_right, bisect_left
from itertools import count


class SegmentedPrimeSieve(ABC):
    """
    An abstract segmented prime sieve. It can compute primes in chunks (segments) and return the so-far-computed primes
    at any time, or do prime finding or counting related operations.
    The values of the primes are stored for the duration of the object, so multiple computations potentially
    requiring further primes to be computed will be accelerated if the object is kept alive.
    The stored primes are guaranteed to be all the primes in the range [2, p_k^2) for some k, referred to as the end segment index.
    """

    @property
    @abstractmethod
    def primes(self):
        """
        A read-only view of the currently computed primes. Do not modify the return value, make a copy first if needed.

        :return: A sequence-like object of primes
        """
        pass

    @abstractmethod
    def _extend(self) -> None:
        """
        Extends the currently computed primes with the primes in the range [p_k^2, p_{k+n}^2) for some n,
        where k is the end segment index.
        Note: the range [p_k^2, p_{k+n}^2) is sieved by [p_0, ..., p_{k+n-1}]
        because if a composite number n has all prime factors >= p_{k+n}, then n >= p_{k+n}^2.
        Precondition: primes contains all primes in the range [2, p_k^2) and no more.
        Postcondition: primes contains all primes in the range [2, p_{k+n}^2)  for some n and no more.
        """
        pass

    def __contains__(self, item) -> bool:
        """
        Returns whether item is prime, computing new primes as necessary in order to check.
        Note: a sieve is not meant to be a primality checker, there are much faster ways to check primality than using a sieve.

        :param item: An int to check whether it is prime.
        :return: Whether item is prime.
        """
        return self.is_prime(item)

    def __len__(self) -> int:
        """
        The number of primes that have been computed and are stored so far.

        :return: The length of the internal storage of primes.
        """
        return len(self.primes)

    def __getitem__(self, item):
        """
        Gets a prime by index starting with p_0 = 2, p_1 = 3, etc.
        Also accepts slices of indices.
        Primes will be computed as necessary.

        :param item: Either an int or slice of indices of primes to get.
        :return: Either the prime at that index or the slice of precomputed primes with the sliced indices.
        """
        if isinstance(item, int):
            return self.nth_prime(item)
        elif isinstance(item, slice):
            self.ensure_len_greater_or_equal(item.stop)
            return self.primes[item]

    def iter_all_primes(self):
        """
        Yield all prime numbers starting at 2. The primes are computed as needed.

        :return A generator yielding all primes:
        """
        for idx in count():
            yield self.nth_prime(idx)

    def is_prime(self, n: int):
        """
        Returns whether n is prime, computing new primes as necessary in order to check.
        Note: a sieve is not meant to be a primality checker, there are much faster ways to check primality than using a sieve.

        :param n: An int to check whether it is prime.
        :return: Whether n is prime.
        """
        return self.next_prime_greater_than(n - 1) == n

    def nth_prime(self, n: int):
        """
        Returns the nth prime number, starting with p_0 = 2, p_1 = 3, etc.
        Primes are computed as necessary.

        :param n: The zero-based index of the prime to compute.
        :return: The nth prime number.
        """
        self.ensure_len_greater_or_equal(n + 1)
        return self.primes[n]

    def primes_in_range(self, n: int, m: int):
        """
        Returns a read-only view of primes in range(n,m), i.e. primes p with n <= p < m.
        Primes are computed as necessary.
        Do not modify the contents of the returned range, make a copy if necessary.

        :param n: The lower bound (inclusive) of primes to compute.
        :param m: The upper bound (exclusive) of primes to compute.
        :return: A read-only sequence of prime p with n <= p < m.
        """
        start = self.index_of_next_prime_greater_than(n - 1)
        end = self.index_of_prev_prime_less_than(m) + 1
        return self.primes[start:end]

    def index_of_next_prime_greater_than(self, n: int) -> int:
        """
        Return the index i of the smallest prime p_i with p_i > n.
        Primes are computed as necessary.

        :param n: An integer.
        :return: the index i for which p_i is the smallest prime with p_i > n.
        """
        self.ensure_max_greater_or_equal(n + 1)
        idx = bisect_right(self.primes, n)
        return idx

    def index_of(self, p: int) -> int:
        """
        Return the index i of a prime p such that p = p_i.

        :return: The index i such that p = p_i
        """
        idx = self.index_of_next_prime_greater_than(p - 1)
        if p != self.primes[idx]:
            raise ValueError("not a prime")
        return idx

    def next_prime_greater_than(self, n: int):
        """
        Return the smallest prime strictly greater than a given number.
        Primes are computed as necessary.

        :param n: An integer.
        :return: The smallest prime p with p > n.
        """
        idx = self.index_of_next_prime_greater_than(n)
        return self.primes[idx]

    def index_of_prev_prime_less_than(self, n: int) -> int:
        """
        Return the index i of the largest prime p_i with p_i < n.
        Primes are computed as necessary.

        :param n: An integer.
        :return: the index i for which p_i is the largest prime with p_i < n.
        """
        if n <= 2:
            raise ValueError
        self.ensure_max_greater_or_equal(n - 1)
        idx = bisect_left(self.primes, n)
        return idx - 1

    def prev_prime_less_than(self, n: int):
        """
        Return the largest prime strictly less than a given number.
        Primes are computed as necessary.

        :param n: An integer.
        :return: The largest prime p with p < n.
        """
        idx = self.index_of_prev_prime_less_than(n)
        return self.primes[idx]

    def count_primes_less_or_equal(self, n: int) -> int:
        """
        Count the number of primes less than or equal to a given bound.
        Primes are computed as necessary.

        :param n: An integer.
        :return: The number of primes less than or equal to n., commonly referred to as pi(n).
        """
        self.ensure_max_greater_or_equal(n)
        return bisect_right(self.primes, n)

    def count_primes_in_range(self, n: int, m: int) -> int:
        """
        Count the number of primes in range(n, m), i.e. the number of primes p with n <= p < m.
        Primes are computed as necessary.

        :param n: The lower bound.
        :param m: The upper bound.
        :return: The number of primes p with n <= p < m.
        """
        start = self.index_of_next_prime_greater_than(n - 1)
        end = self.index_of_prev_prime_less_than(m)
        return max(0, end - start + 1)

    def ensure_len_greater_or_equal(self, n: int) -> None:
        """
        Precompute primes until at least n primes have been computed.
        Afterwards, it is guaranteed than the length of self is at least n.
        Most likely this will cause more than n primes to be computed.

        :param n: The number of primes to ensure are computed.
        :return: None
        """
        while len(self.primes) < n:
            self._extend()

    def ensure_max_greater_or_equal(self, n: int) -> None:
        """
        Precompute primes until the largest computed prime is at least n.
        Afterwards, it is guaranteed that that self.primes[-1] >= n.
        Most likely, afterwards self.primes[-1] > n even if n is prime.

        :param n: An integer.
        :return: None
        """
        while self.primes[-1] < n:
            self._extend()

    def find_primes_until(self, stop_cb, progress_cb=None) -> None:
        """
        Compute more and more primes until a told to stop by the stop callback.

        :param stop_cb: A callable accepting this object as its only argument whose return value's truthiness indicates
         whether to stop computing.
        :param progress_cb: A callable accepting this object as its only argument that will be called for each segment
         of primes computed.
        :return: None
        """
        while not stop_cb(self):
            self._extend()
            if progress_cb is not None:
                progress_cb(self)
