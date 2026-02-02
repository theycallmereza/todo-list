from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    estimated_completion_time: Mapped[DateTime | None] = mapped_column(
        DateTime, nullable=True
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="tasks")
