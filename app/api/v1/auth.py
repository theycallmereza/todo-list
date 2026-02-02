import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.models.user import User
from app.schemas.auth import OTPRequest, OTPVerify, Token
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

settings = get_settings()


@router.post("/request-otp")
async def request_otp(
    data: OTPRequest,
    db: AsyncSession = Depends(get_db),
):
    """Request a one-time password (OTP) for login via email.

    If user exists, uses that user. If not, creates a new user.
    In a real app, you'd send the OTP via email/SMS.
    Here we return it in the response for demo purposes.
    """

    # Try to find existing user
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    user_created = False
    if user is None:
        # Create a new user with a simple nickname derived from email
        nickname = data.email.split("@", 1)[0]
        user = User(nickname=nickname, email=data.email)
        db.add(user)
        await db.flush()  # assign id
        user_created = True

    # Generate 6-digit OTP
    otp = f"{secrets.randbelow(10**6):06d}"
    # Use naive UTC datetimes for consistency with SQLite storage
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

    user.otp_code = otp
    user.otp_expires_at = expires_at

    await db.commit()
    await db.refresh(user)

    # In production, DO NOT return the OTP – send via email instead.
    return {
        "detail": "OTP generated (in real apps, this would be emailed).",
        "user": UserOut.model_validate(user),
        "user_created": user_created,
        "otp": otp,
        "expires_at": expires_at.isoformat(),
    }


@router.post("/login-otp", response_model=Token)
async def login_with_otp(
    data: OTPVerify,
    db: AsyncSession = Depends(get_db),
):
    """Verify an OTP and return a JWT access token."""

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found for this email.",
        )

    if not user.otp_code or not user.otp_expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active OTP for this user. Request a new one.",
        )

    if user.otp_code != data.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code.",
        )

    # Compare using naive UTC datetimes
    if user.otp_expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Request a new one.",
        )

    # OTP is valid – clear it and issue JWT
    user.otp_code = None
    user.otp_expires_at = None
    await db.commit()

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(get_current_user)) -> UserOut:
    """Return the currently authenticated user's public profile."""

    return UserOut.model_validate(current_user)
