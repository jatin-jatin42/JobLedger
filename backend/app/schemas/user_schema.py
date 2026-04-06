import re
from marshmallow import fields, validates, ValidationError
from ..extensions import ma
from ..models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        fields = ('id', 'email', 'full_name', 'created_at')


class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    full_name = fields.String(required=True)

    @validates('password')
    def validate_password(self, value: str) -> str:
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters.')
        return value

    @validates('full_name')
    def validate_full_name(self, value: str) -> str:
        if len(value.strip()) < 2:
            raise ValidationError('Full name must be at least 2 characters.')
        if not re.match(r"^[a-zA-Z\s'\-]+$", value):
            raise ValidationError('Full name contains invalid characters.')
        return value


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


user_schema = UserSchema()
register_schema = RegisterSchema()
login_schema = LoginSchema()
