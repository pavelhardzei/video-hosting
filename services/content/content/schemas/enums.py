import enum


class MediaContentTypeEnum(str, enum.Enum):
    movie = 'movie'
    serial = 'serial'
    season = 'season'
    episode = 'episode'
    moment = 'moment'
