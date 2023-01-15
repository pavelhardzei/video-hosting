import os
from concurrent import futures
from signal import SIGTERM, signal

import grpc
from base.settings import PROJ_DIR, settings
from grpc_module.interceptors import ExceptionIntercepter
from grpc_module.proto.authorization_pb2_grpc import add_AuthorizationServicer_to_server
from grpc_module.service import AuthorizationService


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=3),
        interceptors=(ExceptionIntercepter(), )
    )

    add_AuthorizationServicer_to_server(AuthorizationService(), server)

    with open(os.path.join(PROJ_DIR, 'keys', 'server.key'), 'rb') as fp:
        server_key = fp.read()
    with open(os.path.join(PROJ_DIR, 'keys', 'server.pem'), 'rb') as fp:
        server_cert = fp.read()
    with open(os.path.join(PROJ_DIR, 'keys', 'ca.pem'), 'rb') as fp:
        ca_cert = fp.read()

    creds = grpc.ssl_server_credentials(
        ((server_key, server_cert), ),
        root_certificates=ca_cert,
        require_client_auth=True
    )

    server.add_secure_port(settings.grpc_server, creds)
    server.start()

    def handle_sigterm(*_):
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
    signal(SIGTERM, handle_sigterm)

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
