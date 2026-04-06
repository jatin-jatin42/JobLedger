from datetime import date
from marshmallow import fields, validates, validates_schema, ValidationError, EXCLUDE
from ..extensions import ma
from ..models.application import Application

VALID_STAGES = ['APPLIED', 'SCREENING', 'INTERVIEW', 'OFFER', 'REJECTED', 'WITHDRAWN']


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    applied_date = fields.Date()

    class Meta:
        model = Application
        load_instance = False
        fields = (
            'id', 'user_id', 'company_name', 'role_title', 'job_url',
            'location', 'salary_min', 'salary_max', 'stage',
            'applied_date', 'created_at', 'updated_at',
        )


class CreateApplicationSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    company_name = fields.String(required=True)
    role_title = fields.String(required=True)
    job_url = fields.String(load_default=None, allow_none=True)
    location = fields.String(load_default=None, allow_none=True)
    salary_min = fields.Integer(load_default=None, allow_none=True)
    salary_max = fields.Integer(load_default=None, allow_none=True)
    applied_date = fields.Date(load_default=None, allow_none=True)

    @validates('company_name')
    def validate_company_name(self, value: str) -> str:
        if not value or not value.strip():
            raise ValidationError('Company name cannot be empty.')
        return value

    @validates('role_title')
    def validate_role_title(self, value: str) -> str:
        if not value or not value.strip():
            raise ValidationError('Role title cannot be empty.')
        return value

    @validates('applied_date')
    def validate_applied_date(self, value: date) -> date:
        if value and value > date.today():
            raise ValidationError('applied_date cannot be in the future.')
        return value

    @validates_schema
    def validate_salary(self, data: dict, **kwargs) -> None:
        s_min = data.get('salary_min')
        s_max = data.get('salary_max')
        if s_min is not None and s_max is not None and s_min > s_max:
            raise ValidationError(
                {'salary_min': ['salary_min must be less than or equal to salary_max.']}
            )


class UpdateApplicationSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    company_name = fields.String()
    role_title = fields.String()
    job_url = fields.String(allow_none=True)
    location = fields.String(allow_none=True)
    salary_min = fields.Integer(allow_none=True)
    salary_max = fields.Integer(allow_none=True)
    applied_date = fields.Date(allow_none=True)

    @validates('applied_date')
    def validate_applied_date(self, value: date) -> date:
        if value and value > date.today():
            raise ValidationError('applied_date cannot be in the future.')
        return value

    @validates_schema
    def validate_salary(self, data: dict, **kwargs) -> None:
        s_min = data.get('salary_min')
        s_max = data.get('salary_max')
        if s_min is not None and s_max is not None and s_min > s_max:
            raise ValidationError(
                {'salary_min': ['salary_min must be less than or equal to salary_max.']}
            )


class StageUpdateSchema(ma.Schema):
    stage = fields.String(required=True)

    @validates('stage')
    def validate_stage(self, value: str) -> str:
        if value not in VALID_STAGES:
            raise ValidationError(
                f'Invalid stage. Must be one of: {", ".join(VALID_STAGES)}'
            )
        return value


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)
create_application_schema = CreateApplicationSchema()
update_application_schema = UpdateApplicationSchema()
stage_update_schema = StageUpdateSchema()
