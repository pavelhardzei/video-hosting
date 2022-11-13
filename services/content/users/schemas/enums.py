import enum


class LibraryTypeEnum(str, enum.Enum):
    favorite = 'favorite'
    watch_later = 'watch_later'
    watched = 'watched'
    history = 'history'


class ObjectTypeEnum(str, enum.Enum):
    movie = 'Movie'
    serial = 'Serial'
    season = 'Season'
    episode = 'Episode'
    moment = 'Moment'
