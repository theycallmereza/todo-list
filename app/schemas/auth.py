from pydantic import BaseModel, EmailStr


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    code: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
