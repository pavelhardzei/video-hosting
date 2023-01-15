from typing import List

from content.schemas.content import PlaylistBaseSchema, PlaylistItemBaseSchema
from content.schemas.enums import PlaylistItemObjectEnum


class PlaylistItemCreateSchema(PlaylistItemBaseSchema):
    object_type: PlaylistItemObjectEnum
    object_id: int


class PlaylistCreateSchema(PlaylistBaseSchema):
    playlist_items: List[PlaylistItemCreateSchema]
