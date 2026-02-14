"""
Authentication API Routes
"""

from flask import Blueprint, request, jsonify
from services import AuthService
from models import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields: name, email, password'}), 400
    
    user, error = AuthService.register(
        name=data['name'],
        email=data['email'],
        password=data['password']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing required fields: email, password'}), 400
    
    token, error = AuthService.login(
        email=data['email'],
        password=data['password']
    )
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'message': 'Login successful',
        'token': token
    }), 200

@auth_bp.route('/verify', methods=['POST'])
def verify():
    """Verify JWT token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    token = auth_header[7:]  # Remove 'Bearer '
    user, error = AuthService.get_user_from_token(token)
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'valid': True,
        'user': user.to_dict()
    }), 200
