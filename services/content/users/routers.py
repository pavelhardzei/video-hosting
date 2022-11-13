from base.database import crud
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from users.database.models import UserLibrary
from users.dependences import current_user_id
from users.schemas import schemas

router = APIRouter(
    prefix='/users/me',
    tags=['users']
)


@router.get('/library/', response_model=schemas.UserLibraryListSchema)
def get_library(user_id: int = Depends(current_user_id), session: Session = Depends(session_dependency)):
    library = session.query(UserLibrary).filter(UserLibrary.user_id == user_id).all()

    return library


@router.post('/library/', response_model=schemas.UserLibrarySchema, status_code=status.HTTP_201_CREATED)
def post_library(data: schemas.UserLibraryCreateSchema, user_id: int = Depends(current_user_id)):
    user_library = UserLibrary(**data.dict())
    user_library.user_id = user_id
    user_library.save()

    return user_library


@router.patch('/library/{id}/', response_model=schemas.UserLibrarySchema)
def patch_library(
    id: int,
    data: schemas.UserLibraryUpdateSchema,
    user_id: int = Depends(current_user_id),
    session: Session = Depends(session_dependency)
):
    user_library = session.query(UserLibrary).filter(UserLibrary.id == id, UserLibrary.user_id == user_id).first()
    check_permissions(user_library, [])

    crud.update(user_library, data)

    return user_library


@router.delete('/library/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_library(id: int, user_id: int = Depends(current_user_id), session: Session = Depends(session_dependency)):
    user_library = session.query(UserLibrary).filter(UserLibrary.id == id, UserLibrary.user_id == user_id).first()
    check_permissions(user_library, [])

    user_library.delete()

    return None
