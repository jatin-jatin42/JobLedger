from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from ..services.application_service import ApplicationService


def require_application_ownership(f):
    """
    Route decorator that verifies the current JWT user owns the application.
    Injects `application` keyword argument into the route function on success.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        application_id = kwargs.get('application_id')
        if application_id:
            app = ApplicationService.get_by_id(application_id, user_id)
            if not app:
                return jsonify({'error': 'Application not found.'}), 404
            kwargs['application'] = app
        return f(*args, **kwargs)
    return decorated
