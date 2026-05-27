#!/usr/bin/python3

"""Module that calculate the minimum number of operation
needed to result in exacly n H character"""


def minOperations(n):
    """return the min number of operations
    Args:
        n (int): target number H
    Returns:
            int: min number
    """
    if n <= 1:
        return 0

    operations = 0
    facteur = 2

    while n > 1:
        while n % facteur == 0:
            operations += facteur
            n //= facteur
        facteur += 1
    return operations
