"""
CareerAI - Cognitive Career Recommendation System
Main Flask Application
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from api import auth_bp, profile_bp, resume_bp, recommendations_bp, dashboard_bp
from services import JobDatasetLoader

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///career_ai.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(dashboard_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'CareerAI API is running'
        }), 200
    
    # Create tables and load data
    with app.app_context():
        db.create_all()
        JobDatasetLoader.load_job_dataset()
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("""
    ============================================================
      CareerAI - Cognitive Career Recommendation System
    ============================================================
    
    Production Backend API
    
    Available Endpoints:
    
    Authentication:
      POST   /api/auth/register
      POST   /api/auth/login
      POST   /api/auth/verify
    
    Profile:
      POST   /api/profile/manual
      GET    /api/profile
      POST   /api/profile/skills
      GET    /api/profile/skills
      DELETE /api/profile/skills/<skill_name>
    
    Resume:
      POST   /api/resume/upload
      GET    /api/resume/parsed-data
    
    Recommendations:
      GET    /api/recommendations
      GET    /api/recommendations/<job_id>
      GET    /api/recommendations/<job_id>/explain
      GET    /api/recommendations/roadmap/<job_id>
    
    Dashboard:
      GET    /api/dashboard/summary
      GET    /api/dashboard/stats
      GET    /api/dashboard/progress
    
    Status:
      GET    /api/health
    
    ============================================================
    """)
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
