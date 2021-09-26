import logging
from typing import Any, Iterable
import itertools


LOGGER = logging.getLogger()


def compare_iterables(iterable1: Iterable[Any], iterable2: Iterable[Any]) -> bool:
    for x1, x2 in itertools.zip_longest(iterable1, iterable2):
        if x1 is None or x2 is None:
            LOGGER.info(f'Comparing iterables, they are of different length')
            return False
        if x1 != x2:
            LOGGER.info(f'Comparing iterables, different elements found: {x1}, {x2}')
            return False
    return True
