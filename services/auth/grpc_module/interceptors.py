from base.exceptions import HTTPExceptionWithCode
from grpc_interceptor import ServerInterceptor


class ExceptionIntercepter(ServerInterceptor):
    def intercept(self, method, request_or_iterator, context, *_):
        try:
            return method(request_or_iterator, context)
        except HTTPExceptionWithCode as e:
            context.set_trailing_metadata((
                ('error_code', e.error_code),
                ('status_code', f'{e.status_code}')
            ))
            context.set_details(e.detail)
        except Exception as e:
            context.set_details(f'{e}')
