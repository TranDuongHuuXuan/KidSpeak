from datetime import datetime, date
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.schemas.auth_schema import RegisterSchema
from app.utils.password import hash_password

# Default role assigned on registration
ROLE_USER = "USER"


class AuthService:
    """Service handling user authentication logic."""

    # ── Register ──────────────────────────────────────────────────────────────
    @staticmethod
    async def register_user(db: Session, data: RegisterSchema) -> dict:
        """
        Register a new user.

        Steps:
        1. Check if email / username already exists.
        2. Hash the password.
        3. Save the user to the database with the USER role.
           (System roles: USER, ADMIN, EXPERT — expert/teacher)
        4. Return the newly created user's information.
        """
        try:
            # ── 1. Check for duplicate email ──────────────────────────────────
            existing_email = (
                db.query(User)
                .filter(User.email == str(data.email))
                .first()
            )
            if existing_email:
                raise ValueError("Email này đã được đăng ký")

            # ── 1b. Check for duplicate username ──────────────────────────────
            existing_username = (
                db.query(User)
                .filter(User.username == str(data.username))
                .first()
            )
            if existing_username:
                raise ValueError("Tên đăng nhập này đã được sử dụng")

            # ── 2. Hash the password ──────────────────────────────────────────
            hashed_password = hash_password(data.password)

            # ── 3. Get or auto-create the USER role ───────────────────────────
            role = (
                db.query(Role)
                .filter(Role.name == ROLE_USER)
                .first()
            )
            if not role:
                role = Role(
                    name=ROLE_USER,
                    description="Regular user",
                )
                db.add(role)
                db.flush()  # get role.id before commit

            # ── 3b. Parse date of birth ───────────────────────────────────────
            date_of_birth: Optional[datetime] = None
            if data.date_of_birth:
                try:
                    parsed = date.fromisoformat(str(data.date_of_birth))
                    date_of_birth = datetime(parsed.year, parsed.month, parsed.day)
                except ValueError:
                    raise ValueError(
                        "Ngày sinh không hợp lệ, định dạng yêu cầu: YYYY-MM-DD"
                    )

            # ── 3c. Create and persist the User ──────────────────────────────
            now = datetime.utcnow()
            user = User(
                username=str(data.username),
                email=str(data.email),
                password=str(hashed_password),
                role_id=role.id,
                date_of_birth=date_of_birth,
                avatar=None,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            # ── 4. Return created user data ───────────────────────────────────
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role_id": user.role_id,
                "date_of_birth": user.date_of_birth,
                "avatar": user.avatar,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }

        except Exception:
            db.rollback()
            raise
