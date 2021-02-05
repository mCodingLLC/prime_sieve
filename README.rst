===========
Prime Sieve
===========


.. image:: https://img.shields.io/pypi/v/prime_sieve.svg
        :target: https://pypi.python.org/pypi/prime_sieve

.. image:: https://img.shields.io/travis/mCodingLLC/prime_sieve.svg
        :target: https://travis-ci.com/mCodingLLC/prime_sieve

.. image:: https://readthedocs.org/projects/prime-sieve/badge/?version=latest
        :target: https://prime-sieve.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




An understandable prime sieve implementation in numpy or pure python.
The focus is providing a sieve that is easy to understand rather than the absolute fastest implementation.
Though the numpy implementation is reasonably quick,
being able to compute the first 100 million primes in 30 seconds on my mid-tier laptop.

* Free software: MIT license
* Documentation: https://prime-sieve.readthedocs.io.


Usage
-----

.. code-block:: python3

    # Use a numpy or pure python implementation
    from prime_sieve.array import PrimeArraySieve
    # from prime_sieve.list import PrimeListSieve

    sieve = PrimeArraySieve()
    # sieve = PrimeListSieve()

    print(sieve.nth_prime(0)) # 2
    print(sieve[4]) #  7

    print(sieve[:100]) # [2, 3, ..., 541]
    print(sieve[1:6]) # [3, 5, 7, 11, 13]

    print(86*97 in sieve) # False
    print(sieve.is_prime(2 ** 13 - 1)) # True

    # ranges are like python ranges, inclusive start, exclusive stop
    print(sieve.primes_in_range(10, 20)) # [11, 13, 17, 19]
    print(sieve.primes_in_range(10, 19)) # [11, 13, 17]

    print(sieve.count_primes_in_range(3, 7)) # 2
    print(sieve.count_primes_in_range(3, 8)) # 3

    print(sieve.next_prime_greater_than(100)) # 101
    print(sieve.next_prime_greater_than(101)) # 103

    print(sieve.prev_prime_less_than(8)) # 7
    print(sieve.prev_prime_less_than(7)) # 5

    print(sieve.count_primes_less_or_equal(10 ** 7)) # 664579

    for p in sieve.iter_all_primes(): # infinite loop
        print(p)

    # see sieve internals
    print(len(sieve)) # how many primes have currently been computed
    print(sieve.primes) # read-only view of already computed primes

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
