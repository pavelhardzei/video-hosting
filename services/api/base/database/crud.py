from base.database.mixins import BaseDBMixin
from pydantic import BaseModel


def update(instance: BaseDBMixin, data: BaseModel):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(instance, key, value)
    instance.save()
