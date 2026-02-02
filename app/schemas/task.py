from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserOut


class TaskIn(BaseModel):
    title: str
    estimated_completion_time: datetime | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    estimated_completion_time: datetime | None = None
    user: UserOut | None = None

    model_config = {"from_attributes": True}
