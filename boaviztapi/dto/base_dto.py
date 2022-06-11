from typing import Union
from uuid import UUID, uuid4

from pydantic import BaseModel


class BaseDTO(BaseModel):
    """
    BaseDTO is simple BaseModel object with an extra field `_id` that is not included by default in object dumps.
    The field `__id` is invisible for the end user, but it can be dumped using `.dict(include_id=True)` method.
    """
    __slots__ = ('__id',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '__id', uuid4())

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        include_id: bool = False
    ) -> 'DictStrAny':
        res = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if include_id:
            res['__id'] = self.__id
        return res
