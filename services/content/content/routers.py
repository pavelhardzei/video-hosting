from content.movies.routers import router as movies_router
from content.serials.routers import router as serials_router
from fastapi import APIRouter

router = APIRouter(
    prefix='/content',
    tags=['content']
)

router.include_router(movies_router)
router.include_router(serials_router)
