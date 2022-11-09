from fastapi import APIRouter
from grpc_module.client import authorize

router = APIRouter(
    prefix='/users/me',
    tags=['content']
)


@router.post('/')
def health():
    pk = authorize('health')

    return {'pk': pk}
