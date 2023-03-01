from auth.routers import router as auth_router
from auth.users.routers import router as users_router
from base.database.dependencies import session_commit_hook
from base.exceptions import HTTPExceptionWithCode
from base.schemas.enums import ErrorCodeEnum
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

origins = [
    'https://darktheater-app.web.app',
    'https://darktheater-app.firebaseapp.com',
    'https://darktheater.net',
    'https://docs.darktheater.net',
    'https://darktheater.vercel.app/',
    'http://localhost:4200',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

router = APIRouter(
    prefix='/api/v1',
    dependencies=[Depends(session_commit_hook)]
)

router.include_router(auth_router)
router.include_router(users_router)

app.include_router(router)


@app.exception_handler(HTTPExceptionWithCode)
def http_exception_handler(request: Request, e: HTTPExceptionWithCode):
    return JSONResponse(status_code=e.status_code,
                        content={'detail': e.detail, 'error_code': e.error_code},
                        headers=e.headers)


@app.exception_handler(StarletteHTTPException)
def http_default_exception_handler(request: Request, e: StarletteHTTPException):
    return JSONResponse(status_code=e.status_code,
                        content={'detail': e.detail, 'error_code': ErrorCodeEnum.base_error},
                        headers=e.headers)
