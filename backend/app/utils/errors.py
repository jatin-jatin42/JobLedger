import logging
from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError

logger = logging.getLogger(__name__)


def register_error_handlers(app) -> None:

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': str(e.description)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'Authentication required.'}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'Access denied.'}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found.'}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'Method not allowed.'}), 405

    @app.errorhandler(409)
    def conflict(e):
        return jsonify({'error': str(e.description)}), 409

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({'error': str(e.description)}), 422

    @app.errorhandler(500)
    def internal_error(e):
        logger.error('Internal server error: %s', e, exc_info=True)
        return jsonify({'error': 'An unexpected error occurred.'}), 500

    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth(e):
        return jsonify({'error': 'Authentication required.'}), 401

    @app.errorhandler(InvalidHeaderError)
    def handle_invalid_header(e):
        return jsonify({'error': 'Authentication required.'}), 401
