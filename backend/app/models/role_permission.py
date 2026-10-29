from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class RolePermission(Base):
    """Junction table linking roles and permissions."""

    __tablename__ = "role_permissions"

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id = Column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")

    def __repr__(self) -> str:
        return f"<RolePermission role={self.role_id} permission={self.permission_id}>"
