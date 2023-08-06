"""
Yet Another Domain (Driven) Development librarY.

This module encapsulates all the public interfaces for
yaddy.
"""

from .entity import Entity
from .value import Value

__version__ = "0.1.0"

__all__ = [
    "Entity",
    "Value",
]
