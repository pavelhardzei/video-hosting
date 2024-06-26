# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import authorization_pb2 as authorization__pb2


class AuthorizationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.authorize = channel.unary_unary(
            '/authorization.Authorization/authorize',
            request_serializer=authorization__pb2.AuthorizationRequest.SerializeToString,
            response_deserializer=authorization__pb2.AuthorizationResponse.FromString,
        )


class AuthorizationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def authorize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthorizationServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'authorize': grpc.unary_unary_rpc_method_handler(
            servicer.authorize,
            request_deserializer=authorization__pb2.AuthorizationRequest.FromString,
            response_serializer=authorization__pb2.AuthorizationResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'authorization.Authorization', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class Authorization(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def authorize(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/authorization.Authorization/authorize',
                                             authorization__pb2.AuthorizationRequest.SerializeToString,
                                             authorization__pb2.AuthorizationResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
