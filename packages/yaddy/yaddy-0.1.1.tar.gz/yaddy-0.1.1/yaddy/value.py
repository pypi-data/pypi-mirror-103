"""
This module describes Value class.
"""
from typing import Any

from .domain_object import DomainObject


class Value(DomainObject):
    """
    Value class for DDD.

    Value should be immutable, values are compared by... well, value.
    There are no special identifiers as in Entity.
    """

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        for variable in self.fields:
            if getattr(self, variable) != getattr(other, variable):
                return False
        return True
