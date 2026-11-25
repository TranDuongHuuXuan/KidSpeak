"""create persistent admin expert messaging

Revision ID: c4a91f7e2d60
Revises: 9f21c0ab47d1
Create Date: 2026-11-25 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "c4a91f7e2d60"
down_revision = "9f21c0ab47d1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admin_expert_conversations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("admin_id", sa.Integer(), nullable=False),
        sa.Column("expert_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["admin_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["expert_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("admin_id", "expert_id", name="uq_admin_expert_conversation_pair"),
    )
    op.create_index("ix_admin_expert_conversations_id", "admin_expert_conversations", ["id"])
    op.create_index("ix_admin_expert_conversations_admin_id", "admin_expert_conversations", ["admin_id"])
    op.create_index("ix_admin_expert_conversations_expert_id", "admin_expert_conversations", ["expert_id"])
    op.create_index("ix_admin_expert_conversations_updated_at", "admin_expert_conversations", ["updated_at"])

    op.create_table(
        "admin_expert_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("recipient_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
        sa.Column("read_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["conversation_id"], ["admin_expert_conversations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["recipient_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_admin_expert_messages_id", "admin_expert_messages", ["id"])
    op.create_index("ix_admin_expert_messages_conversation_id", "admin_expert_messages", ["conversation_id"])
    op.create_index("ix_admin_expert_messages_sender_id", "admin_expert_messages", ["sender_id"])
    op.create_index("ix_admin_expert_messages_recipient_id", "admin_expert_messages", ["recipient_id"])
    op.create_index("ix_admin_expert_messages_sent_at", "admin_expert_messages", ["sent_at"])
    op.create_index("ix_admin_expert_messages_conversation_id_id", "admin_expert_messages", ["conversation_id", "id"])
    op.create_index("ix_admin_expert_messages_recipient_read", "admin_expert_messages", ["recipient_id", "read_at"])


def downgrade() -> None:
    op.drop_index("ix_admin_expert_messages_recipient_read", table_name="admin_expert_messages")
    op.drop_index("ix_admin_expert_messages_conversation_id_id", table_name="admin_expert_messages")
    op.drop_index("ix_admin_expert_messages_sent_at", table_name="admin_expert_messages")
    op.drop_index("ix_admin_expert_messages_recipient_id", table_name="admin_expert_messages")
    op.drop_index("ix_admin_expert_messages_sender_id", table_name="admin_expert_messages")
    op.drop_index("ix_admin_expert_messages_conversation_id", table_name="admin_expert_messages")
    op.drop_index("ix_admin_expert_messages_id", table_name="admin_expert_messages")
    op.drop_table("admin_expert_messages")
    op.drop_index("ix_admin_expert_conversations_updated_at", table_name="admin_expert_conversations")
    op.drop_index("ix_admin_expert_conversations_expert_id", table_name="admin_expert_conversations")
    op.drop_index("ix_admin_expert_conversations_admin_id", table_name="admin_expert_conversations")
    op.drop_index("ix_admin_expert_conversations_id", table_name="admin_expert_conversations")
    op.drop_table("admin_expert_conversations")
