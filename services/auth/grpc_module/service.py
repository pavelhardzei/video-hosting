from auth import utils
from auth.database.models import UserProfile
from auth.permissions import UserAccessTokenValid, UserActive
from base.database.config import SessionLocal
from base.permissions import check_permissions
from grpc_module.proto.authorization_pb2 import AuthorizationRequest, AuthorizationResponse
from grpc_module.proto.authorization_pb2_grpc import AuthorizationServicer


class AuthorizationService(AuthorizationServicer):

    def authorize(self, request: AuthorizationRequest, context) -> AuthorizationResponse:
        payload = utils.decode_access_token(request.access_token)

        user = SessionLocal.get(UserProfile, payload.get('id'))
        check_permissions(user, (UserActive(), UserAccessTokenValid(request.access_token)))

        response = AuthorizationResponse(id=user.id, role=user.role)

        return response
