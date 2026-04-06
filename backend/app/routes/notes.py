from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..services.note_service import NoteService
from ..schemas.note_schema import note_schema, notes_schema, create_note_schema

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/<application_id>/notes', methods=['GET'])
@jwt_required()
def get_notes(application_id):
    user_id = get_jwt_identity()
    notes, total = NoteService.get_all(application_id, user_id)
    if notes is None:
        return jsonify({'error': 'Application not found.'}), 404
    return jsonify({'data': notes_schema.dump(notes), 'total': total}), 200


@notes_bp.route('/<application_id>/notes', methods=['POST'])
@jwt_required()
def create_note(application_id):
    user_id = get_jwt_identity()
    try:
        data = create_note_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    note = NoteService.create(application_id, user_id, data['content'])
    if note is None:
        return jsonify({'error': 'Application not found.'}), 404

    return jsonify({'data': note_schema.dump(note)}), 201


@notes_bp.route('/<application_id>/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(application_id, note_id):
    user_id = get_jwt_identity()
    success, _ = NoteService.delete(note_id, application_id, user_id)
    if not success:
        return jsonify({'error': 'Note or application not found.'}), 404
    return '', 204
