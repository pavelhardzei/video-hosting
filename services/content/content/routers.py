from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from base.utils.pagination import Params, paginate
from content.database.models import Movie
from content.schemas.content import MovieListSchema, MovieSchema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, joinedload

router = APIRouter(
    prefix='/content',
    tags=['content']
)


@router.get('/movies/', response_model=MovieListSchema)
def movies(params: Params = Depends(), session: Session = Depends(session_dependency)):
    movies = session.query(Movie).options(joinedload(Movie.content)).order_by(Movie.id)

    return paginate(movies, params)


@router.get('/movies/{id}/', response_model=MovieSchema,
            responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}})
def movie(id: int, session: Session = Depends(session_dependency)):
    movie = session.query(Movie).options(joinedload(Movie.content)).filter(Movie.id == id).first()
    check_permissions(movie, [])

    return movie
