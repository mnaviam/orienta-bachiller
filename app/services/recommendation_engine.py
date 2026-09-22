import math
from app.models.career_model import Career
from app.models.question_model import Question

# Definición de Arquetipos Vocacionales basados en combinaciones Holland
ARCHETYPES = {
    ('I', 'R'): {
        'title': 'El Creador Científico y Tecnológico',
        'badge': 'Innovación & Ingeniería',
        'icon': 'fa-solid fa-microchip',
        'desc': 'Posees una mente analítica orientada a la resolución práctica de problemas. Te apasiona entender cómo funcionan las cosas y crear o perfeccionar sistemas, maquinarias o tecnologías con bases científicas sólidas.'
    },
    ('R', 'I'): {
        'title': 'El Ingeniero y Constructor Práctico',
        'badge': 'Técnica & Ciencia',
        'icon': 'fa-solid fa-gears',
        'desc': 'Te motivan los retos tangibles y la aplicación directa de la ciencia. Tienes una habilidad natural para interactuar con herramientas, tecnología y proyectos físicos de gran impacto.'
    },
    ('I', 'A'): {
        'title': 'El Pensador Innovador y Visionario',
        'badge': 'Creatividad & Análisis',
        'icon': 'fa-solid fa-lightbulb',
        'desc': 'Combinas una profunda curiosidad intelectual con un pensamiento divergente y original. Eres capaz de idear soluciones vanguardistas cruzando ciencia, diseño y tecnología.'
    },
    ('A', 'I'): {
        'title': 'El Diseñador Conceptual',
        'badge': 'Arte & Lógica',
        'icon': 'fa-solid fa-palette',
        'desc': 'Tu creatividad se alimenta de la investigación y la comprensión profunda de conceptos. Te destacas por dar forma y estructura estética a ideas complejas.'
    },
    ('S', 'I'): {
        'title': 'El Sanador e Investigador Humano',
        'badge': 'Salud & Ciencias',
        'icon': 'fa-solid fa-heart-pulse',
        'desc': 'Posees una combinación única de vocación de servicio humanitario y rigor investigativo. Te orientas naturalmente hacia las ciencias de la salud y el bienestar integral de las personas.'
    },
    ('S', 'E'): {
        'title': 'El Líder Transformador y Educador',
        'badge': 'Liderazgo & Impacto Social',
        'icon': 'fa-solid fa-users-gear',
        'desc': 'Tienes un carisma innato para inspirar, orientar y organizar a grupos hacia metas comunes de desarrollo humano, social o educativo.'
    },
    ('E', 'S'): {
        'title': 'El Estratega Social y Comunicador',
        'badge': 'Gestión & Relaciones',
        'icon': 'fa-solid fa-bullhorn',
        'desc': 'Sobresales en la persuasión, las relaciones públicas y la dirección de iniciativas con impacto en las personas y comunidades.'
    },
    ('E', 'C'): {
        'title': 'El Emprendedor y Gestor Corporativo',
        'badge': 'Negocios & Estructura',
        'icon': 'fa-solid fa-briefcase',
        'desc': 'Posees visión estratégica y habilidad para organizar procesos, finanzas y personas para lograr altos estándares de rentabilidad y eficiencia.'
    },
    ('C', 'E'): {
        'title': 'El Organizador y Financiero de Éxito',
        'badge': 'Control & Finanzas',
        'icon': 'fa-solid fa-file-invoice-dollar',
        'desc': 'Eres meticuloso, estructurado y analítico en la toma de decisiones económicas y operativas, garantizando el éxito y cumplimiento normativo.'
    },
    ('A', 'S'): {
        'title': 'El Expresador Humanista',
        'badge': 'Arte & Sociedad',
        'icon': 'fa-solid fa-feather-pointed',
        'desc': 'Utilizas el arte, la comunicación y la creatividad como vehículo para conectar con las emociones de las personas y generar cambios positivos en la sociedad.'
    },
    ('C', 'I'): {
        'title': 'El Analista de Sistemas y Datos',
        'badge': 'Precisión & Investigación',
        'icon': 'fa-solid fa-chart-column',
        'desc': 'Te destacas por tu precisión metódica, amor por los datos verificables y rigor analítico para optimizar flujos de información.'
    },
    ('R', 'S'): {
        'title': 'El Cuidador del Entorno y la Vida Animal',
        'badge': 'Ciencias Agropecuarias & Veterinaria',
        'icon': 'fa-solid fa-paw',
        'desc': 'Combinas una fuerte orientación práctica con una profunda vocación de cuidado hacia los seres vivos y la naturaleza. Te motivan los entornos naturales, la salud animal y la producción sostenible.'
    },
    ('R', 'E'): {
        'title': 'El Productor y Líder Agroindustrial',
        'badge': 'Agronegocios & Producción',
        'icon': 'fa-solid fa-tractor',
        'desc': 'Unes la visión comercial y el liderazgo empresarial con la ejecución técnica en el campo y la agroindustria. Tienes talento para hacer rentables y sostenibles las actividades agroalimentarias.'
    }
}

DEFAULT_ARCHETYPE = {
    'title': 'El Perfil Multidimensional Equilibrado',
    'badge': 'Versatilidad Vocacional',
    'icon': 'fa-solid fa-compass',
    'desc': 'Cuentas con un perfil flexible y polifacético, con intereses balanceados en diversas áreas del conocimiento, lo que te permite adaptarte a carreras interdisciplinarias.'
}

class RecommendationEngine:
    """Motor de cálculo y recomendación vocacional basado en Holland RIASEC y Aptitudes."""

    @classmethod
    def process_test(cls, answers_dict):
        """
        answers_dict: dict con clave 'q_{question_id}' y valor int de 1 a 5 (escala Likert).
        """
        questions = Question.get_all()
        q_map = {str(q['id']): q for q in questions}

        # Acumuladores de puntajes
        riasec_raw = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}
        riasec_count = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}

        skills_raw = {
            'logic_math': 0, 'verbal': 0, 'spatial_creative': 0,
            'social_leadership': 0, 'technical_manual': 0, 'scientific_research': 0
        }
        skills_count = {
            'logic_math': 0, 'verbal': 0, 'spatial_creative': 0,
            'social_leadership': 0, 'technical_manual': 0, 'scientific_research': 0
        }

        # Procesar respuestas del formulario
        for key, val in answers_dict.items():
            if not key.startswith('q_'):
                continue
            q_id = key.replace('q_', '')
            if q_id not in q_map:
                continue

            q = q_map[q_id]
            try:
                score = float(val)
            except (ValueError, TypeError):
                score = 3.0  # valor neutro por defecto

            score = max(1.0, min(5.0, score)) # acotar entre 1 y 5

            if q['section'] == 'interests':
                dim = q['dimension']
                if dim in riasec_raw:
                    riasec_raw[dim] += score
                    riasec_count[dim] += 1
            elif q['section'] == 'skills':
                dim = q['dimension']
                if dim in skills_raw:
                    skills_raw[dim] += score
                    skills_count[dim] += 1

        # Normalizar puntajes a escala 0.0 a 1.0 (y porcentaje 0-100)
        riasec_norm = {}
        riasec_percent = {}
        for dim, total in riasec_raw.items():
            count = max(1, riasec_count[dim])
            avg = total / count
            # 1.0 -> 0.0, 5.0 -> 1.0
            norm = (avg - 1.0) / 4.0
            riasec_norm[dim] = round(norm, 4)
            riasec_percent[dim] = round(norm * 100, 1)

        skills_norm = {}
        skills_percent = {}
        for dim, total in skills_raw.items():
            count = max(1, skills_count[dim])
            avg = total / count
            norm = (avg - 1.0) / 4.0
            skills_norm[dim] = round(norm, 4)
            skills_percent[dim] = round(norm * 100, 1)

        # Identificar las dimensiones dominantes RIASEC
        sorted_riasec = sorted(riasec_norm.items(), key=lambda x: x[1], reverse=True)
        top1_dim, top1_val = sorted_riasec[0]
        top2_dim, top2_val = sorted_riasec[1]

        archetype_key = (top1_dim, top2_dim)
        archetype = ARCHETYPES.get(archetype_key, ARCHETYPES.get((top2_dim, top1_dim), DEFAULT_ARCHETYPE))

        # Evaluar compatibilidad con todas las carreras de la base de datos
        all_careers = Career.get_all()
        ranked_careers = []

        for c in all_careers:
            match_score, match_reasons = cls._calculate_career_affinity(c, riasec_norm, skills_norm)
            ranked_careers.append({
                'id': c['id'],
                'name': c['name'],
                'slug': c['slug'],
                'category': c['category'],
                'icon': c['icon'],
                'short_description': c['short_description'],
                'duration_semesters': c['duration_semesters'],
                'degree_title': c['degree_title'],
                'match_percentage': round(match_score * 100, 1),
                'match_reasons': match_reasons,
                'key_skills': c.get('key_skills', []),
                'labor_market': c.get('labor_market', [])
            })

        # Ordenar carreras de mayor a menor compatibilidad
        ranked_careers.sort(key=lambda x: x['match_percentage'], reverse=True)

        # Estructurar resultado
        result_data = {
            'riasec_scores': {
                'normalized': riasec_norm,
                'percentages': riasec_percent,
                'dominant_dims': [top1_dim, top2_dim]
            },
            'skill_scores': {
                'normalized': skills_norm,
                'percentages': skills_percent
            },
            'dominant_profile': archetype['title'],
            'dominant_profile_badge': archetype['badge'],
            'dominant_profile_icon': archetype['icon'],
            'dominant_profile_desc': archetype['desc'],
            'ranked_careers': ranked_careers,
            'top_careers': ranked_careers[:6],
            'secondary_careers': ranked_careers[6:12]
        }

        return result_data

    @classmethod
    def _calculate_career_affinity(cls, career, user_riasec, user_skills):
        """Calcula la distancia vectorial ponderada y afinidad porcentual."""
        
        # Pesos RIASEC
        riasec_dims = ['r', 'i', 'a', 's', 'e', 'c']
        riasec_diff_sum = 0.0
        riasec_weights_sum = 0.0

        for d in riasec_dims:
            c_val = float(career.get(f'riasec_{d}', 0.0))
            u_val = float(user_riasec.get(d.upper(), 0.0))
            # Ponderamos más las dimensiones donde la carrera exige un perfil alto
            weight = 0.5 + c_val
            diff = abs(u_val - c_val)
            riasec_diff_sum += weight * diff
            riasec_weights_sum += weight

        riasec_similarity = 1.0 - (riasec_diff_sum / max(0.001, riasec_weights_sum))

        # Pesos Aptitudes / Habilidades
        skill_dims = [
            'logic_math', 'verbal', 'spatial_creative',
            'social_leadership', 'technical_manual', 'scientific_research'
        ]
        skill_diff_sum = 0.0
        skill_weights_sum = 0.0

        for s in skill_dims:
            c_val = float(career.get(f'skill_{s}', 0.0))
            u_val = float(user_skills.get(s, 0.0))
            weight = 0.5 + c_val
            diff = abs(u_val - c_val)
            skill_diff_sum += weight * diff
            skill_weights_sum += weight

        skill_similarity = 1.0 - (skill_diff_sum / max(0.001, skill_weights_sum))

        # Ponderación combinada: 55% Preferencias/Intereses + 45% Habilidades/Aptitudes
        combined_raw = (0.55 * riasec_similarity) + (0.45 * skill_similarity)

        # Ajuste de escala para dar claridad (mapeo suave a 50% - 98%)
        # Si combined_raw es 1.0 -> 0.98, si es 0.5 -> 0.74, etc.
        adjusted_score = 0.50 + (combined_raw * 0.48)
        adjusted_score = max(0.40, min(0.98, adjusted_score))

        # Generar razones del match
        reasons = []
        if career.get('riasec_i', 0) >= 0.8 and user_riasec.get('I', 0) >= 0.6:
            reasons.append('Tu alta curiosidad investigativa y pensamiento analítico encajan perfectamente con el rigor académico de esta carrera.')
        if career.get('riasec_a', 0) >= 0.8 and user_riasec.get('A', 0) >= 0.6:
            reasons.append('Tu perfil creativo y capacidad de innovación estética son altamente valorados en este campo.')
        if career.get('riasec_s', 0) >= 0.8 and user_riasec.get('S', 0) >= 0.6:
            reasons.append('Tu vocación solidaria y habilidad para conectar con las personas son pilares fundamentales de esta profesión.')
        if career.get('riasec_e', 0) >= 0.8 and user_riasec.get('E', 0) >= 0.6:
            reasons.append('Tu liderazgo, persuasión y orientación a resultados impulsarán tu éxito en este entorno competitivo.')
        if career.get('riasec_r', 0) >= 0.8 and user_riasec.get('R', 0) >= 0.6:
            reasons.append('Tu destreza técnica, gusto por lo práctico y resolución tangible de problemas son ideales para esta disciplina.')
        if career.get('riasec_c', 0) >= 0.8 and user_riasec.get('C', 0) >= 0.6:
            reasons.append('Tu orden, método y atención a los detalles te permitirán destacar en la gestión y análisis estructurado.')

        if career.get('skill_logic_math', 0) >= 0.8 and user_skills.get('logic_math', 0) >= 0.6:
            reasons.append('Tu destreza lógico-matemática facilitará el dominio de las asignaturas técnicas y cuantitativas.')
        if career.get('skill_verbal', 0) >= 0.8 and user_skills.get('verbal', 0) >= 0.6:
            reasons.append('Tu fluidez verbal y facilidad de redacción y oratoria son fortalezas clave para esta carrera.')
        if career.get('skill_spatial_creative', 0) >= 0.8 and user_skills.get('spatial_creative', 0) >= 0.6:
            reasons.append('Tu visión espacial y talento creativo te dan una ventaja notable en el diseño de soluciones.')
        if career.get('skill_technical_manual', 0) >= 0.8 and user_skills.get('technical_manual', 0) >= 0.6:
            reasons.append('Tu alta destreza técnica e instrumental te permitirá dominar sistemas informáticos avanzados, circuitos y tecnología biomédica.')
        if career.get('skill_scientific_research', 0) >= 0.8 and user_skills.get('scientific_research', 0) >= 0.6:
            reasons.append('Tu rigor científico y pensamiento experimental son ideales para la investigación y el desarrollo tecnológico de vanguardia.')

        if not reasons:
            reasons.append('Tus intereses generales y habilidades proporcionan una base versátil para adaptarte con éxito a esta disciplina.')

        return adjusted_score, reasons[:2]
