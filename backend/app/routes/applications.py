from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..services.application_service import ApplicationService
from ..schemas.application_schema import (
    application_schema, applications_schema,
    create_application_schema, update_application_schema,
    stage_update_schema,
)
from ..schemas.note_schema import notes_schema

applications_bp = Blueprint('applications', __name__)


def _serialize(app, include_notes: bool = False) -> dict:
    data = application_schema.dump(app)
    if include_notes:
        data['notes'] = notes_schema.dump(app.notes)
    return data


@applications_bp.route('', methods=['GET'])
@jwt_required()
def list_applications():
    user_id = get_jwt_identity()
    apps = ApplicationService.get_all(
        user_id,
        stage=request.args.get('stage'),
        search=request.args.get('search'),
        sort_by=request.args.get('sort_by', 'updated_at'),
        order=request.args.get('order', 'desc'),
    )
    return jsonify({'data': applications_schema.dump(apps), 'total': len(apps)}), 200


@applications_bp.route('', methods=['POST'])
@jwt_required()
def create_application():
    user_id = get_jwt_identity()
    try:
        data = create_application_schema.load(request.get_json() or {})
    except ValidationError as e:
        msgs = e.messages
        # salary_min / applied_date errors are business-rule violations → 422
        if 'salary_min' in msgs or 'applied_date' in msgs:
            return jsonify({'error': msgs}), 422
        return jsonify({'error': msgs}), 400

    app = ApplicationService.create(user_id, data)
    return jsonify({'data': _serialize(app)}), 201


@applications_bp.route('/<application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    user_id = get_jwt_identity()
    app = ApplicationService.get_by_id(application_id, user_id)
    if not app:
        return jsonify({'error': 'Application not found.'}), 404
    return jsonify({'data': _serialize(app, include_notes=True)}), 200


@applications_bp.route('/<application_id>', methods=['PATCH'])
@jwt_required()
def update_application(application_id):
    user_id = get_jwt_identity()
    app = ApplicationService.get_by_id(application_id, user_id)
    if not app:
        return jsonify({'error': 'Application not found.'}), 404

    try:
        data = update_application_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    app = ApplicationService.update(app, data)
    return jsonify({'data': _serialize(app)}), 200


@applications_bp.route('/<application_id>/stage', methods=['PATCH'])
@jwt_required()
def update_stage(application_id):
    user_id = get_jwt_identity()
    app = ApplicationService.get_by_id(application_id, user_id)
    if not app:
        return jsonify({'error': 'Application not found.'}), 404

    try:
        data = stage_update_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    try:
        app = ApplicationService.update_stage(app, data['stage'])
    except ValueError as e:
        return jsonify({'error': str(e)}), 422

    return jsonify({'data': _serialize(app)}), 200


@applications_bp.route('/<application_id>', methods=['DELETE'])
@jwt_required()
def delete_application(application_id):
    user_id = get_jwt_identity()
    app = ApplicationService.get_by_id(application_id, user_id)
    if not app:
        return jsonify({'error': 'Application not found.'}), 404

    ApplicationService.delete(app)
    return '', 204
