from base.database.mixins import SaveDeleteDBMixin
from pydantic import BaseModel


def update(instance: SaveDeleteDBMixin, data: BaseModel):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(instance, key, value)
    instance.save()
