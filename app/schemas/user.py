from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    nickname: str
    email: EmailStr


class UserOut(BaseModel):
    id: int
    nickname: str
    email: EmailStr

    model_config = {"from_attributes": True}
