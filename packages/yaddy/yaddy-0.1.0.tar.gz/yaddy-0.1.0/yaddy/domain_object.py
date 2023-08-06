"""
This module describes DomainObject class.
"""
from typing import Any, Dict, Iterable


class DomainObject:
    """
    DomainObject is any object that could be represented in domain.

    This class implements common behaviour for values and entities
    and should not be subclassed directly.
    """

    def __init__(
        self,
        **kwargs: Any,
    ):
        for field, value in kwargs.items():
            setattr(self, field, value)

    @property
    def fields(self) -> Iterable[str]:
        """Return fields for current object"""
        try:
            fields = self.__annotations__.keys()  # pylint: disable=no-member
        except AttributeError:
            return []
        return fields

    def asdict(self) -> Dict[str, Any]:
        """Return dictionary serialization for Domain object"""
        fields = self.fields
        res = {}
        for field in fields:
            value = getattr(self, field)
            if isinstance(value, DomainObject):
                value = value.asdict()
            res[field] = value
        return res

    def __repr__(self) -> str:
        fields = self.fields
        values = ((field, getattr(self, field)) for field in fields)
        parameters = (f"{field}={value!r}" for field, value in values)

        return f"{self.__class__.__name__}({', '.join(parameters)})"
