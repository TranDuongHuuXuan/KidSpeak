"""Rename users.username to users.full_name.

Revision ID: b31e7c9a4f20
Revises: 69786eb07024
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b31e7c9a4f20"
down_revision: Union[str, Sequence[str], None] = "69786eb07024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_users_username", table_name="users")
    op.alter_column(
        "users",
        "username",
        new_column_name="full_name",
        existing_type=sa.String(length=100),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "full_name",
        new_column_name="username",
        existing_type=sa.String(length=100),
        existing_nullable=False,
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)
