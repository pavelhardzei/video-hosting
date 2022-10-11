from pydantic import BaseModel, validator
from sqlalchemy.orm import Query


class OrmBaseMixin(BaseModel):
    @validator('*', pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True


class FlattenMixin(BaseModel):
    def _iter(self, to_dict: bool = False, *args, **kwargs):
        for dict_key, v in super()._iter(to_dict, *args, **kwargs):
            if to_dict and self.__fields__[dict_key].field_info.extra.get('flatten', False):
                yield from v.items()
            else:
                yield dict_key, v
