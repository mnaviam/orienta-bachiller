from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.result_model import TestResult
from app.models.career_model import Career

result_bp = Blueprint('result', __name__, url_prefix='/resultados')

@result_bp.route('/<code_or_id>')
def view_result(code_or_id):
    """Vista detallada de resultados para el estudiante."""
    result = TestResult.get_by_code(code_or_id)
    if not result:
        # Intentar por ID si es numérico
        try:
            conn_results = TestResult.get_recent(50)
            result = next((r for r in conn_results if str(r['id']) == str(code_or_id)), None)
        except Exception:
            result = None

    if not result:
        flash('No se encontró ningún resultado con ese código de test.', 'danger')
        return render_template('404.html', message="Resultado de test vocacional no encontrado"), 404

    # Extraer carreras recomendadas
    recommended_careers = result.get('recommended_careers', [])
    top_careers = recommended_careers[:6]
    secondary_careers = recommended_careers[6:12]

    # Mapeo de nombres legibles para dimensiones RIASEC
    riasec_names = {
        'R': 'Realista / Práctico',
        'I': 'Investigativo / Analítico',
        'A': 'Artístico / Creativo',
        'S': 'Social / Humanitario',
        'E': 'Emprendedor / Líder',
        'C': 'Convencional / Organizador'
    }

    # Mapeo de nombres de habilidades
    skill_names = {
        'logic_math': 'Lógico-Matemática',
        'verbal': 'Verbal y Comunicación',
        'spatial_creative': 'Espacial y Creativa',
        'social_leadership': 'Interpersonal y Liderazgo',
        'technical_manual': 'Técnica y Manual',
        'scientific_research': 'Científica y de Investigación'
    }

    return render_template(
        'results/view.html',
        result=result,
        top_careers=top_careers,
        secondary_careers=secondary_careers,
        riasec_names=riasec_names,
        skill_names=skill_names
    )

@result_bp.route('/<code_or_id>/imprimir')
def print_report(code_or_id):
    """Ficha vocacional imprimible en formato A4 / PDF para el estudiante y orientador."""
    result = TestResult.get_by_code(code_or_id)
    if not result:
        return render_template('404.html', message="Informe no encontrado"), 404

    top_careers = result.get('recommended_careers', [])[:5]

    riasec_names = {
        'R': 'Realista / Práctico',
        'I': 'Investigativo / Analítico',
        'A': 'Artístico / Creativo',
        'S': 'Social / Humanitario',
        'E': 'Emprendedor / Líder',
        'C': 'Convencional / Organizador'
    }

    skill_names = {
        'logic_math': 'Lógico-Matemática',
        'verbal': 'Verbal y Comunicación',
        'spatial_creative': 'Espacial y Creativa',
        'social_leadership': 'Interpersonal y Liderazgo',
        'technical_manual': 'Técnica y Manual',
        'scientific_research': 'Científica y de Investigación'
    }

    return render_template(
        'results/report_print.html',
        result=result,
        top_careers=top_careers,
        riasec_names=riasec_names,
        skill_names=skill_names
    )

@result_bp.route('/consultar', methods=['GET', 'POST'])
def search_result():
    """Permite al estudiante ingresar su código de test y ver sus resultados en cualquier momento."""
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        if not code:
            flash('Por favor ingresa un código de resultado.', 'warning')
            return render_template('results/search.html')
        
        result = TestResult.get_by_code(code)
        if result:
            return redirect(url_for('result.view_result', code_or_id=code))
        else:
            flash(f'No se encontró ningún test registrado con el código "{code}".', 'danger')

    return render_template('results/search.html')
