from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.application_service import ApplicationService
from ..schemas.application_schema import applications_schema

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    stats = ApplicationService.get_dashboard_stats(user_id)
    return jsonify({
        'data': {
            'total': stats['total'],
            'by_stage': stats['by_stage'],
            'recent_activity': applications_schema.dump(stats['recent_activity']),
        }
    }), 200
