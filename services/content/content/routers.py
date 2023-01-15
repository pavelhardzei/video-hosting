from content.content.routers import movies_router, playlists_router, serials_router
from fastapi import APIRouter

router = APIRouter(
    prefix='/content',
    tags=['content']
)

router.include_router(movies_router)
router.include_router(playlists_router)
router.include_router(serials_router)
