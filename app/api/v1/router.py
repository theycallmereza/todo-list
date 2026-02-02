from fastapi import APIRouter

from app.api.v1 import auth, tasks

router = APIRouter()

router.include_router(auth.router)
router.include_router(tasks.router)
