from datetime import datetime
from typing import List, Optional, Union

from base.mixins.schemas import OrmBaseMixin
from content.schemas.content import (EpisodeTruncatedSchema, MovieTruncatedSchema, SeasonTruncatedSchema,
                                     SerialTruncatedSchema)
from pydantic import BaseModel
from users.schemas.enums import LibraryTypeEnum, UserLibraryObjectEnum


class UserLibraryBaseSchema(BaseModel):
    library_type: LibraryTypeEnum
    offset: Optional[int] = None


class UserLibraryCreateSchema(UserLibraryBaseSchema):
    object_type: UserLibraryObjectEnum
    object_id: int


class UserLibrarySchema(OrmBaseMixin, UserLibraryBaseSchema):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    object: Union[EpisodeTruncatedSchema, MovieTruncatedSchema, SerialTruncatedSchema, SeasonTruncatedSchema]


class UserLibraryListSchema(BaseModel):
    __root__: List[UserLibrarySchema]


class UserLibraryUpdateSchema(BaseModel):
    offset: Optional[int] = None
