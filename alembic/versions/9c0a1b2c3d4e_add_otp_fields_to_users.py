"""add otp fields to users

Revision ID: 9c0a1b2c3d4e
Revises: 72bd1ea036be
Create Date: 2026-02-02 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9c0a1b2c3d4e"
down_revision: Union[str, Sequence[str], None] = "72bd1ea036be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("otp_code", sa.String(length=6), nullable=True))
    op.add_column("users", sa.Column("otp_expires_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "otp_expires_at")
    op.drop_column("users", "otp_code")
