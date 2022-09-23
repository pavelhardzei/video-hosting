from fastapi import APIRouter

router = APIRouter(
    prefix='/content',
    tags=['content']
)


@router.get('/health/')
def health():
    return {'health': 'ok'}
