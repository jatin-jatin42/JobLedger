from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models.user import User
from ..extensions import db


class AuthService:

    @staticmethod
    def register(email: str, password: str, full_name: str) -> User:
        """Register a new user. Raises ValueError('EMAIL_TAKEN') on duplicate."""
        if User.query.filter_by(email=email.lower()).first():
            raise ValueError('EMAIL_TAKEN')

        user = User(
            email=email.lower(),
            password_hash=generate_password_hash(password),
            full_name=full_name.strip(),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email: str, password: str) -> tuple:
        """Login. Returns (user, access_token). Raises ValueError on bad credentials."""
        user = User.query.filter_by(email=email.lower()).first()
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError('INVALID_CREDENTIALS')

        access_token = create_access_token(identity=user.id)
        return user, access_token

    @staticmethod
    def get_user_by_id(user_id: str) -> User | None:
        return db.session.get(User, user_id)
