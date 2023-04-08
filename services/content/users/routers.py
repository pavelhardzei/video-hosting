from base.database import crud
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.utils.dependences import current_user_data
from base.utils.pagination import Params, paginate
from content.database.models import Episode, Movie, Season, Serial
from dark_utils.sqlalchemy_utils import attach_relationships
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, joinedload
from users.database.models import UserLibrary
from users.schemas import schemas
from users.schemas.enums import LibraryTypeEnum

router = APIRouter(
    prefix='/users/me',
    tags=['users']
)


@router.get('/library/{library_type}/', response_model=schemas.UserLibraryListSchema)
def get_library(
    library_type: LibraryTypeEnum,
    params: Params = Depends(),
    user_data: dict = Depends(current_user_data),
    session: Session = Depends(session_dependency)
):
    attach_relationships(UserLibrary, [Movie, Serial, Season, Episode])

    library = session.query(UserLibrary).options(
        joinedload(UserLibrary._object_movie),
        joinedload(UserLibrary._object_serial),
        joinedload(UserLibrary._object_season),
        joinedload(UserLibrary._object_episode)
    ).filter(
        UserLibrary.user_id == user_data['id'],
        UserLibrary.library_type == library_type
    ).order_by(UserLibrary.id)

    return paginate(library, params)


@router.post('/library/', response_model=schemas.UserLibrarySchema, status_code=status.HTTP_201_CREATED)
def post_library(data: schemas.UserLibraryCreateSchema, user_data: dict = Depends(current_user_data)):
    user_library = UserLibrary(**data.dict(), user_id=user_data['id'])
    user_library.save()

    return user_library


@router.patch('/library/{id}/', response_model=schemas.UserLibrarySchema)
def patch_library(
    id: int,
    data: schemas.UserLibraryUpdateSchema,
    user_data: dict = Depends(current_user_data),
    session: Session = Depends(session_dependency)
):
    user_library = session.query(UserLibrary).filter(
        UserLibrary.id == id, UserLibrary.user_id == user_data['id']).first()
    check_permissions(user_library, [])

    crud.update(user_library, data)

    return user_library


@router.delete('/library/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_library(id: int, user_data: dict = Depends(current_user_data),
                   session: Session = Depends(session_dependency)):
    user_library = session.query(UserLibrary).filter(
        UserLibrary.id == id, UserLibrary.user_id == user_data['id']).first()
    check_permissions(user_library, [])

    user_library.delete()

    return None
