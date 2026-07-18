from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token
from app.core.exceptions import UserAlreadyExists
from app.core.exceptions import InvalidCredentials


class AuthService:

    @staticmethod
    def register(db: Session, data):

        user = UserRepository.get_by_email(
            db,
            data.email
        )

        if user:
            raise UserAlreadyExists()

        new_user = User(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password)
        )

        return UserRepository.create(
            db,
            new_user
        )

    @staticmethod
    def login(db: Session, data):

        user = UserRepository.get_by_email(
            db,
            data.email
        )

        if not user:
            raise InvalidCredentials()

        if not verify_password(
            data.password,
            user.password
        ):
            raise InvalidCredentials()

        token = create_access_token(
            {
                "sub": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }