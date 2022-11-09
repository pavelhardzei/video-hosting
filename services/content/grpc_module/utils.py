import grpc
from base.exceptions import HTTPExceptionWithCode
from base.schemas.enums import ErrorCodeEnum
from fastapi import status


def handle_response(method, request):
    try:
        response = method(request)
    except grpc.RpcError as e:
        metadata = dict(e.trailing_metadata())

        detail = e.details()
        error_code = metadata.get('error_code', ErrorCodeEnum.base_error)
        status_code = int(metadata.get('status_code', status.HTTP_400_BAD_REQUEST))

        raise HTTPExceptionWithCode(
            status_code=status_code,
            error_code=error_code,
            detail=detail
        )

    return response
