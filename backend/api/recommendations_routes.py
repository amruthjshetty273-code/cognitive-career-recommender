"""
Recommendations API Routes
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import json
from services import (
    AuthService, SkillMatcher, CognitiveReasoner, 
    XAIExplainer, RoadmapGenerator
)
from models import db, Recommendation, Job

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

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

@recommendations_bp.route('', methods=['GET'])
@token_required
def get_recommendations():
    """Get all career recommendations for user"""
    limit = request.args.get('limit', 10, type=int)
    
    recommendations = SkillMatcher.get_all_recommendations(request.user.id, limit=limit)
    
    result = []
    for job, score in recommendations:
        rec_dict = {
            'job_id': job.id,
            'job_title': job.job_title,
            'domain': job.domain,
            'match_score': round(score, 1),
            'salary': job.average_salary,
            'demand': job.job_market_demand
        }
        result.append(rec_dict)
    
    return jsonify({
        'recommendations': result,
        'total': len(result)
    }), 200

@recommendations_bp.route('/<int:job_id>', methods=['GET'])
@token_required
def get_recommendation_detail(job_id):
    """Get detailed explanation for a specific job recommendation"""
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    # Calculate match score
    match_score = SkillMatcher.calculate_match_score(request.user.id, job_id)
    
    # Get skill analysis
    matched_skills = SkillMatcher.get_matched_skills(request.user.id, job_id)
    missing_skills = SkillMatcher.get_missing_skills(request.user.id, job_id)
    
    # Generate reasoning
    reasoning = CognitiveReasoner.generate_reasoning(
        request.user.id, job_id, matched_skills, missing_skills, match_score
    )
    
    # Generate XAI explanation
    xai_explanation = XAIExplainer.generate_xai_explanation(
        request.user.id, job_id, match_score, matched_skills, missing_skills, reasoning
    )
    
    # Generate roadmap
    roadmap = RoadmapGenerator.generate_roadmap(job.domain, missing_skills)
    
    # Store recommendation in database
    rec = Recommendation.query.filter_by(
        user_id=request.user.id,
        job_id=job_id
    ).first()
    
    if not rec:
        rec = Recommendation(
            user_id=request.user.id,
            job_id=job_id,
            match_score=match_score,
            matched_skills=json.dumps(list(matched_skills.keys())),
            missing_skills=json.dumps(list(missing_skills.keys())),
            reasoning=reasoning,
            learning_path=json.dumps(roadmap)
        )
        db.session.add(rec)
    else:
        rec.match_score = match_score
        rec.reasoning = reasoning
        rec.learning_path = json.dumps(roadmap)
    
    db.session.commit()
    
    return jsonify({
        'job': job.to_dict(),
        'explanation': xai_explanation,
        'roadmap': roadmap
    }), 200

@recommendations_bp.route('/explain/<int:job_id>', methods=['GET'])
@token_required
def explain_recommendation(job_id):
    """Get XAI explanation for a job recommendation"""
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    match_score = SkillMatcher.calculate_match_score(request.user.id, job_id)
    matched_skills = SkillMatcher.get_matched_skills(request.user.id, job_id)
    missing_skills = SkillMatcher.get_missing_skills(request.user.id, job_id)
    
    reasoning = CognitiveReasoner.generate_reasoning(
        request.user.id, job_id, matched_skills, missing_skills, match_score
    )
    
    explanation = XAIExplainer.generate_xai_explanation(
        request.user.id, job_id, match_score, matched_skills, missing_skills, reasoning
    )
    
    return jsonify(explanation), 200

@recommendations_bp.route('/roadmap/<int:job_id>', methods=['GET'])
@token_required
def get_career_roadmap(job_id):
    """Get learning roadmap for a job"""
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    missing_skills = SkillMatcher.get_missing_skills(request.user.id, job_id)
    roadmap = RoadmapGenerator.generate_roadmap(job.domain, missing_skills)
    
    return jsonify({
        'job_title': job.job_title,
        'domain': job.domain,
        'roadmap': roadmap,
        'total_steps': len(roadmap)
    }), 200
