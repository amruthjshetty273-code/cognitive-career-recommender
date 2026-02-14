"""
API Routes Init
"""

from .auth_routes import auth_bp
from .profile_routes import profile_bp
from .resume_routes import resume_bp
from .recommendations_routes import recommendations_bp
from .dashboard_routes import dashboard_bp

__all__ = [
    'auth_bp',
    'profile_bp',
    'resume_bp',
    'recommendations_bp',
    'dashboard_bp'
]
