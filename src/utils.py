"""
utils.py
Created by dturba at 30/06/2020
"""
from typing import Iterable, Callable, Any


def clear_instances(cls):
    cls._instances = \
        {key: ref for key, ref in cls._instances.items() if ref()}


def first(array: Iterable, predicate: Callable) -> Any:
    """Generic tool, not bind to the logic"""
    for elem in array:
        if predicate(elem):
            return elem
