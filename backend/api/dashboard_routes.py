"""
Dashboard API Routes
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from services import AuthService, SkillMatcher, ProfileService
from models import UserProfile, UserSkill, Job

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

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

@dashboard_bp.route('/summary', methods=['GET'])
@token_required
def dashboard_summary():
    """Get dashboard summary for user"""
    user = request.user
    profile = ProfileService.get_profile(user.id)
    
    # Get recommendations
    recommendations = SkillMatcher.get_all_recommendations(user.id, limit=5)
    
    # Get skills stats
    skills = UserSkill.query.filter_by(user_id=user.id).all()
    
    # Calculate aggregate match score
    top_match = recommendations[0][1] if recommendations else 0
    
    summary = {
        'user': {
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        },
        'profile': {
            'completeness': profile.profile_completeness if profile else 0,
            'education': profile.education_level if profile else None,
            'experience_years': profile.experience_years if profile else 0
        },
        'skills': {
            'total_count': len(skills),
            'skill_list': [s.skill_name for s in skills]
        },
        'recommendations': {
            'total_count': len(recommendations),
            'top_match_job': recommendations[0][0].job_title if recommendations else None,
            'top_match_score': round(top_match, 1) if top_match else 0,
            'top_recommendations': [
                {
                    'job_title': job.job_title,
                    'match_score': round(score, 1),
                    'domain': job.domain
                }
                for job, score in recommendations
            ]
        }
    }
    
    return jsonify(summary), 200

@dashboard_bp.route('/stats', methods=['GET'])
@token_required
def dashboard_stats():
    """Get detailed statistics for dashboard"""
    user = request.user
    profile = ProfileService.get_profile(user.id)
    skills = UserSkill.query.filter_by(user_id=user.id).all()
    
    # Skill level distribution
    skill_levels = {
        'expert': sum(1 for s in skills if s.skill_level == 'expert'),
        'intermediate': sum(1 for s in skills if s.skill_level == 'intermediate'),
        'beginner': sum(1 for s in skills if s.skill_level == 'beginner')
    }
    
    # Domain distribution
    job_count = Job.query.count()
    
    # Career recommendations
    recommendations = SkillMatcher.get_all_recommendations(user.id, limit=10)
    domain_scores = {}
    
    for job, score in recommendations:
        if job.domain not in domain_scores:
            domain_scores[job.domain] = []
        domain_scores[job.domain].append(score)
    
    # Average score by domain
    domain_avg = {
        domain: round(sum(scores) / len(scores), 1)
        for domain, scores in domain_scores.items()
    }
    
    stats = {
        'profile_completion': profile.profile_completeness if profile else 0,
        'total_skills': len(skills),
        'skill_distribution': skill_levels,
        'domain_scores': domain_avg,
        'recommendation_count': len(recommendations),
        'average_match_score': round(
            sum(score for _, score in recommendations) / len(recommendations), 1
        ) if recommendations else 0
    }
    
    return jsonify(stats), 200

@dashboard_bp.route('/progress', methods=['GET'])
@token_required
def profile_progress():
    """Get profile completion progress"""
    profile = ProfileService.get_profile(request.user.id)
    skills = UserSkill.query.filter_by(user_id=request.user.id).all()
    
    progress = {
        'profile_completeness': profile.profile_completeness if profile else 0,
        'skill_count': len(skills),
        'next_steps': []
    }
    
    # Suggest next steps
    if not profile or profile.profile_completeness < 100:
        progress['next_steps'].append('Complete your profile information')
    
    if len(skills) < 5:
        progress['next_steps'].append('Add more skills to your profile')
    
    progress['next_steps'].append('Get personalized career recommendations')
    
    return jsonify(progress), 200
