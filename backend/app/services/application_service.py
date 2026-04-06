from datetime import date as date_type, datetime, timezone
from ..models.application import Application
from ..extensions import db

# ─── Single Source of Truth for State Machine ───────────────────────────────
VALID_TRANSITIONS: dict[str, list[str]] = {
    'APPLIED':   ['SCREENING', 'REJECTED', 'WITHDRAWN'],
    'SCREENING': ['INTERVIEW', 'REJECTED', 'WITHDRAWN'],
    'INTERVIEW': ['OFFER',     'REJECTED', 'WITHDRAWN'],
    'OFFER':     ['REJECTED',  'WITHDRAWN'],
    'REJECTED':  [],
    'WITHDRAWN': [],
}
# ─────────────────────────────────────────────────────────────────────────────


class ApplicationService:

    @staticmethod
    def get_all(
        user_id: str,
        stage: str | None = None,
        search: str | None = None,
        sort_by: str = 'updated_at',
        order: str = 'desc',
    ) -> list[Application]:
        query = Application.query.filter_by(user_id=user_id)

        if stage:
            query = query.filter_by(stage=stage.upper())

        if search:
            term = f'%{search}%'
            query = query.filter(
                db.or_(
                    Application.company_name.ilike(term),
                    Application.role_title.ilike(term),
                )
            )

        field_map = {
            'applied_date': Application.applied_date,
            'updated_at':   Application.updated_at,
            'company_name': Application.company_name,
        }
        sort_field = field_map.get(sort_by, Application.updated_at)
        query = query.order_by(sort_field.asc() if order == 'asc' else sort_field.desc())

        return query.all()

    @staticmethod
    def get_by_id(application_id: str, user_id: str) -> Application | None:
        return Application.query.filter_by(id=application_id, user_id=user_id).first()

    @staticmethod
    def create(user_id: str, data: dict) -> Application:
        applied_date = data.get('applied_date') or date_type.today()
        app = Application(
            user_id=user_id,
            company_name=data['company_name'].strip(),
            role_title=data['role_title'].strip(),
            job_url=data.get('job_url'),
            location=data.get('location'),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            applied_date=applied_date,
        )
        db.session.add(app)
        db.session.commit()
        return app

    @staticmethod
    def update(application: Application, data: dict) -> Application:
        updateable = [
            'company_name', 'role_title', 'job_url',
            'location', 'salary_min', 'salary_max', 'applied_date',
        ]
        for field in updateable:
            if field in data:
                setattr(application, field, data[field])
        application.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return application

    @staticmethod
    def update_stage(application: Application, new_stage: str) -> Application:
        """Enforce state machine. Raises ValueError on invalid transition."""
        current = application.stage
        valid_next = VALID_TRANSITIONS.get(current, [])

        if new_stage not in valid_next:
            if valid_next:
                msg = (
                    f'Cannot transition from {current} to {new_stage}. '
                    f'Valid next stages: {", ".join(valid_next)}.'
                )
            else:
                msg = f'{current} is a terminal stage — no further transitions are allowed.'
            raise ValueError(msg)

        application.stage = new_stage
        application.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return application

    @staticmethod
    def delete(application: Application) -> None:
        db.session.delete(application)
        db.session.commit()

    @staticmethod
    def get_dashboard_stats(user_id: str) -> dict:
        all_apps = Application.query.filter_by(user_id=user_id).all()

        by_stage = {s: 0 for s in VALID_TRANSITIONS}
        for app in all_apps:
            if app.stage in by_stage:
                by_stage[app.stage] += 1

        recent = (
            Application.query
            .filter_by(user_id=user_id)
            .order_by(Application.updated_at.desc())
            .limit(5)
            .all()
        )

        return {'total': len(all_apps), 'by_stage': by_stage, 'recent_activity': recent}
