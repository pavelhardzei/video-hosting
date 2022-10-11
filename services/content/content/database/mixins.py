from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import declared_attr, relationship


class ContentMixin:
    @declared_attr
    def content_id(cls):
        return Column(Integer, ForeignKey('content.id'))

    @declared_attr
    def content(cls):
        return relationship('Content')


class MediaMixin:
    @declared_attr
    def media_id(cls):
        return Column(Integer, ForeignKey('media.id'))

    @declared_attr
    def media(cls):
        return relationship('Media', lazy='joined')
