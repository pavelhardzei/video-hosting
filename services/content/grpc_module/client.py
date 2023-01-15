import os

import grpc
from base.settings import PROJ_DIR, settings
from grpc_module.proto.authorization_pb2 import AuthorizationRequest
from grpc_module.proto.authorization_pb2_grpc import AuthorizationStub
from grpc_module.utils import handle_response


def authorize(access_token: str) -> dict:
    with open(os.path.join(PROJ_DIR, 'keys', 'client.key'), 'rb') as fp:
        client_key = fp.read()
    with open(os.path.join(PROJ_DIR, 'keys', 'client.pem'), 'rb') as fp:
        client_cert = fp.read()
    with open(os.path.join(PROJ_DIR, 'keys', 'ca.pem'), 'rb') as fp:
        ca_cert = fp.read()
    creds = grpc.ssl_channel_credentials(ca_cert, client_key, client_cert)

    with grpc.secure_channel(settings.grpc_server, creds) as channel:
        stub = AuthorizationStub(channel)
        request = AuthorizationRequest(access_token=access_token)
        response = handle_response(stub.authorize, request)

    return {'id': response.id, 'role': response.role}
