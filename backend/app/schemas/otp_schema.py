from pydantic import BaseModel

class MsgResponse(BaseModel):
    status: str = "success"
    message: str

class OTPVerifyResponse(BaseModel):
    status: str = "success"
    message: str
    verified_token: str
