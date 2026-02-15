"""gRPC interceptors for logging and error handling."""
import grpc
import structlog
from grpc.aio import ServerInterceptor

from app.common.errors import BookingError, HotelValidationError, UserValidationError

logger = structlog.get_logger()


class LoggingInterceptor(ServerInterceptor):
    """Interceptor for logging gRPC requests."""

    async def intercept_service(self, continuation, handler_call_details):
        """Intercept and log gRPC calls."""
        method = handler_call_details.method
        logger.info("grpc_request_started", method=method)

        try:
            response = await continuation(handler_call_details)
            logger.info("grpc_request_completed", method=method)
            return response
        except Exception as e:
            logger.error("grpc_request_failed", method=method, error=str(e))
            raise


class ErrorMappingInterceptor(ServerInterceptor):
    """Interceptor for mapping domain errors to gRPC errors."""

    async def intercept_service(self, continuation, handler_call_details):
        """Intercept and map domain errors to gRPC errors."""
        try:
            return await continuation(handler_call_details)
        except UserValidationError as e:
            logger.warning("user_validation_error", error=str(e))
            raise grpc.aio.AioRpcError(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                initial_metadata=grpc.aio.Metadata(),
                trailing_metadata=grpc.aio.Metadata(),
                details=str(e),
            )
        except HotelValidationError as e:
            logger.warning("hotel_validation_error", error=str(e))
            raise grpc.aio.AioRpcError(
                code=grpc.StatusCode.INVALID_ARGUMENT,
                initial_metadata=grpc.aio.Metadata(),
                trailing_metadata=grpc.aio.Metadata(),
                details=str(e),
            )
        except BookingError as e:
            logger.error("booking_error", error=str(e))
            raise grpc.aio.AioRpcError(
                code=grpc.StatusCode.INTERNAL,
                initial_metadata=grpc.aio.Metadata(),
                trailing_metadata=grpc.aio.Metadata(),
                details=str(e),
            )
        except Exception as e:
            logger.error("unexpected_error", error=str(e), exc_info=True)
            raise grpc.aio.AioRpcError(
                code=grpc.StatusCode.INTERNAL,
                initial_metadata=grpc.aio.Metadata(),
                trailing_metadata=grpc.aio.Metadata(),
                details="Internal server error",
            )
