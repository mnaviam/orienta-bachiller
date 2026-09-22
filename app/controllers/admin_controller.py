from flask import Blueprint, render_template
from app.models.result_model import TestResult
from app.models.career_model import Career

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Panel de control para orientadores escolares y administradores."""
    stats = TestResult.get_stats()
    recent_tests = TestResult.get_recent(limit=15)
    all_careers = Career.get_all()

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_tests=recent_tests,
        total_careers=len(all_careers)
    )
