"""
utils.py
Created by dturba at 30/06/2020
"""


def clear_instances(cls):
    cls._instances = \
        {key: ref for key, ref in cls._instances.items() if ref()}
