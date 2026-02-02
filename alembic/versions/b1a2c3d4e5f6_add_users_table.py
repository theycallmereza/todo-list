"""add users table

Revision ID: b1a2c3d4e5f6
Revises: 43f75db90ec5
Create Date: 2026-02-02 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b1a2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "43f75db90ec5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_users_nickname", "users", ["nickname"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_nickname", table_name="users")
    op.drop_table("users")
