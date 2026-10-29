from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Permission(Base):
    """Permission table for system access control."""

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Permission id={self.id} name={self.name!r}>"
