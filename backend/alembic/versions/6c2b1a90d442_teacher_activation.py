"""add teacher activation timestamp

Revision ID: 6c2b1a90d442
Revises: 2a31585ac471
"""
from alembic import op
import sqlalchemy as sa

revision = "6c2b1a90d442"
down_revision = "2a31585ac471"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("expert_upgrade_requests", sa.Column("activated_at", sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column("expert_upgrade_requests", "activated_at")
