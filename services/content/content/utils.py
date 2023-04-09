from content.database.mixins import ContentMixin
from content.database.models import Content, ContentActors, ContentCountries, ContentDirectors, ContentGenres
from sqlalchemy.orm import Query, contains_eager, selectinload


def prefetch_content_data(query: Query) -> Query:
    model: ContentMixin = query.column_descriptions[0]['entity']
    query = (
        query.join(model.content)
        .outerjoin(ContentCountries).outerjoin(ContentCountries.country)
        .outerjoin(ContentGenres).outerjoin(ContentGenres.genre)
        .outerjoin(ContentActors).outerjoin(ContentActors.actor)
        .outerjoin(ContentDirectors).outerjoin(ContentDirectors.director)
        .options(contains_eager(model.content).options(
            selectinload(Content.countries),
            selectinload(Content.genres),
            selectinload(Content.actors),
            selectinload(Content.directors))
        ).distinct()
    )
    return query
