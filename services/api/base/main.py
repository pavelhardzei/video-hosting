from auth.routers import router as auth_router
from base.schemas.enums import ErrorCodeEnum
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(auth_router)

app.include_router(router)


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request, e):
    return JSONResponse(status_code=e.status_code,
                        content={'detail': e.detail,
                                 'error_code': e.headers.get('Error-Code', ErrorCodeEnum.base_error)
                                 if e.headers else ErrorCodeEnum.base_error})
