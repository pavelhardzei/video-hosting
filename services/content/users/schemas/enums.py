import enum


class LibraryTypeEnum(str, enum.Enum):
    favorite = 'favorite'
    watch_later = 'watch_later'
    watched = 'watched'
    history = 'history'


class UserLibraryObjectEnum(str, enum.Enum):
    movie = 'movie'
    serial = 'serial'
    season = 'season'
    episode = 'episode'
    moment = 'moment'
