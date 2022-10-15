from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from base.utils.pagination import Params, paginate
from content.database.models import Serial
from content.schemas.content import SerialListSchema, SerialSchema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/serials'
)


@router.get('/', response_model=SerialListSchema)
def serials(params: Params = Depends(), session: Session = Depends(session_dependency)):
    serials = session.query(Serial).order_by(Serial.id)

    return paginate(serials, params)


@router.get('/{id}/', response_model=SerialSchema,
            responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}})
def serial(id: int, session: Session = Depends(session_dependency)):
    serial = session.query(Serial).filter(Serial.id == id).first()
    check_permissions(serial, [])

    return serial
