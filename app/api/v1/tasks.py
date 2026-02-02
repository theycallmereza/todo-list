from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskIn, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])


async def auto_complete_expired_tasks(user_id: int, db: AsyncSession) -> None:
    """Auto-complete tasks that have passed their estimated completion time."""
    now = datetime.utcnow()
    result = await db.execute(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,  # noqa: E712
            Task.estimated_completion_time.isnot(None),
            Task.estimated_completion_time < now,
        )
    )
    expired_tasks = result.scalars().all()

    for task in expired_tasks:
        task.completed = True

    if expired_tasks:
        await db.commit()


@router.get("/", response_model=list[TaskOut])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all tasks for the authenticated user."""
    # Auto-complete expired tasks before fetching
    await auto_complete_expired_tasks(current_user.id, db)

    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .options(selectinload(Task.user))
    )
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single task by ID (only if it belongs to the authenticated user)."""
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id, Task.user_id == current_user.id)
        .options(selectinload(Task.user))
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    # Auto-complete if expired
    if (
        not task.completed
        and task.estimated_completion_time
        and task.estimated_completion_time < datetime.utcnow()
    ):
        task.completed = True
        await db.commit()
        await db.refresh(task)

    return task


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new task for the authenticated user."""
    todo = Task(
        title=data.title,
        user_id=current_user.id,
        estimated_completion_time=data.estimated_completion_time,
    )
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    # Load user relationship for response
    await db.refresh(todo, ["user"])
    return todo
