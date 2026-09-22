from flask import Blueprint, render_template, request
from app.models.career_model import Career

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Página de inicio con presentación, guía para bachilleres y llamado a la acción."""
    categories = Career.get_categories()
    featured_careers = Career.get_all()[:6]
    return render_template('home.html', categories=categories, featured_careers=featured_careers)

@main_bp.route('/guia-vocacional')
def guide():
    """Guía paso a paso sobre cómo elegir carrera universitaria al salir del colegio."""
    return render_template('guide.html')

@main_bp.route('/carreras')
def careers_list():
    """Directorio y catálogo de carreras con buscador y filtros por área de conocimiento."""
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()
    
    careers = Career.get_all(category=category, search_term=search)
    categories = Career.get_categories()
    
    return render_template('careers/index.html', careers=careers, categories=categories, current_category=category, search=search)

@main_bp.route('/carreras/<slug>')
def career_detail(slug):
    """Ficha detallada de una carrera universitaria."""
    career = Career.get_by_slug(slug)
    if not career:
        # Si no se encuentra por slug, intentar por ID
        try:
            career = Career.get_by_id(int(slug))
        except ValueError:
            career = None

    if not career:
        return render_template('404.html', message="Carrera no encontrada"), 404

    # Carreras relacionadas en la misma área
    related = [c for c in Career.get_all(category=career['category']) if c['id'] != career['id']][:3]

    return render_template('careers/detail.html', career=career, related=related)

@main_bp.route('/comparador')
def compare_careers():
    """Comparador interactivo de 2 o 3 carreras lado a lado."""
    all_careers = Career.get_all()
    c1_id = request.args.get('c1', type=int)
    c2_id = request.args.get('c2', type=int)
    c3_id = request.args.get('c3', type=int)

    selected_ids = [cid for cid in [c1_id, c2_id, c3_id] if cid]
    
    # Si no se seleccionaron, elegir por defecto las dos primeras
    if not selected_ids and len(all_careers) >= 2:
        selected_ids = [all_careers[0]['id'], all_careers[1]['id']]

    selected_careers = Career.get_multiple_by_ids(selected_ids)

    return render_template('careers/compare.html', all_careers=all_careers, selected_careers=selected_careers, selected_ids=selected_ids)
