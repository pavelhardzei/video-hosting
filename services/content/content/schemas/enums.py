import enum


class MediaContentTypeEnum(str, enum.Enum):
    movie = 'movie'
    serial = 'serial'
    season = 'season'
    episode = 'episode'
    moment = 'moment'


class PlaylistItemObjectEnum(str, enum.Enum):
    movie = 'Movie'
    serial = 'Serial'


class PlaylistTypeEnum(str, enum.Enum):
    cards = 'cards'
    highlights = 'highlights'
