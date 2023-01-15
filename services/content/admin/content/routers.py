from admin.permissions import AdminUser
from admin.schemas.schemas import PlaylistCreateSchema
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.utils.dependences import current_user_data
from content.database.models import Playlist, PlaylistItem
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

playlists_router = APIRouter(
    prefix='/playlists'
)


@playlists_router.post('/', status_code=status.HTTP_201_CREATED)
def post_playlist(data: PlaylistCreateSchema, user_data: dict = Depends(current_user_data)):
    check_permissions(user_data, (AdminUser(), ))

    playlist = Playlist(
        **data.dict(exclude={'playlist_items'}),
        playlist_items=[PlaylistItem(**item.dict()) for item in data.playlist_items]
    )
    playlist.save()

    return None


@playlists_router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    id: int,
    user_data: dict = Depends(current_user_data),
    session: Session = Depends(session_dependency)
):
    check_permissions(user_data, (AdminUser(), ))

    playlist = session.query(Playlist).filter(Playlist.id == id).first()
    check_permissions(playlist, [])

    playlist.delete()

    return None
