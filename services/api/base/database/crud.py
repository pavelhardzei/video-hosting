from base.database.mixins import SaveDeleteDBMixin
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError


def update(instance: SaveDeleteDBMixin, data: BaseModel):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(instance, key, value)
    try:
        instance.save()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{e.orig}')
