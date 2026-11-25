"""Normalize system roles to ADMIN=1, STUDENT=2, EXPERT=3.

Revision ID: 9f21c0ab47d1
Revises: 564b10d63991
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "9f21c0ab47d1"
down_revision: Union[str, Sequence[str], None] = "564b10d63991"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ROLE_IDS = {"ADMIN": 1, "STUDENT": 2, "EXPERT": 3}
ROLE_NAMES = {
    "ADMIN": "ADMIN",
    "STUDENT": "STUDENT",
    "USER": "STUDENT",
    "EXPERT": "EXPERT",
}


def upgrade() -> None:
    connection = op.get_bind()
    role_rows = connection.execute(sa.text("SELECT id, name, description FROM roles")).mappings().all()
    role_to_canonical = {}
    descriptions = {}
    for row in role_rows:
        name = str(row["name"]).strip().upper()
        canonical = ROLE_NAMES.get(name)
        if canonical is None:
            raise RuntimeError(f"Cannot normalize unknown role {row['name']!r}; resolve it before upgrading.")
        role_to_canonical[row["id"]] = canonical
        if canonical not in descriptions or name == canonical:
            descriptions[canonical] = row["description"]

    # USER records are merged into STUDENT; seed canonical roles missing from this database.
    permission_rows = connection.execute(
        sa.text("SELECT role_id, permission_id FROM role_permissions")
    ).mappings().all()
    merged_permissions = {
        (ROLE_IDS[role_to_canonical[row["role_id"]]], row["permission_id"])
        for row in permission_rows
        if row["role_id"] in role_to_canonical
    }
    user_rows = connection.execute(sa.text("SELECT id, role_id FROM users")).mappings().all()
    user_role_updates = [
        {"user_id": row["id"], "new_role_id": ROLE_IDS[role_to_canonical[row["role_id"]]]}
        for row in user_rows
        if row["role_id"] is not None and row["role_id"] in role_to_canonical
    ]

    # Remove foreign-key references before rebuilding the three canonical role rows.
    connection.execute(sa.text("DELETE FROM role_permissions"))
    connection.execute(sa.text("UPDATE users SET role_id = NULL WHERE role_id IS NOT NULL"))
    connection.execute(sa.text("DELETE FROM roles"))
    connection.execute(
        sa.text("INSERT INTO roles (id, name, description) VALUES (:id, :name, :description)"),
        [
            {"id": role_id, "name": name, "description": descriptions.get(name)}
            for name, role_id in ROLE_IDS.items()
        ],
    )
    if user_role_updates:
        connection.execute(
            sa.text("UPDATE users SET role_id = :new_role_id WHERE id = :user_id"),
            user_role_updates,
        )
    if merged_permissions:
        connection.execute(
            sa.text("INSERT INTO role_permissions (role_id, permission_id) VALUES (:role_id, :permission_id)"),
            [{"role_id": role_id, "permission_id": permission_id} for role_id, permission_id in sorted(merged_permissions)],
        )

    if connection.dialect.name == "postgresql":
        connection.execute(sa.text(
            "SELECT setval(pg_get_serial_sequence('roles', 'id'), (SELECT MAX(id) FROM roles), true)"
        ))


def downgrade() -> None:
    raise RuntimeError("Role normalization merges USER accounts into STUDENT and cannot be safely reversed.")
