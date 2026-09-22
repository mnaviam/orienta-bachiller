import sqlite3
import json
import os
from config import Config

def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite con soporte para nombres de columna."""
    db_path = Config.DATABASE_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la estructura de la base de datos e inserta los datos iniciales si no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla de Carreras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        icon TEXT NOT NULL,
        short_description TEXT NOT NULL,
        full_description TEXT NOT NULL,
        duration_semesters INTEGER NOT NULL,
        degree_title TEXT NOT NULL,
        labor_market TEXT NOT NULL,
        key_skills TEXT NOT NULL,
        typical_subjects TEXT NOT NULL,
        reasons_to_study TEXT NOT NULL,
        riasec_r REAL NOT NULL DEFAULT 0.0,
        riasec_i REAL NOT NULL DEFAULT 0.0,
        riasec_a REAL NOT NULL DEFAULT 0.0,
        riasec_s REAL NOT NULL DEFAULT 0.0,
        riasec_e REAL NOT NULL DEFAULT 0.0,
        riasec_c REAL NOT NULL DEFAULT 0.0,
        skill_logic_math REAL NOT NULL DEFAULT 0.0,
        skill_verbal REAL NOT NULL DEFAULT 0.0,
        skill_spatial_creative REAL NOT NULL DEFAULT 0.0,
        skill_social_leadership REAL NOT NULL DEFAULT 0.0,
        skill_technical_manual REAL NOT NULL DEFAULT 0.0,
        skill_scientific_research REAL NOT NULL DEFAULT 0.0
    )
    ''')

    # Tabla de Preguntas del Test
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section TEXT NOT NULL, -- 'interests' o 'skills'
        dimension TEXT NOT NULL, -- 'R','I','A','S','E','C' o 'logic_math','verbal', etc.
        dimension_name TEXT NOT NULL,
        text TEXT NOT NULL,
        subtitle TEXT,
        icon TEXT,
        order_num INTEGER NOT NULL
    )
    ''')

    # Tabla de Resultados de Tests
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        student_name TEXT NOT NULL,
        student_school TEXT,
        student_grade TEXT,
        student_email TEXT,
        student_age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        riasec_scores_json TEXT NOT NULL,
        skill_scores_json TEXT NOT NULL,
        dominant_profile TEXT NOT NULL,
        dominant_profile_desc TEXT NOT NULL,
        recommended_careers_json TEXT NOT NULL,
        answers_json TEXT NOT NULL
    )
    ''')

    conn.commit()

    # Verificar si ya existen carreras y preguntas
    cursor.execute('SELECT COUNT(*) as count FROM careers')
    if cursor.fetchone()['count'] == 0:
        seed_careers(conn)

    cursor.execute('SELECT COUNT(*) as count FROM questions')
    if cursor.fetchone()['count'] == 0:
        seed_questions(conn)

    conn.close()

def seed_questions(conn):
    cursor = conn.cursor()
    questions = [
        # --- SECCIÓN 1: INTERESES Y PREFERENCIAS (RIASEC) ---
        # REALISTA (R)
        (
            'interests', 'R', 'Realista / Práctico',
            '¿Te entusiasma desarmar cosas, armar modelos mecánicos, usar herramientas o trabajar con maquinaria y circuitos?',
            'Atracción por actividades manuales, técnicas, mecánicas y tangibles.',
            'fa-solid fa-wrench', 1
        ),
        (
            'interests', 'R', 'Realista / Práctico',
            '¿Prefieres actividades al aire libre, trabajo de campo, interacción con animales, cultivos o proyectos prácticos antes que permanecer todo el día en un escritorio?',
            'Gusto por la naturaleza, el sector agropecuario, los seres vivos y la ejecución en campo.',
            'fa-solid fa-seedling', 2
        ),
        # INVESTIGATIVO (I)
        (
            'interests', 'I', 'Investigativo / Analítico',
            '¿Te apasiona descubrir el "por qué" de las cosas, hacer experimentos, investigar sobre ciencia o resolver enigmas lógicos complejos?',
            'Curiosidad intelectual, razonamiento abstracto e investigación.',
            'fa-solid fa-microscope', 3
        ),
        (
            'interests', 'I', 'Investigativo / Analítico',
            '¿Disfrutas analizar datos, patrones matemáticos, estadísticas o comprender fenómenos naturales y tecnológicos a fondo?',
            'Afinidad con el análisis cuantitativo y la deducción lógica.',
            'fa-solid fa-brain', 4
        ),
        # ARTÍSTICO (A)
        (
            'interests', 'A', 'Artístico / Creativo',
            '¿Te sientes motivado/a creando cosas originales: dibujar, diseñar interfaces, escribir historias, componer música o producir contenido audiovisual?',
            'Búsqueda de autoexpresión, originalidad estética e innovación libre.',
            'fa-solid fa-palette', 5
        ),
        (
            'interests', 'A', 'Artístico / Creativo',
            '¿Valoras los entornos flexibles, poco rutinarios y con libertad para romper esquemas tradicionales y proponer soluciones no convencionales?',
            'Preferencia por la creatividad sobre estructuras rígidas.',
            'fa-solid fa-wand-magic-sparkles', 6
        ),
        # SOCIAL (S)
        (
            'interests', 'S', 'Social / Humanitario',
            '¿Sientes una vocación genuina por ayudar a los demás, escuchar sus problemas, cuidar su bienestar o enseñarles algo nuevo?',
            'Orientación hacia el servicio a la comunidad, la empatía y la salud.',
            'fa-solid fa-hand-holding-heart', 7
        ),
        (
            'interests', 'S', 'Social / Humanitario',
            '¿Te desenvuelves con facilidad trabajando en equipo, coordinando grupos y buscando el bienestar colectivo o la justicia social?',
            'Habilidad para conectar humanamente y generar impacto social.',
            'fa-solid fa-users', 8
        ),
        # EMPRENDEDOR (E)
        (
            'interests', 'E', 'Emprendedor / Líder',
            '¿Te atrae la idea de liderar proyectos, convencer a personas con tus ideas, crear tu propio negocio o negociar acuerdos?',
            'Iniciativa, persuasión, ambición y capacidad de toma de decisiones.',
            'fa-solid fa-chart-line', 9
        ),
        (
            'interests', 'E', 'Emprendedor / Líder',
            '¿Te motiva asumir retos competitivos, hablar en público y orientar los esfuerzos hacia metas de alto rendimiento y éxito?',
            'Gusto por el dinamismo comercial, la influencia y la gestión estratégica.',
            'fa-solid fa-bullhorn', 10
        ),
        # CONVENCIONAL (C)
        (
            'interests', 'C', 'Convencional / Organizador',
            '¿Te agrada trabajar de forma ordenada y metódica: organizar archivos, llevar presupuestos claros y seguir normas precisas?',
            'Preferencia por la estructura, el control de calidad y la claridad en los procesos.',
            'fa-solid fa-folder-tree', 11
        ),
        (
            'interests', 'C', 'Convencional / Organizador',
            '¿Prefieres tareas con instrucciones definidas y objetivos estructurados donde la precisión y el detalle sean fundamentales?',
            'Enfoque en la eficiencia operativa, la minuciosidad y la fiabilidad.',
            'fa-solid fa-clipboard-check', 12
        ),

        # --- SECCIÓN 2: AUTOEVALUACIÓN DE HABILIDADES Y APTITUDES ---
        # LÓGICO-MATEMÁTICA
        (
            'skills', 'logic_math', 'Lógico-Matemática',
            '¿Qué tan hábil te consideras para resolver problemas matemáticos, operar con fórmulas y razonar con lógica y números?',
            'Capacidad de cálculo, pensamiento algorítmico y deducción formal.',
            'fa-solid fa-calculator', 13
        ),
        (
            'skills', 'logic_math', 'Lógico-Matemática',
            '¿Con qué facilidad entiendes problemas abstractos, diagramas de flujo o lógica de programación e informática?',
            'Habilidad de abstracción y pensamiento estructurado.',
            'fa-solid fa-laptop-code', 14
        ),
        # VERBAL Y COMUNICACIÓN
        (
            'skills', 'verbal', 'Verbal y Comunicación',
            '¿Qué tan bien te desenvuelves redactando ensayos, argumentando ideas de forma oral o leyendo textos complejos con buena comprensión?',
            'Dominio del lenguaje, vocabulario, redacción y elocuencia.',
            'fa-solid fa-book-open', 15
        ),
        (
            'skills', 'verbal', 'Verbal y Comunicación',
            '¿Qué tanta facilidad tienes para sintetizar información, comunicar conceptos difíciles de forma sencilla o aprender nuevos idiomas?',
            'Fluidez expresiva y capacidad explicativa.',
            'fa-solid fa-comments', 16
        ),
        # ESPACIAL Y CREATIVA
        (
            'skills', 'spatial_creative', 'Espacial y Creativa',
            '¿Qué tan hábil eres visualizando objetos en 3D, combinando colores, diseñando composiciones visuales o interpretando planos y mapas?',
            'Inteligencia visual, percepción espacial y sentido estético.',
            'fa-solid fa-cube', 17
        ),
        (
            'skills', 'spatial_creative', 'Espacial y Creativa',
            '¿Con qué frecuencia se te ocurren ideas novedosas frente a un problema donde los demás solo ven obstáculos comunes?',
            'Pensamiento divergente e ingenio innovador.',
            'fa-solid fa-lightbulb', 18
        ),
        # INTERPERSONAL Y LIDERAZGO
        (
            'skills', 'social_leadership', 'Interpersonal y Liderazgo',
            '¿Qué tan hábil eres mediando conflictos entre compañeros, motivando a un grupo o entendiendo los sentimientos de los demás?',
            'Empatía, inteligencia emocional y facilitación de consensos.',
            'fa-solid fa-people-arrows', 19
        ),
        (
            'skills', 'social_leadership', 'Interpersonal y Liderazgo',
            '¿Qué tan seguro/a te sientes al coordinar a tus compañeros en una exposición o proyecto escolar para lograr una meta común?',
            'Liderazgo situacional y persuasión positiva.',
            'fa-solid fa-users-gear', 20
        ),
        # TÉCNICA Y MANUAL
        (
            'skills', 'technical_manual', 'Técnica y Manual',
            '¿Qué tan diestro/a eres en el manejo de instrumentos de precisión, equipos tecnológicos, reparaciones o maquetas físicas?',
            'Coordinación visomotora, motricidad fina y habilidad técnica.',
            'fa-solid fa-screwdriver-wrench', 21
        ),
        (
            'skills', 'technical_manual', 'Técnica y Manual',
            '¿Con qué rapidez aprendes a manejar nuevas herramientas digitales complejas, software especializado o aparatos electrónicos?',
            'Adaptabilidad tecnológica y destreza operativa.',
            'fa-solid fa-microchip', 22
        ),
        # CIENTÍFICA Y DE INVESTIGACIÓN
        (
            'skills', 'scientific_research', 'Científica y de Investigación',
            '¿Qué tan riguroso/a y metódico/a eres cuando necesitas comprobar una hipótesis, buscar fuentes confiables o realizar un trabajo académico?',
            'Método científico, pensamiento crítico y análisis documental.',
            'fa-solid fa-flask-vial', 23
        ),
        (
            'skills', 'scientific_research', 'Científica y de Investigación',
            '¿Con qué profundidad sueles cuestionar afirmaciones hasta encontrar pruebas sólidas y explicaciones comprobables?',
            'Curiosidad epistemológica y verificación analítica.',
            'fa-solid fa-magnifying-glass-chart', 24
        )
    ]

    cursor.executemany('''
    INSERT INTO questions (section, dimension, dimension_name, text, subtitle, icon, order_num)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', questions)
    conn.commit()

def seed_careers(conn):
    cursor = conn.cursor()
    careers = [
        {
            'name': 'Ingeniería de Software y Sistemas',
            'slug': 'ingenieria-software-sistemas',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-laptop-code',
            'short_description': 'Diseña, programa y optimiza aplicaciones, arquitecturas en la nube, inteligencia artificial y soluciones informáticas de alto impacto.',
            'full_description': 'La Ingeniería de Software forma profesionales de Tercer Nivel capaces de liderar la transformación digital mediante el desarrollo de aplicaciones web y móviles, inteligencia artificial, ciberseguridad y computación en la nube en empresas nacionales e internacionales.',
            'duration_semesters': 10,
            'degree_title': 'Ingeniero/a en Software (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Empresas tecnológicas globales (Big Tech)', 'Startups y empresas de base tecnológica en Ecuador', 'Sector financiero, banca y Fintech', 'Consultoría en transformación digital', 'Trabajo remoto internacional independiente']),
            'key_skills': json.dumps(['Programación y Algoritmia', 'Pensamiento Lógico y Abstracto', 'Resolución de Problemas Complejos', 'Arquitectura de Software y Cloud', 'Trabajo Colaborativo Ágil']),
            'typical_subjects': json.dumps(['Estructuras de Datos y Algoritmos', 'Bases de Datos Relacionales y NoSQL', 'Inteligencia Artificial y Machine Learning', 'Ingeniería de Software', 'Ciberseguridad y Redes']),
            'reasons_to_study': json.dumps([
                'Te apasiona la tecnología y la creación de soluciones digitales desde cero.',
                'Disfrutas de los retos intelectuales y el razonamiento lógico.',
                'Buscas una profesión de altísima demanda y flexibilidad global de trabajo.'
            ]),
            'riasec_r': 0.6, 'riasec_i': 0.95, 'riasec_a': 0.45, 'riasec_s': 0.3, 'riasec_e': 0.6, 'riasec_c': 0.75,
            'skill_logic_math': 0.95, 'skill_verbal': 0.5, 'skill_spatial_creative': 0.6, 'skill_social_leadership': 0.5, 'skill_technical_manual': 0.75, 'skill_scientific_research': 0.85
        },
        {
            'name': 'Medicina Humana',
            'slug': 'medicina-humana',
            'category': 'Ciencias de la Salud',
            'icon': 'fa-solid fa-user-doctor',
            'short_description': 'Diagnostica, trata y previene enfermedades para preservar y mejorar la calidad de vida y salud de las personas.',
            'full_description': 'Medicina es una disciplina científica y humanista dedicada al cuidado integral de la salud, la prevención patológica y el tratamiento de pacientes en la red de salud pública (IESS, MSP) y clínicas privadas del Ecuador.',
            'duration_semesters': 12,
            'degree_title': 'Médico/a (Tercer Nivel con Internado Rotativo)',
            'labor_market': json.dumps(['Hospitales y clínicas de alta complejidad', 'Centros de atención primaria y salud pública', 'Investigación médica y ensayos clínicos', 'Organizaciones de ayuda humanitaria (OMS, Cruz Roja)', 'Práctica médica privada y especializada']),
            'key_skills': json.dumps(['Pensamiento Clínico y Diagnóstico', 'Empatía y Comunicación Asertiva', 'Toma de Decisiones bajo Presión', 'Rigor Científico y Biológico', 'Destreza Procedimental']),
            'typical_subjects': json.dumps(['Anatomía y Fisiología Humana', 'Farmacología Clínica', 'Patología y Microbiología', 'Semiología y Medicina Interna', 'Cirugía y Urgencias Médicas']),
            'reasons_to_study': json.dumps([
                'Tienes una profunda vocación de servicio y empatía hacia los demás.',
                'Te fascina el funcionamiento biológico del cuerpo humano.',
                'Estás dispuesto/a a asumir un compromiso constante de estudio y rigor ético.'
            ]),
            'riasec_r': 0.45, 'riasec_i': 0.95, 'riasec_a': 0.2, 'riasec_s': 0.95, 'riasec_e': 0.4, 'riasec_c': 0.65,
            'skill_logic_math': 0.65, 'skill_verbal': 0.8, 'skill_spatial_creative': 0.55, 'skill_social_leadership': 0.85, 'skill_technical_manual': 0.7, 'skill_scientific_research': 0.95
        },
        {
            'name': 'Diseño Gráfico y Comunicación Visual',
            'slug': 'diseno-grafico-comunicacion-visual',
            'category': 'Arte y Diseño',
            'icon': 'fa-solid fa-pen-nib',
            'short_description': 'Transforma ideas en mensajes visuales impactantes a través de branding, diseño digital, UI/UX, animación e ilustración.',
            'full_description': 'El Diseño Gráfico integra arte, psicología visual y tecnología para crear identidades de marca, interfaces de usuario interactivas, empaques, campañas publicitarias y narrativa audiovisual contemporánea.',
            'duration_semesters': 8,
            'degree_title': 'Licenciado/a en Diseño Gráfico / Comunicación Visual',
            'labor_market': json.dumps(['Agencias de publicidad y marketing digital', 'Estudios de diseño y branding', 'Empresas de software (Diseño UI/UX)', 'Editoriales y medios digitales', 'Trabajo Freelance para marcas internacionales']),
            'key_skills': json.dumps(['Creatividad Visual e Ilustración', 'Dominio de Herramientas de Diseño Digital (Adobe/Figma)', 'Tipografía y Teoría del Color', 'Diseño de Experiencia de Usuario (UX/UI)', 'Comunicación Conceptual']),
            'typical_subjects': json.dumps(['Fundamentos de Composición y Color', 'Diseño de Identidad y Branding', 'Diseño Web e Interfaces Digitales (UI/UX)', 'Animación Digital y Motion Graphics', 'Fotografía y Edición Digital']),
            'reasons_to_study': json.dumps([
                'Expresas tu creatividad a través de formas, colores, imágenes y tecnología.',
                'Te gusta crear proyectos visuales que llamen la atención y comuniquen emociones.',
                'Buscas una carrera dinámica e innovadora con gran campo digital.'
            ]),
            'riasec_r': 0.35, 'riasec_i': 0.4, 'riasec_a': 0.98, 'riasec_s': 0.45, 'riasec_e': 0.55, 'riasec_c': 0.35,
            'skill_logic_math': 0.35, 'skill_verbal': 0.7, 'skill_spatial_creative': 0.98, 'skill_social_leadership': 0.5, 'skill_technical_manual': 0.65, 'skill_scientific_research': 0.4
        },
        {
            'name': 'Administración de Empresas y Negocios Internacionales',
            'slug': 'administracion-empresas-negocios',
            'category': 'Negocios y Finanzas',
            'icon': 'fa-solid fa-briefcase',
            'short_description': 'Lidera organizaciones, formula estrategias comerciales rentables, gestiona equipos y abre mercados globales.',
            'full_description': 'Forma líderes estratégicos con visión empresarial para planificar, organizar, dirigir y controlar recursos financieros, humanos y de mercado en empresas nacionales e internacionales.',
            'duration_semesters': 8,
            'degree_title': 'Licenciado/a en Administración de Empresas / Negocios Internacionales',
            'labor_market': json.dumps(['Corporaciones multinacionales y empresas privadas', 'Emprendimientos y negocios propios', 'Comercio exterior y aduanas', 'Consultoría gerencial y estratégica', 'Entidades financieras y bursátiles']),
            'key_skills': json.dumps(['Liderazgo y Gestión de Equipos', 'Planificación Estratégica y Negociación', 'Análisis Financiero y de Mercado', 'Toma de Decisiones y Manejo del Riesgo', 'Comunicación Persuasiva']),
            'typical_subjects': json.dumps(['Estrategia Empresarial y Gestión del Cambio', 'Marketing Estratégico y Digital', 'Finanzas Corporativas y Contabilidad', 'Comercio y Logística Internacional', 'Gestión del Talento Humano']),
            'reasons_to_study': json.dumps([
                'Te entusiasma liderar proyectos, coordinar personas y hacer realidad ideas de negocio.',
                'Tienes facilidad para negociar, comunicar y tomar decisiones prácticas.',
                'Quieres dominar el mundo corporativo y la creación de empresas exitosas.'
            ]),
            'riasec_r': 0.25, 'riasec_i': 0.5, 'riasec_a': 0.35, 'riasec_s': 0.65, 'riasec_e': 0.98, 'riasec_c': 0.8,
            'skill_logic_math': 0.7, 'skill_verbal': 0.85, 'skill_spatial_creative': 0.5, 'skill_social_leadership': 0.95, 'skill_technical_manual': 0.3, 'skill_scientific_research': 0.55
        },
        {
            'name': 'Psicología',
            'slug': 'psicologia',
            'category': 'Ciencias Sociales y Humanidades',
            'icon': 'fa-solid fa-head-side-virus',
            'short_description': 'Comprende la mente y el comportamiento humano para brindar apoyo emocional, clínico, educativo y organizacional.',
            'full_description': 'Estudia los procesos cognitivos, afectivos y conductuales del ser humano. Los psicólogos evalúan, diagnostican y facilitan intervenciones terapéuticas, desarrollo de talento humano y programas de bienestar mental.',
            'duration_semesters': 10,
            'degree_title': 'Licenciado/a en Psicología / Psicólogo/a',
            'labor_market': json.dumps(['Centros de salud mental, hospitales y clínicas', 'Instituciones educativas y departamentos de orientación', 'Departamentos de Recursos Humanos y Talento', 'Consultoría en bienestar y psicología deportiva', 'Investigación social y comunitaria']),
            'key_skills': json.dumps(['Escucha Activa y Empatía Profunda', 'Evaluación Psicológica y Diagnóstico', 'Capacidad de Análisis Crítico', 'Comunicación Terapéutica Asertiva', 'Ética y Confidencialidad']),
            'typical_subjects': json.dumps(['Psicología del Desarrollo y Ciclo Vital', 'Neurociencias y Psicobiología', 'Psicología Clínica y Psicoterapia', 'Evaluación Psicométrica', 'Psicología Social y Comunitaria']),
            'reasons_to_study': json.dumps([
                'Te interesa profundamente comprender por qué las personas sienten y actúan como lo hacen.',
                'Tienes una gran capacidad de escucha y vocación de apoyo emocional.',
                'Quieres contribuir a la salud mental y al bienestar de tu comunidad.'
            ]),
            'riasec_r': 0.2, 'riasec_i': 0.8, 'riasec_a': 0.45, 'riasec_s': 0.98, 'riasec_e': 0.55, 'riasec_c': 0.45,
            'skill_logic_math': 0.45, 'skill_verbal': 0.9, 'skill_spatial_creative': 0.45, 'skill_social_leadership': 0.9, 'skill_technical_manual': 0.2, 'skill_scientific_research': 0.85
        },
        {
            'name': 'Ingeniería Mecatrónica y Robótica',
            'slug': 'ingenieria-mecatronica-robotica',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-robot',
            'short_description': 'Integra mecánica, electrónica, control y computación para construir robots inteligentes, automatización industrial y drones.',
            'full_description': 'Combina la mecánica de precisión, la electrónica avanzada y la programación de microcontroladores para concebir sistemas autónomos, brazos robóticos industriales, vehículos no tripulados y prótesis biónicas.',
            'duration_semesters': 10,
            'degree_title': 'Ingeniero/a Mecatrónico/a',
            'labor_market': json.dumps(['Industria automotriz, aeroespacial y de automatización', 'Plantas de manufactura inteligente y robótica', 'Empresas de dispositivos médicos y biomédicos', 'Centros de investigación en inteligencia artificial aplicada', 'Desarrollo de drones y sistemas autónomos']),
            'key_skills': json.dumps(['Diseño Mecánico en 3D (CAD/CAM)', 'Electrónica y Microcontroladores', 'Programación de Sistemas Embebidos', 'Sistemas de Control y Sensores', 'Integración Multidisciplinaria']),
            'typical_subjects': json.dumps(['Cinemática y Dinámica de Robots', 'Circuitos Electrónicos y Microprocesadores', 'Control Automático y Automatismos', 'Diseño de Elementos de Máquinas', 'Visión Artificial y Sensores']),
            'reasons_to_study': json.dumps([
                'Te fascina construir robots, circuitos y mecanismos físicos inteligentes.',
                'Te encanta desarmar tecnología y entender cómo se mueve cada componente.',
                'Quieres estar a la vanguardia de la automatización y el hardware del futuro.'
            ]),
            'riasec_r': 0.95, 'riasec_i': 0.9, 'riasec_a': 0.35, 'riasec_s': 0.25, 'riasec_e': 0.45, 'riasec_c': 0.65,
            'skill_logic_math': 0.9, 'skill_verbal': 0.45, 'skill_spatial_creative': 0.85, 'skill_social_leadership': 0.4, 'skill_technical_manual': 0.95, 'skill_scientific_research': 0.85
        },
        {
            'name': 'Arquitectura y Urbanismo',
            'slug': 'arquitectura-urbanismo',
            'category': 'Arte y Diseño',
            'icon': 'fa-solid fa-compass-drafting',
            'short_description': 'Diseña espacios habitables, edificios sostenibles y ciudades modernas fusionando arte, funcionalidad e ingeniería.',
            'full_description': 'La Arquitectura es la disciplina que proyecta y edifica el hábitat humano. Combina estética, estructura, sostenibilidad ambiental y planificación urbana para transformar el paisaje de las ciudades.',
            'duration_semesters': 10,
            'degree_title': 'Arquitecto/a',
            'labor_market': json.dumps(['Estudios de arquitectura y constructoras', 'Desarrolladoras inmobiliarias y diseño de interiores', 'Planificación urbana municipal y obras públicas', 'Restauración del patrimonio histórico', 'Consultoría en arquitectura bioclimática']),
            'key_skills': json.dumps(['Diseño Espacial y Modelado 3D / BIM', 'Sensibilidad Estética y Compositiva', 'Comprensión Estructural y Constructiva', 'Gestión de Proyectos y Presupuestos', 'Sostenibilidad y Conciencia Ambiental']),
            'typical_subjects': json.dumps(['Taller de Diseño Arquitectónico', 'Estructuras e Instalaciones en Edificaciones', 'Historia y Teoría de la Arquitectura', 'Urbanismo y Territorio', 'Modelado Digital y Representación BIM']),
            'reasons_to_study': json.dumps([
                'Te gusta plasmar tus ideas en dibujos, maquetas y modelos tridimensionales.',
                'Disfrutas crear espacios cómodos, bellos y útiles para las personas.',
                'Combinas una mente artística con el interés por la construcción real.'
            ]),
            'riasec_r': 0.7, 'riasec_i': 0.65, 'riasec_a': 0.95, 'riasec_s': 0.4, 'riasec_e': 0.65, 'riasec_c': 0.6,
            'skill_logic_math': 0.75, 'skill_verbal': 0.6, 'skill_spatial_creative': 0.98, 'skill_social_leadership': 0.6, 'skill_technical_manual': 0.8, 'skill_scientific_research': 0.6
        },
        {
            'name': 'Derecho y Ciencias Jurídicas',
            'slug': 'derecho-ciencias-juridicas',
            'category': 'Ciencias Sociales y Humanidades',
            'icon': 'fa-solid fa-scale-balanced',
            'short_description': 'Defiende la justicia, interpreta las leyes, asesora a personas y organizaciones y resuelve disputas legales.',
            'full_description': 'El Derecho forma profesionales con sólida formación ética y jurídica capaces de litigar, asesorar a empresas, redactar normas y velar por el cumplimiento de los derechos humanos y el ordenamiento constitucional.',
            'duration_semesters': 10,
            'degree_title': 'Abogado/a de los Tribunales y Juzgados de la República',
            'labor_market': json.dumps(['Bufetes de abogados y despachos jurídicos', 'Poder judicial, fiscalías y tribunales de justicia del Ecuador', 'Asesoría legal corporativa en empresas privadas', 'Organismos internacionales y derechos humanos', 'Sector público, ministerios y diplomacia']),
            'key_skills': json.dumps(['Argumentación Jurídica y Oratoria', 'Comprensión Lectora y Análisis Normativo', 'Negociación y Resolución de Conflictos', 'Pensamiento Crítico y Ética', 'Redacción de Contratos y Dictámenes']),
            'typical_subjects': json.dumps(['Derecho Constitucional y Derechos Fundamentales', 'Derecho Civil y Contratos', 'Derecho Penal y Procesal', 'Derecho Corporativo y Mercantil', 'Argumentación y Litigación Oral']),
            'reasons_to_study': json.dumps([
                'Tienes un alto sentido de la justicia y te gusta defender tus argumentos con pruebas.',
                'Disfrutas de la lectura, el debate estructurado y la oratoria.',
                'Quieres ser una voz clave en la resolución pacífica de problemas sociales.'
            ]),
            'riasec_r': 0.15, 'riasec_i': 0.7, 'riasec_a': 0.35, 'riasec_s': 0.8, 'riasec_e': 0.92, 'riasec_c': 0.85,
            'skill_logic_math': 0.45, 'skill_verbal': 0.98, 'skill_spatial_creative': 0.35, 'skill_social_leadership': 0.9, 'skill_technical_manual': 0.15, 'skill_scientific_research': 0.85
        },
        {
            'name': 'Biología y Biotecnología',
            'slug': 'biologia-biotecnologia',
            'category': 'Ciencias Exactas y Naturales',
            'icon': 'fa-solid fa-dna',
            'short_description': 'Investiga los seres vivos a nivel genético y ecológico para desarrollar medicinas, alimentos sostenibles y proteger la biodiversidad.',
            'full_description': 'Aplica el método científico y herramientas genéticas y moleculares para comprender los ecosistemas y generar soluciones innovadoras en farmacología, agricultura sostenible, bioenergía y conservación.',
            'duration_semesters': 10,
            'degree_title': 'Biólogo/a / Biotecnólogo/a',
            'labor_market': json.dumps(['Laboratorios farmacéuticos y de bioingeniería', 'Institutos de investigación científica y genética', 'Empresas agroindustriales y de alimentos', 'Áreas protegidas y consultoría ambiental', 'Organizaciones de conservación de fauna y flora']),
            'key_skills': json.dumps(['Técnicas de Laboratorio y Microbiología', 'Genética Molecular y Bioinformática', 'Observación y Trabajo de Campo', 'Análisis Estadístico de Datos Biológicos', 'Rigor Experimental']),
            'typical_subjects': json.dumps(['Biología Celular y Genética Molecular', 'Bioquímica y Enzimología', 'Ecología y Biodiversidad', 'Microbiología e Inmunología', 'Bioinformática y Biotecnología Aplicada']),
            'reasons_to_study': json.dumps([
                'Te fascina la naturaleza, los animales, las plantas o el mundo microscópico.',
                'Te gustaría trabajar en laboratorios de investigación o en expediciones científicas.',
                'Quieres desarrollar curas médicas o proteger el medio ambiente del cambio climático.'
            ]),
            'riasec_r': 0.65, 'riasec_i': 0.98, 'riasec_a': 0.3, 'riasec_s': 0.5, 'riasec_e': 0.3, 'riasec_c': 0.7,
            'skill_logic_math': 0.75, 'skill_verbal': 0.65, 'skill_spatial_creative': 0.5, 'skill_social_leadership': 0.4, 'skill_technical_manual': 0.8, 'skill_scientific_research': 0.98
        },
        {
            'name': 'Marketing Digital y Publicidad',
            'slug': 'marketing-digital-publicidad',
            'category': 'Negocios y Finanzas',
            'icon': 'fa-solid fa-bullhorn',
            'short_description': 'Diseña campañas digitales virales, gestiona redes sociales, analiza el comportamiento del consumidor y posiciona marcas.',
            'full_description': 'Fusiona creatividad publicitaria, psicología del consumidor y analítica de datos en canales digitales para conectar marcas con audiencias de forma innovadora e impulsar las ventas.',
            'duration_semesters': 8,
            'degree_title': 'Licenciado/a en Marketing y Publicidad Digital',
            'labor_market': json.dumps(['Agencias de medios y marketing digital', 'Departamentos de marketing de empresas de consumo masivo', 'Plataformas de e-commerce y startups', 'Empresas de entretenimiento y medios', 'Consultoría en crecimiento de marcas (Growth Hacker)']),
            'key_skills': json.dumps(['Estrategia de Contenidos y Redes Sociales', 'Analítica Web y Métricas de Rendimiento', 'Creatividad y Copywriting Publicitario', 'Campañas de Pauta Digital (Google/Meta Ads)', 'Investigación del Consumidor']),
            'typical_subjects': json.dumps(['Estrategias de Marketing Digital y SEO', 'Comportamiento y Psicología del Consumidor', 'Creatividad Publicitaria y Storytelling', 'Analítica de Datos de Marketing', 'Branding y Gestión de Marcas']),
            'reasons_to_study': json.dumps([
                'Te encantan las redes sociales, las tendencias virales y la comunicación visual.',
                'Disfrutas idear estrategias creativas para promocionar productos y servicios.',
                'Te atrae combinar la creatividad con el análisis de métricas de impacto.'
            ]),
            'riasec_r': 0.2, 'riasec_i': 0.55, 'riasec_a': 0.88, 'riasec_s': 0.7, 'riasec_e': 0.95, 'riasec_c': 0.6,
            'skill_logic_math': 0.6, 'skill_verbal': 0.9, 'skill_spatial_creative': 0.85, 'skill_social_leadership': 0.85, 'skill_technical_manual': 0.5, 'skill_scientific_research': 0.65
        },
        {
            'name': 'Enfermería y Cuidados de la Salud',
            'slug': 'enfermeria-cuidados-salud',
            'category': 'Ciencias de la Salud',
            'icon': 'fa-solid fa-user-nurse',
            'short_description': 'Proporciona atención y cuidado clínico directo y humano a pacientes en todas las etapas de la vida y situaciones críticas.',
            'full_description': 'La Enfermería es una disciplina del cuidado de la salud enfocada en la atención integral, administración de tratamientos, recuperación física y acompañamiento emocional de los pacientes en entornos hospitalarios y comunitarios.',
            'duration_semesters': 8,
            'degree_title': 'Licenciado/a en Enfermería',
            'labor_market': json.dumps(['Hospitales generales y unidades de cuidados intensivos', 'Clínicas quirúrgicas y centros de salud comunitarios', 'Servicios de emergencias médicas y ambulancias', 'Atención domiciliaria y centros geriátricos', 'Programas de salud escolar y preventiva']),
            'key_skills': json.dumps(['Procedimientos Clínicos y Administración de Fármacos', 'Atención Humanizada y Empatía', 'Respuesta en Urgencias y Primeros Auxilios', 'Trabajo en Equipo Multidisciplinario', 'Monitoreo de Signos Vitales']),
            'typical_subjects': json.dumps(['Fundamentos del Cuidado de Enfermería', 'Farmacología y Terapéutica', 'Enfermería Quirúrgica y Cuidados Críticos', 'Salud Materno-Infantil', 'Salud Pública y Comunitaria']),
            'reasons_to_study': json.dumps([
                'Deseas estar en contacto directo y cotidiano cuidando y curando a las personas.',
                'Tienes una vocación servicial infatigable y temple ante emergencias.',
                'Buscas una profesión médica esencial con empleo garantizado a nivel mundial.'
            ]),
            'riasec_r': 0.5, 'riasec_i': 0.75, 'riasec_a': 0.2, 'riasec_s': 0.98, 'riasec_e': 0.35, 'riasec_c': 0.7,
            'skill_logic_math': 0.55, 'skill_verbal': 0.75, 'skill_spatial_creative': 0.35, 'skill_social_leadership': 0.8, 'skill_technical_manual': 0.85, 'skill_scientific_research': 0.75
        },
        {
            'name': 'Ingeniería Civil y Construcción',
            'slug': 'ingenieria-civil-construccion',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-bridge',
            'short_description': 'Calcula, diseña y supervisa la construcción de puentes, carreteras, rascacielos, presas y megaestructuras seguras.',
            'full_description': 'Lidera la concepción, cálculo estructural, gestión y construcción de la infraestructura física indispensable para el desarrollo de la sociedad, aplicando física de materiales y gestión de obras.',
            'duration_semesters': 10,
            'degree_title': 'Ingeniero/a Civil',
            'labor_market': json.dumps(['Empresas constructoras y consultoras de ingeniería', 'Ministerios de obras públicas y transporte', 'Empresas de geotecnia y estudios de suelos', 'Supervisión e interventoría de megaobras', 'Desarrollo de infraestructura hidráulica y vial']),
            'key_skills': json.dumps(['Cálculo Estructural y Resistencia de Materiales', 'Topografía y Mecánica de Suelos', 'Dirección de Obra y Presupuestos', 'Modelado y Diseño Estructural por Computador', 'Gestión de Seguridad en Construcción']),
            'typical_subjects': json.dumps(['Cálculo Diferencial e Integral', 'Mecánica de Estructuras y Concreto Armado', 'Mecánica de Suelos y Cimentaciones', 'Hidráulica y Recursos Hídricos', 'Gestión y Programación de Obras']),
            'reasons_to_study': json.dumps([
                'Te fascina ver cómo se levantan los grandes edificios, puentes y carreteras.',
                'Disfrutas de las matemáticas y la física aplicadas a estructuras reales.',
                'Te gusta alternar el trabajo técnico en oficina con la acción en obras de campo.'
            ]),
            'riasec_r': 0.9, 'riasec_i': 0.85, 'riasec_a': 0.3, 'riasec_s': 0.3, 'riasec_e': 0.65, 'riasec_c': 0.8,
            'skill_logic_math': 0.95, 'skill_verbal': 0.5, 'skill_spatial_creative': 0.8, 'skill_social_leadership': 0.65, 'skill_technical_manual': 0.85, 'skill_scientific_research': 0.75
        },
        {
            'name': 'Periodismo y Comunicación Social',
            'slug': 'periodismo-comunicacion-social',
            'category': 'Ciencias Sociales y Humanidades',
            'icon': 'fa-solid fa-newspaper',
            'short_description': 'Investiga hechos, narra historias, produce noticias y contenidos para televisión, radio, prensa escrita y medios digitales.',
            'full_description': 'Forma comunicadores éticos e investigadores con capacidad para informar verazmente a la opinión pública mediante reportajes, crónicas, podcasts, producción audiovisual y periodismo de datos.',
            'duration_semesters': 8,
            'degree_title': 'Licenciado/a en Comunicación Social / Periodista',
            'labor_market': json.dumps(['Canales de televisión, radio y prensa escrita', 'Medios nativos digitales y plataformas de podcast', 'Departamentos de prensa y relaciones públicas corporativas', 'Periodismo de investigación independiente', 'Producción de contenidos audiovisuales y documentales']),
            'key_skills': json.dumps(['Investigación y Verificación de Fuentes', 'Redacción Periodística y Storytelling', 'Locución y Presentación ante Cámaras', 'Edición de Audio y Video', 'Pensamiento Crítico y Análisis Social']),
            'typical_subjects': json.dumps(['Géneros Periodísticos y Redacción de Noticias', 'Producción Audiovisual y Radiofónica', 'Periodismo de Investigación y Datos', 'Ética de la Comunicación y Legislación de Prensa', 'Opinión Pública y Sociología']),
            'reasons_to_study': json.dumps([
                'Eres una persona sumamente curiosa, informada y apasionada por la verdad.',
                'Te encanta redactar, entrevistar personas y contar historias impactantes.',
                'Quieres dar voz a los hechos y defender la libertad de expresión.'
            ]),
            'riasec_r': 0.25, 'riasec_i': 0.75, 'riasec_a': 0.85, 'riasec_s': 0.8, 'riasec_e': 0.85, 'riasec_c': 0.45,
            'skill_logic_math': 0.35, 'skill_verbal': 0.98, 'skill_spatial_creative': 0.75, 'skill_social_leadership': 0.8, 'skill_technical_manual': 0.5, 'skill_scientific_research': 0.85
        },
        {
            'name': 'Economía y Finanzas Cuantitativas',
            'slug': 'economia-finanzas',
            'category': 'Negocios y Finanzas',
            'icon': 'fa-solid fa-coins',
            'short_description': 'Analiza el funcionamiento de los mercados, la inflación, las inversiones financieras y formula políticas económicas de impacto.',
            'full_description': 'Aplica modelos matemáticos y estadísticos para entender la asignación de recursos, pronosticar tendencias de mercado, gestionar portafolios de inversión y diseñar políticas públicas y monetarias.',
            'duration_semesters': 8,
            'degree_title': 'Economista / Licenciado/a en Finanzas',
            'labor_market': json.dumps(['Bancos centrales y ministerios de hacienda', 'Bancos de inversión y bolsas de valores', 'Organismos multilaterales (FMI, Banco Mundial)', 'Consultoras económicas y de riesgo financiero', 'Grandes corporaciones multinacionales']),
            'key_skills': json.dumps(['Modelación Econométrica y Estadística', 'Análisis Macroeconómico y Microeconómico', 'Evaluación de Inversiones y Riesgos', 'Manejo de Bases de Datos Económicas', 'Pensamiento Crítico Cuantitativo']),
            'typical_subjects': json.dumps(['Microeconomía y Teoría de Juegos', 'Macroeconomía y Política Monetaria', 'Econometría y Análisis de Series Temporales', 'Finanzas Corporativas y Mercados de Capitales', 'Economía Internacional y Comercio']),
            'reasons_to_study': json.dumps([
                'Te apasiona entender cómo se mueve el dinero, el comercio y la riqueza mundial.',
                'Disfrutas de las matemáticas aplicadas a problemas sociales y financieros reales.',
                'Quieres asesorar a gobiernos o corporaciones en decisiones estratégicas de inversión.'
            ]),
            'riasec_r': 0.2, 'riasec_i': 0.92, 'riasec_a': 0.25, 'riasec_s': 0.45, 'riasec_e': 0.88, 'riasec_c': 0.9,
            'skill_logic_math': 0.95, 'skill_verbal': 0.75, 'skill_spatial_creative': 0.4, 'skill_social_leadership': 0.7, 'skill_technical_manual': 0.3, 'skill_scientific_research': 0.9
        },
        {
            'name': 'Gastronomía y Artes Culinarias',
            'slug': 'gastronomia-artes-culinarias',
            'category': 'Arte y Diseño',
            'icon': 'fa-solid fa-utensils',
            'short_description': 'Crea experiencias culinarias excepcionales, domina técnicas de alta cocina y gestiona restaurantes y negocios gastronómicos.',
            'full_description': 'Combina técnicas culinarias de vanguardia, química de los alimentos, creatividad sensorial y gestión de restaurantes para convertir la alimentación en una experiencia artística de alto nivel.',
            'duration_semesters': 8,
            'degree_title': 'Chef Ejecutivo / Licenciado/a en Gastronomía',
            'labor_market': json.dumps(['Restaurantes de alta cocina y hoteles internacionales', 'Emprendimientos gastronómicos y catering', 'Cruceros y cadenas de hospitalidad', 'Crítica culinaria y desarrollo de nuevos productos alimenticios', 'Consultoría en menú y asesoría gastronómica']),
            'key_skills': json.dumps(['Técnicas Culinarias de Alta Cocina', 'Creatividad Sensorial y Emplatado', 'Gestión de Costos y Cocinas Profesionales', 'Higiene y Seguridad Alimentaria (HACCP)', 'Trabajo Rápido y Bajo Presión']),
            'typical_subjects': json.dumps(['Cocina Internacional y Vanguardista', 'Pastelería y Panadería Profesional', 'Enología, Maridaje y Sommelier', 'Gestión y Administración de Alimentos y Bebidas', 'Química Culinaria y Nutrición']),
            'reasons_to_study': json.dumps([
                'Te apasiona la cocina, experimentar con sabores y crear platos memorables.',
                'Tienes destreza manual y disfrutas de un ambiente de trabajo dinámico y enérgico.',
                'Sueñas con abrir tu propio restaurante o liderar cocinas prestigiosas.'
            ]),
            'riasec_r': 0.85, 'riasec_i': 0.4, 'riasec_a': 0.95, 'riasec_s': 0.5, 'riasec_e': 0.8, 'riasec_c': 0.5,
            'skill_logic_math': 0.4, 'skill_verbal': 0.55, 'skill_spatial_creative': 0.9, 'skill_social_leadership': 0.75, 'skill_technical_manual': 0.95, 'skill_scientific_research': 0.4
        },
        {
            'name': 'Educación y Pedagogía',
            'slug': 'educacion-pedagogia',
            'category': 'Ciencias Sociales y Humanidades',
            'icon': 'fa-solid fa-chalkboard-user',
            'short_description': 'Forma a las nuevas generaciones mediante metodologías innovadoras de enseñanza, didáctica y desarrollo infantil y juvenil.',
            'full_description': 'Diseña planes educativos, aplica psicopedagogía y tecnologías educativas para inspirar y formar el conocimiento y carácter de niños, adolescentes y universitarios.',
            'duration_semesters': 10,
            'degree_title': 'Licenciado/a en Educación / Pedagogo/a',
            'labor_market': json.dumps(['Colegios públicos y privados de todos los niveles', 'Universidades e institutos técnicos', 'Diseño de contenidos para plataformas EdTech', 'Asesoría y tutoría pedagógica personalizada', 'Ministerios de educación y formulación de políticas educativas']),
            'key_skills': json.dumps(['Didáctica y Métodos de Aprendizaje Activo', 'Paciencia, Empatía y Manejo de Grupo', 'Diseño Curricular y Evaluación Formativa', 'Uso de Tecnologías Educativas (EdTech)', 'Oratoria y Comunicación Adaptada']),
            'typical_subjects': json.dumps(['Teorías del Aprendizaje y Pedagogía Contemporánea', 'Psicología Educativa y Neuroeducación', 'Didáctica Especializada', 'Tecnología Aplicada a la Educación', 'Evaluación del Aprendizaje e Inclusión Escolar']),
            'reasons_to_study': json.dumps([
                'Sientes satisfacción al explicar temas y ver cómo otros aprenden gracias a ti.',
                'Deseas dejar una huella positiva en la formación de niños y jóvenes.',
                'Crees firmemente que la educación es la herramienta más poderosa para cambiar la sociedad.'
            ]),
            'riasec_r': 0.2, 'riasec_i': 0.7, 'riasec_a': 0.6, 'riasec_s': 0.99, 'riasec_e': 0.6, 'riasec_c': 0.6,
            'skill_logic_math': 0.5, 'skill_verbal': 0.95, 'skill_spatial_creative': 0.65, 'skill_social_leadership': 0.95, 'skill_technical_manual': 0.4, 'skill_scientific_research': 0.75
        },
        {
            'name': 'Ingeniería Ambiental y Sostenibilidad',
            'slug': 'ingenieria-ambiental-sostenibilidad',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-seedling',
            'short_description': 'Desarrolla tecnologías y procesos para mitigar la contaminación, gestionar recursos hídricos y liderar la transición ecológica.',
            'full_description': 'Aplica conocimientos de ciencias ambientales e ingeniería para solucionar problemas de contaminación del agua, aire y suelo, tratamiento de residuos y diseño de procesos industriales ecológicos.',
            'duration_semesters': 10,
            'degree_title': 'Ingeniero/a Ambiental',
            'labor_market': json.dumps(['Empresas de energías renovables y tratamiento de aguas', 'Consultoría de impacto ambiental y auditorías verdes', 'Industrias con programas de sostenibilidad (ESG)', 'Entidades gubernamentales de protección ambiental', 'Organizaciones no gubernamentales ambientales']),
            'key_skills': json.dumps(['Evaluación de Impacto Ambiental', 'Tratamiento de Aguas y Gestión de Residuos', 'Monitoreo de Calidad de Aire y Suelos', 'Normativa Ambiental Internacional', 'Diseño de Procesos Sostenibles']),
            'typical_subjects': json.dumps(['Química Ambiental y Toxicología', 'Hidrología y Tratamiento de Aguas Residuales', 'Gestión Integral de Residuos Sólidos', 'Energías Renovables y Huella de Carbono', 'Legislación y Auditoría Ambiental']),
            'reasons_to_study': json.dumps([
                'Te preocupa el cambio climático y quieres aportar soluciones técnicas reales.',
                'Disfrutas de las ciencias naturales y la ingeniería aplicada.',
                'Te gusta alternar el trabajo científico con trabajo de campo en ecosistemas.'
            ]),
            'riasec_r': 0.75, 'riasec_i': 0.92, 'riasec_a': 0.35, 'riasec_s': 0.65, 'riasec_e': 0.5, 'riasec_c': 0.7,
            'skill_logic_math': 0.85, 'skill_verbal': 0.65, 'skill_spatial_creative': 0.6, 'skill_social_leadership': 0.6, 'skill_technical_manual': 0.8, 'skill_scientific_research': 0.92
        },
        {
            'name': 'Contabilidad Pública y Auditoría',
            'slug': 'contabilidad-auditoria',
            'category': 'Negocios y Finanzas',
            'icon': 'fa-solid fa-file-invoice-dollar',
            'short_description': 'Garantiza la transparencia financiera, elabora estados contables, audita procesos y diseña estrategias tributarias.',
            'full_description': 'Profesionales expertos en normas internacionales de información financiera (NIIF), auditoría forense, control interno y tributación para asegurar la solidez y cumplimiento legal de las empresas.',
            'duration_semesters': 8,
            'degree_title': 'Licenciado/a en Contabilidad y Auditoría (CPA)',
            'labor_market': json.dumps(['Firmas de auditoría internacional (Big Four)', 'Departamentos contables y tributarios corporativos', 'Servicio de Rentas Internas (SRI)', 'Peritaje contable y auditoría forense judicial', 'Asesoría contable y tributaria independiente']),
            'key_skills': json.dumps(['Normas Contables Internacionales (NIIF)', 'Auditoría y Control Interno', 'Legislación Tributaria e Impuestos', 'Precisión en el Manejo Numérico y de Libros', 'Sistemas ERP y Software Contable']),
            'typical_subjects': json.dumps(['Contabilidad Financiera y de Costos', 'Auditoría de Estados Financieros', 'Derecho Tributario y Fiscal', 'Sistemas de Información Contable', 'Finanzas y Presupuestos Empresariales']),
            'reasons_to_study': json.dumps([
                'Eres una persona muy ordenada, metódica y atenta a los detalles numéricos.',
                'Te gusta la estabilidad laboral y ser una pieza fundamental en cualquier empresa.',
                'Prefieres trabajar con reglas claras, procesos definidos y cuentas exactas.'
            ]),
            'riasec_r': 0.3, 'riasec_i': 0.7, 'riasec_a': 0.15, 'riasec_s': 0.4, 'riasec_e': 0.7, 'riasec_c': 0.98,
            'skill_logic_math': 0.88, 'skill_verbal': 0.6, 'skill_spatial_creative': 0.25, 'skill_social_leadership': 0.55, 'skill_technical_manual': 0.4, 'skill_scientific_research': 0.7
        },
        {
            'name': 'Ingeniería en Ciberseguridad y Seguridad de la Información',
            'slug': 'ingenieria-ciberseguridad',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-shield-halved',
            'short_description': 'Protege infraestructuras digitales, previene ciberataques, implementa criptografía y lidera la defensa de datos confidenciales.',
            'full_description': 'La Ingeniería en Ciberseguridad forma profesionales de vanguardia capacitados para detectar vulnerabilidades, ejecutar pruebas de penetración (Hacking Ético), diseñar arquitecturas defensivas de redes y responder ante incidentes de ciberseguridad en banca, telecomunicaciones e industrias críticas del Ecuador y el mundo.',
            'duration_semesters': 9,
            'degree_title': 'Ingeniero/a en Ciberseguridad (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Centros de Operaciones de Seguridad (SOC) y CERT', 'Sector bancario, financiero y pasarelas de pago', 'Empresas de telecomunicaciones y defensa de infraestructuras críticas', 'Consultoría en auditoría informática y Hacking Ético', 'Entidades de seguridad estatal y ciberdefensa']),
            'key_skills': json.dumps(['Análisis de Vulnerabilidades y Hacking Ético', 'Criptografía y Seguridad en Redes', 'Forense Digital y Respuesta a Incidentes', 'Normativas ISO 27001 y Gobierno de Datos', 'Programación Segura y Scripting']),
            'typical_subjects': json.dumps(['Seguridad en Redes y Sistemas Operativos', 'Criptografía Aplicada y Autenticación', 'Hacking Ético y Test de Penetración', 'Análisis Forense Digital y Malware', 'Gestión de Riesgos y Cumplimiento Normativo']),
            'reasons_to_study': json.dumps([
                'Te fascina proteger información y descubrir cómo funcionan los ataques y defensas digitales.',
                'Disfrutas del pensamiento analítico, la investigación metódica y los desafíos lógicos.',
                'Buscas una carrera moderna de altísima demanda global y excelente remuneración.'
            ]),
            'riasec_r': 0.70, 'riasec_i': 0.95, 'riasec_a': 0.35, 'riasec_s': 0.30, 'riasec_e': 0.60, 'riasec_c': 0.90,
            'skill_logic_math': 0.92, 'skill_verbal': 0.60, 'skill_spatial_creative': 0.55, 'skill_social_leadership': 0.50, 'skill_technical_manual': 0.88, 'skill_scientific_research': 0.88
        },
        {
            'name': 'Ingeniería Biomédica y Bioingeniería',
            'slug': 'ingenieria-biomedica-bioingenieria',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-heart-pulse',
            'short_description': 'Diseña prótesis biónicas, equipos médicos hospitalarios, nanotecnología y software de diagnóstico clínico para salvar vidas.',
            'full_description': 'La Ingeniería Biomédica fusiona la medicina, la biología y la ingeniería (electrónica, mecánica y computación) para desarrollar tecnologías sanitarias avanzadas: resonadores, marcapasos, órganos artificiales, prótesis inteligentes y sistemas de telemedicina de última generación.',
            'duration_semesters': 10,
            'degree_title': 'Ingeniero/a Biomédico/a (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Hospitales de alta complejidad y centros de diagnóstico', 'Industria de fabricación de dispositivos médicos e implantes', 'Empresas de desarrollo de prótesis y biónica', 'Laboratorios de investigación en biomateriales y genética', 'Empresas de software de telemedicina e imágenes médicas']),
            'key_skills': json.dumps(['Diseño de Dispositivos Médicos y Biomecánica', 'Procesamiento de Señales e Imágenes Biomédicas', 'Electrónica Médica y Sensores Fisiológicos', 'Biomateriales y Tejidos Artificiales', 'Mantenimiento y Gestión de Tecnología Hospitalaria']),
            'typical_subjects': json.dumps(['Fisiología y Anatomía para Ingenieros', 'Instrumentación y Sensores Biomédicos', 'Biomecánica y Prótesis Biónicas', 'Procesamiento Digital de Señales e Imágenes Médicas', 'Ingeniería Clínica y Seguridad Hospitalaria']),
            'reasons_to_study': json.dumps([
                'Te apasiona combinar la tecnología y la ingeniería con la medicina y el cuidado humano.',
                'Quieres inventar dispositivos y prótesis que mejoren directamente la vida de pacientes.',
                'Disfrutas tanto de las ciencias biológicas como de la electrónica y la programación.'
            ]),
            'riasec_r': 0.85, 'riasec_i': 0.98, 'riasec_a': 0.40, 'riasec_s': 0.80, 'riasec_e': 0.45, 'riasec_c': 0.70,
            'skill_logic_math': 0.90, 'skill_verbal': 0.65, 'skill_spatial_creative': 0.75, 'skill_social_leadership': 0.70, 'skill_technical_manual': 0.92, 'skill_scientific_research': 0.95
        },
        {
            'name': 'Inteligencia Artificial y Ciencia de Datos',
            'slug': 'inteligencia-artificial-ciencia-datos',
            'category': 'Ingeniería y Tecnología',
            'icon': 'fa-solid fa-brain',
            'short_description': 'Construye modelos predictivos, redes neuronales profundas, procesamiento del lenguaje natural y visión computacional.',
            'full_description': 'Especialidad moderna enfocada en el diseño de algoritmos de aprendizaje automático (Machine Learning), procesamiento de Big Data, análisis predictivo y sistemas autónomos para transformar la salud, industria y finanzas.',
            'duration_semesters': 9,
            'degree_title': 'Ingeniero/a en Inteligencia Artificial y Ciencia de Datos',
            'labor_market': json.dumps(['Empresas de tecnología e IA generativa', 'Sector bancario y detección de fraudes', 'Consultoría en analítica avanzada y Big Data', 'Salud digital y biociencias computacionales', 'Investigación académica y centros de innovación']),
            'key_skills': json.dumps(['Machine Learning y Deep Learning', 'Matemáticas y Estadística Avanzada', 'Python, PyTorch y Arquitecturas de IA', 'Ingeniería de Datos y Big Data', 'Ética y Gobernanza de Algoritmos de IA']),
            'typical_subjects': json.dumps(['Modelos de Machine Learning y Redes Neuronales', 'Procesamiento de Lenguaje Natural (NLP)', 'Visión Artificial y Robótica Inteligente', 'Álgebra Lineal y Probabilidad para IA', 'Bases de Datos Masivas y Cloud Computing']),
            'reasons_to_study': json.dumps([
                'Te entusiasma el auge de la inteligencia artificial y quieres ser quien desarrolle los modelos del futuro.',
                'Disfrutas encontrar patrones ocultos en grandes cantidades de datos.',
                'Buscas una carrera en la frontera de la innovación tecnológica mundial.'
            ]),
            'riasec_r': 0.60, 'riasec_i': 0.99, 'riasec_a': 0.50, 'riasec_s': 0.35, 'riasec_e': 0.65, 'riasec_c': 0.85,
            'skill_logic_math': 0.98, 'skill_verbal': 0.60, 'skill_spatial_creative': 0.65, 'skill_social_leadership': 0.50, 'skill_technical_manual': 0.80, 'skill_scientific_research': 0.98
        },
        {
            'name': 'Medicina Veterinaria y Zootecnia',
            'slug': 'medicina-veterinaria-zootecnia',
            'category': 'Ciencias Agropecuarias y Alimentos',
            'icon': 'fa-solid fa-paw',
            'short_description': 'Diagnostica y trata enfermedades animales, lidera la salud pública (zoonosis), el bienestar animal y la producción pecuaria sostenible.',
            'full_description': 'Forma médicos veterinarios y zootecnistas con sólida base clínica, quirúrgica y de manejo pecuario, capacitados para el cuidado de animales de compañía, fauna silvestre, ganado bovino, porcino y avícola en el Ecuador.',
            'duration_semesters': 10,
            'degree_title': 'Médico/a Veterinario/a Zootecnista (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Clínicas y hospitales veterinarios de animales menores y mayores', 'Haciendas ganaderas, avícolas y centros de producción pecuaria', 'Agencias de regulación y control fito y zoosanitario (AGROCALIDAD)', 'Zoológicos, reservas ecológicas y centros de rescate de fauna', 'Industria farmacéutica y nutrición animal']),
            'key_skills': json.dumps(['Diagnóstico Clínico y Cirugía Veterinaria', 'Manejo Pecuario y Bienestar Animal', 'Epidemiología y Salud Pública (Zoonosis)', 'Nutrición y Reproducción Animal', 'Farmacología Veterinaria']),
            'typical_subjects': json.dumps(['Anatomía y Fisiología Veterinaria', 'Patología y Microbiología Animal', 'Cirugía y Anestesiología Veterinaria', 'Producción de Rumiantes y Monogástricos', 'Epidemiología y Salud Pública Veterinaria']),
            'reasons_to_study': json.dumps([
                'Sientes una profunda empatía y vocación por el cuidado médico y bienestar de los animales.',
                'Te gusta combinar el trabajo clínico con labores en entornos rurales y haciendas.',
                'Quieres proteger la salud pública previniendo enfermedades transmisibles de animales a personas.'
            ]),
            'riasec_r': 0.90, 'riasec_i': 0.95, 'riasec_a': 0.25, 'riasec_s': 0.85, 'riasec_e': 0.40, 'riasec_c': 0.60,
            'skill_logic_math': 0.65, 'skill_verbal': 0.65, 'skill_spatial_creative': 0.50, 'skill_social_leadership': 0.70, 'skill_technical_manual': 0.90, 'skill_scientific_research': 0.92
        },
        {
            'name': 'Ingeniería Agronómica y Agricultura Sostenible',
            'slug': 'ingenieria-agronomica',
            'category': 'Ciencias Agropecuarias y Alimentos',
            'icon': 'fa-solid fa-wheat-awn',
            'short_description': 'Optimiza la producción de cultivos, aplica agricultura de precisión, gestiona suelos y lidera la exportación agrícola sostenible.',
            'full_description': 'Forma profesionales líderes en la producción sostenible de alimentos y cultivos agroexportadores clave del Ecuador (banano, cacao fino de aroma, flores, café, palma y hortalizas), integrando biotecnología vegetal, riego tecnificado y manejo integrado de plagas.',
            'duration_semesters': 9,
            'degree_title': 'Ingeniero/a Agrónomo/a (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Empresas agroexportadoras (bananeras, cacaoteras, florícolas)', 'Plantaciones e industrias agrícolas tecnificadas', 'Organismos de investigación agrícola (INIAP, AGROCALIDAD)', 'Comercializadoras de insumos agrícolas y biotecnología vegetal', 'Consultoría técnica en riego y manejo de suelos']),
            'key_skills': json.dumps(['Manejo Integrado de Plagas y Enfermedades (MIP)', 'Diseño de Riego Tecnificado y Nutrición Vegetal', 'Agricultura de Precisión y Drones Agrícolas', 'Gestión de Suelos y Fertilidad', 'Certificaciones Agrícolas Internacionales (GlobalGAP)']),
            'typical_subjects': json.dumps(['Fisiología Vegetal y Edafología (Suelos)', 'Entomología y Fitopatología Agrícola', 'Sistemas de Riego y Drenaje', 'Genética y Mejoramiento de Cultivos', 'Agroecología y Cultivos Tropicales']),
            'reasons_to_study': json.dumps([
                'Te apasiona el campo, las plantas y el contacto directo con la naturaleza.',
                'Quieres transformar la agricultura con tecnología de precisión y sostenibilidad ambiental.',
                'Buscas una profesión fundamental para la economía y exportación del Ecuador.'
            ]),
            'riasec_r': 0.95, 'riasec_i': 0.90, 'riasec_a': 0.30, 'riasec_s': 0.50, 'riasec_e': 0.65, 'riasec_c': 0.75,
            'skill_logic_math': 0.80, 'skill_verbal': 0.55, 'skill_spatial_creative': 0.65, 'skill_social_leadership': 0.65, 'skill_technical_manual': 0.90, 'skill_scientific_research': 0.90
        },
        {
            'name': 'Ingeniería en Alimentos y Agroindustria',
            'slug': 'ingenieria-alimentos-agroindustria',
            'category': 'Ciencias Agropecuarias y Alimentos',
            'icon': 'fa-solid fa-jar',
            'short_description': 'Transforma materias primas en alimentos seguros, nutritivos y procesados, garantizando calidad, conservación e inocuidad alimentaria.',
            'full_description': 'Aplica la química, microbiología e ingeniería de procesos para diseñar nuevos productos alimenticios, optimizar cadenas de conservación y empaque, y asegurar los más altos estándares de calidad (HACCP, BPM) en la industria de bebidas, lácteos, cárnicos y conservas.',
            'duration_semesters': 9,
            'degree_title': 'Ingeniero/a en Alimentos / Agroindustrial (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Industrias de alimentos y bebidas (lácteos, confitería, cárnicos, cervecerías)', 'Plantas procesadoras de alimentos para consumo nacional y exportación', 'Laboratorios de control de calidad e inocuidad alimentaria (ARCSA)', 'Empresas de investigación y desarrollo de nuevos productos (I+D)', 'Supermercados y cadenas de distribución de alimentos']),
            'key_skills': json.dumps(['Química y Microbiología de Alimentos', 'Diseño de Procesos Industriales y Conservación', 'Control de Calidad e Inocuidad (BPM, HACCP, FSSC 22000)', 'Desarrollo Sensorial y Formulación Nutricional', 'Tecnología de Empaques y Vida Útil']),
            'typical_subjects': json.dumps(['Bioquímica y Análisis de Alimentos', 'Microbiología y Toxicología Alimentaria', 'Operaciones Unitarias e Ingeniería de Procesos', 'Tecnología de Lácteos, Cárnicos y Frutas', 'Sistemas de Gestión de Calidad e Inocuidad']),
            'reasons_to_study': json.dumps([
                'Te fascina la ciencia de los alimentos, la nutrición y la química culinaria e industrial.',
                'Disfrutas del trabajo de laboratorio combinado con plantas de procesamiento industrial.',
                'Quieres garantizar que los alimentos que consumen millones de personas sean sanos y seguros.'
            ]),
            'riasec_r': 0.80, 'riasec_i': 0.92, 'riasec_a': 0.40, 'riasec_s': 0.50, 'riasec_e': 0.60, 'riasec_c': 0.88,
            'skill_logic_math': 0.85, 'skill_verbal': 0.60, 'skill_spatial_creative': 0.60, 'skill_social_leadership': 0.60, 'skill_technical_manual': 0.88, 'skill_scientific_research': 0.92
        },
        {
            'name': 'Ingeniería Agropecuaria y Agronegocios',
            'slug': 'ingenieria-agropecuaria-agronegocios',
            'category': 'Ciencias Agropecuarias y Alimentos',
            'icon': 'fa-solid fa-tractor',
            'short_description': 'Integra la producción animal y vegetal con la administración estratégica, comercialización y exportación agrícola.',
            'full_description': 'Combina las ciencias agrícolas y pecuarias con la gestión empresarial para administrar fincas, optimizar cadenas de suministro agroalimentarias, formular proyectos de inversión rural y abrir canales de comercio exterior.',
            'duration_semesters': 9,
            'degree_title': 'Ingeniero/a Agropecuario/a y de Agronegocios (Tercer Nivel de Grado)',
            'labor_market': json.dumps(['Empresas agroindustriales y de agronegocios', 'Administración gerencial de fincas y haciendas integradas', 'Organizaciones de comercio justo y exportación agropecuaria', 'Banca de desarrollo rural y evaluación de créditos agrícolas', 'Ministerio de Agricultura y Ganadería (MAG)']),
            'key_skills': json.dumps(['Gestión Estratégica de Fincas y Agronegocios', 'Cadenas de Suministro y Logística Agropecuaria', 'Producción Agrícola y Pecuaria Sostenible', 'Finanzas y Proyectos de Inversión Rural', 'Comercialización y Exportación de Commodities']),
            'typical_subjects': json.dumps(['Administración y Economía de Agronegocios', 'Sistemas de Producción Agrícola y Animal', 'Comercio Exterior y Logística Agropecuaria', 'Formulación y Evaluación de Proyectos Agropecuarios', 'Manejo Sostenible de Recursos Naturales']),
            'reasons_to_study': json.dumps([
                'Te apasiona combinar la vida del campo con los negocios, finanzas y exportación.',
                'Quieres liderar la modernización y rentabilidad de empresas agrícolas y ganaderas.',
                'Tienes visión emprendedora y liderazgo para proyectos rurales sostenibles.'
            ]),
            'riasec_r': 0.85, 'riasec_i': 0.75, 'riasec_a': 0.25, 'riasec_s': 0.60, 'riasec_e': 0.90, 'riasec_c': 0.80,
            'skill_logic_math': 0.80, 'skill_verbal': 0.75, 'skill_spatial_creative': 0.50, 'skill_social_leadership': 0.90, 'skill_technical_manual': 0.80, 'skill_scientific_research': 0.75
        }
    ]

    for c in careers:
        cursor.execute('''
        INSERT INTO careers (
            name, slug, category, icon, short_description, full_description,
            duration_semesters, degree_title, labor_market, key_skills,
            typical_subjects, reasons_to_study, riasec_r, riasec_i, riasec_a,
            riasec_s, riasec_e, riasec_c, skill_logic_math, skill_verbal,
            skill_spatial_creative, skill_social_leadership, skill_technical_manual,
            skill_scientific_research
        ) VALUES (
            :name, :slug, :category, :icon, :short_description, :full_description,
            :duration_semesters, :degree_title, :labor_market, :key_skills,
            :typical_subjects, :reasons_to_study, :riasec_r, :riasec_i, :riasec_a,
            :riasec_s, :riasec_e, :riasec_c, :skill_logic_math, :skill_verbal,
            :skill_spatial_creative, :skill_social_leadership, :skill_technical_manual,
            :skill_scientific_research
        )
        ''', c)
    conn.commit()
