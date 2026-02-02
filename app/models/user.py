from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.task import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # OTP login fields
    otp_code: Mapped[str | None] = mapped_column(String(6), nullable=True)
    otp_expires_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    # Relationship
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
