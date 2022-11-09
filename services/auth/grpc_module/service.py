from auth import utils
from grpc_module.proto.authorization_pb2 import AuthorizationRequest, AuthorizationResponse
from grpc_module.proto.authorization_pb2_grpc import AuthorizationServicer


class AuthorizationServicer(AuthorizationServicer):

    def authorize(self, request: AuthorizationRequest, context) -> AuthorizationResponse:
        payload = utils.decode_access_token(request.access_token)
        response = AuthorizationResponse(id=payload.get('id'))

        return response
