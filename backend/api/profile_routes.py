"""
Profile API Routes
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from services import AuthService, ProfileService
from models import db

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header[7:]
        user, error = AuthService.get_user_from_token(token)
        
        if error:
            return jsonify({'error': error}), 401
        
        request.user = user
        return f(*args, **kwargs)
    
    return decorated

@profile_bp.route('/manual', methods=['POST'])
@token_required
def create_manual_profile():
    """Create/update user profile with manual input"""
    data = request.get_json()
    
    profile, error = ProfileService.create_profile(
        user_id=request.user.id,
        education_level=data.get('education_level'),
        branch=data.get('branch'),
        experience_years=data.get('experience_years', 0),
        preferred_domains=data.get('preferred_domains')
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Profile created successfully',
        'profile': profile.to_dict()
    }), 201

@profile_bp.route('', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    profile = ProfileService.get_profile(request.user.id)
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify(profile.to_dict()), 200

@profile_bp.route('/skills', methods=['POST'])
@token_required
def add_skill():
    """Add skill to user profile"""
    data = request.get_json()
    
    if not data or 'skill_name' not in data:
        return jsonify({'error': 'Missing required field: skill_name'}), 400
    
    skill, error = ProfileService.add_skill(
        user_id=request.user.id,
        skill_name=data['skill_name'],
        skill_level=data.get('skill_level', 'intermediate'),
        years_experience=data.get('years_experience', 0)
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Skill added successfully',
        'skill': skill.to_dict()
    }), 201

@profile_bp.route('/skills', methods=['GET'])
@token_required
def get_skills():
    """Get all user skills"""
    skills = ProfileService.get_user_skills(request.user.id)
    
    return jsonify({
        'skills': skills,
        'total': len(skills)
    }), 200

@profile_bp.route('/skills/<skill_name>', methods=['DELETE'])
@token_required
def remove_skill(skill_name):
    """Remove skill from user profile"""
    from models import UserSkill
    
    skill = UserSkill.query.filter_by(
        user_id=request.user.id,
        skill_name=skill_name
    ).first()
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    db.session.delete(skill)
    db.session.commit()
    
    return jsonify({'message': 'Skill removed successfully'}), 200
