from datetime import datetime

from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.core.security import normalize_role_name
from app.schemas.auth_schema import RegisterSchema,LoginSchema, LoginResponseSchema
from app.utils.password import hash_password
from app.utils.auth import generate_token
from app.utils.password import verify_password
from app.schemas.user_schema import UserSchema
from app.core.roles import STUDENT_ROLE_ID, STUDENT_ROLE_NAME


class RegistrationConflictError(ValueError):
    """Raised when registration conflicts with an existing user."""


class InvalidCredentialsError(Exception):
    """Raised when an email/password pair cannot be authenticated."""


class InactiveAccountError(Exception):
    """Raised when an account has no supported role."""


class AccountDisabledError(Exception):
    """Raised when valid credentials belong to a disabled account."""


class AuthService:
    """Service handling user authentication logic."""

    # ── Register ──────────────────────────────────────────────────────────────
    @staticmethod
    async def register_user(db: Session, data: RegisterSchema) -> dict:
        """
        Register a new user.

        Steps:
        1. Check if email already exists.
        2. Hash the password.
        3. Save the user to the database with the STUDENT role.
           (System roles: ADMIN, STUDENT, EXPERT — expert/teacher)
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
                raise RegistrationConflictError("Email này đã được đăng ký.")

            # ── 2. Hash the password ──────────────────────────────────────────
            hashed_password = hash_password(data.password)

            # ── 3. Get the canonical STUDENT role ───────────────────────────
            role = db.query(Role).filter(
                Role.id == STUDENT_ROLE_ID,
                Role.name == STUDENT_ROLE_NAME,
            ).first()
            if not role:
                raise RuntimeError("Canonical STUDENT role (id=2) is not configured. Run Alembic migrations.")

            # ── 3b. Parse date of birth ───────────────────────────────────────
            date_of_birth = datetime.combine(data.date_of_birth, datetime.min.time())

            # ── 3c. Create and persist the User ──────────────────────────────
            now = datetime.utcnow()
            user = User(
                full_name=data.full_name,
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
                "full_name": user.full_name,
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

    @staticmethod
    def login_user(db: Session, data: LoginSchema) -> LoginResponseSchema:
        existing_user = db.query(User).filter(User.email == data.email).first()

        if not existing_user:
            raise InvalidCredentialsError

        if not verify_password(data.password, existing_user.password):
            raise InvalidCredentialsError

        if not existing_user.is_active:
            raise AccountDisabledError

        role_name = normalize_role_name(
            existing_user.role.name if existing_user.role else None
        )
        if role_name not in {"STUDENT", "EXPERT", "ADMIN"}:
            raise InactiveAccountError
        access_token = generate_token(
            data={
                "sub": str(existing_user.id),
                "email": existing_user.email,
                "role": role_name,
            }
        )

        user_principal = UserSchema.model_validate(existing_user).model_copy(
            update={"role_name": role_name}
        )
        return LoginResponseSchema(
            access_token=access_token,
            user_principal=user_principal,
        )
