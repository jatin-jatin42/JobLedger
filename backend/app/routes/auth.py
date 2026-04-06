from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..services.auth_service import AuthService
from ..schemas.user_schema import register_schema, login_schema, user_schema

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = register_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    try:
        user = AuthService.register(data['email'], data['password'], data['full_name'])
    except ValueError as e:
        if str(e) == 'EMAIL_TAKEN':
            return jsonify({'error': 'Email is already registered.'}), 409
        return jsonify({'error': str(e)}), 400

    return jsonify({'data': user_schema.dump(user)}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    try:
        user, access_token = AuthService.login(data['email'], data['password'])
    except ValueError:
        return jsonify({'error': 'Invalid email or password.'}), 401

    return jsonify({
        'data': {
            'access_token': access_token,
            'user': user_schema.dump(user),
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify({'data': user_schema.dump(user)}), 200
