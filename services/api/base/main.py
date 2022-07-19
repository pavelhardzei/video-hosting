from auth.routers import router as auth_router
from fastapi import APIRouter, FastAPI

app = FastAPI()

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(auth_router)

app.include_router(router)
