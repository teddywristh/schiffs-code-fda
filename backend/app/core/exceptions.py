from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class CustomAppException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Đã xảy ra lỗi hệ thống."

    def __init__(self, detail: str = None, status_code: int = None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code

class EmailAlreadyExistsException(CustomAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Email này đã tồn tại."

class InvalidLoginException(CustomAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Email hoặc mật khẩu không chính xác."

class UserNotFoundException(CustomAppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Không tìm thấy người dùng này."

class NotDeveloperException(CustomAppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Bạn không có quyền truy cập tài nguyên này."

class DisconnectedDatabaseException(CustomAppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Mất kết nối với Database."

class DisconnectedRedisException(CustomAppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Mất kết nối với Redis."

class OTPExpiredException(CustomAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Mã OTP đã hết hạn hoặc không tồn tại."

class InvalidOTPException(CustomAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Mã OTP không chính xác."

class OTPNotVerifiedException(CustomAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Mã OTP chưa được xác thực hoặc đã hết hạn."

class OTPOverInputException(CustomAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Mã OTP đã nhập vượt quá số lần cho phép. Vui lòng lấy mã mới"

async def global_app_exception_handler(request: Request, exc: CustomAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.__class__.__name__, # Lấy tên Class làm mã lỗi
                "message": exc.detail
            }
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err["loc"])
        errors.append(f"{loc}: {err['msg']}")
    message = "; ".join(errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "ValidationError",
                "message": message
            }
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTPException",
                "message": exc.detail
            }
        }
    )