"""
Resume API Routes
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from services import AuthService, ResumeService
from werkzeug.utils import secure_filename
import json

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

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

resume_service = ResumeService()

@resume_bp.route('/upload', methods=['POST'])
@token_required
def upload_resume():
    """Upload and parse resume"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    
    resume, error = resume_service.process_resume(
        user_id=request.user.id,
        file=file,
        filename=filename
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Resume uploaded and processed successfully',
        'resume': resume.to_dict()
    }), 201

@resume_bp.route('/parsed-data', methods=['GET'])
@token_required
def get_parsed_data():
    """Get parsed resume data"""
    from models import Resume
    
    resume = Resume.query.filter_by(user_id=request.user.id).first()
    
    if not resume:
        return jsonify({'error': 'No resume found'}), 404
    
    parsed_data = json.loads(resume.parsed_data) if resume.parsed_data else {}
    
    return jsonify({
        'filename': resume.filename,
        'file_type': resume.file_type,
        'parsed_data': parsed_data,
        'created_at': resume.created_at.isoformat()
    }), 200
