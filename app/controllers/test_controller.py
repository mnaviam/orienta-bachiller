from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.question_model import Question
from app.models.result_model import TestResult
from app.services.recommendation_engine import RecommendationEngine

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/iniciar', methods=['GET', 'POST'])
def start_test():
    """Formulario de bienvenida e inicio de datos del estudiante bachiller."""
    if request.method == 'POST':
        name = request.form.get('student_name', '').strip()
        school = request.form.get('student_school', '').strip()
        grade = request.form.get('student_grade', '').strip()
        age = request.form.get('student_age', '').strip()
        email = request.form.get('student_email', '').strip()

        if not name:
            flash('Por favor ingresa tu nombre completo para comenzar.', 'warning')
            return render_template('test/start.html')

        session['student_info'] = {
            'name': name,
            'school': school,
            'grade': grade,
            'age': age,
            'email': email
        }
        return redirect(url_for('test.quiz'))

    return render_template('test/start.html')

@test_bp.route('/cuestionario', methods=['GET'])
def quiz():
    """Cuestionario vocacional interactivo por pasos."""
    student_info = session.get('student_info')
    if not student_info:
        flash('Por favor ingresa tus datos básicos antes de responder el cuestionario.', 'info')
        return redirect(url_for('test.start_test'))

    grouped_questions = Question.get_grouped_by_section()
    total_questions = len(grouped_questions['interests']) + len(grouped_questions['skills'])

    return render_template(
        'test/quiz.html',
        student_info=student_info,
        interests_questions=grouped_questions['interests'],
        skills_questions=grouped_questions['skills'],
        total_questions=total_questions
    )

@test_bp.route('/procesar', methods=['POST'])
def process():
    """Procesa las respuestas del cuestionario y genera las recomendaciones."""
    student_info = session.get('student_info', {
        'name': request.form.get('student_name', 'Estudiante'),
        'school': request.form.get('student_school', ''),
        'grade': request.form.get('student_grade', ''),
        'age': request.form.get('student_age', 17),
        'email': request.form.get('student_email', '')
    })

    # Extraer respuestas del formulario
    raw_answers = {k: v for k, v in request.form.items() if k.startswith('q_')}

    if not raw_answers:
        flash('No se recibieron respuestas. Por favor responde las preguntas del test.', 'danger')
        return redirect(url_for('test.quiz'))

    # Ejecutar motor de recomendación
    results = RecommendationEngine.process_test(raw_answers)

    # Guardar en base de datos
    code = TestResult.save(
        student_data=student_info,
        riasec_scores=results['riasec_scores'],
        skill_scores=results['skill_scores'],
        dominant_profile=results['dominant_profile'],
        dominant_profile_desc=results['dominant_profile_desc'],
        recommended_careers=results['ranked_careers'],
        raw_answers=raw_answers
    )

    # Limpiar información temporal de sesión
    session.pop('student_info', None)

    return redirect(url_for('result.view_result', code_or_id=code))
