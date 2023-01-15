from admin.content.routers import playlists_router
from fastapi import APIRouter

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

router.include_router(playlists_router)
