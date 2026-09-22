# 🎓 OrientaBachiller - Sistema de Orientación Vocacional Universitaria (Ecuador)

Sistema web integral desarrollado bajo la arquitectura **MVC (Modelo - Vista - Controlador)** en **Python / Flask**, adaptado específicamente al **Sistema Educativo del Ecuador (Bachillerato General Unificado - BGU)** para orientar y asesorar a los estudiantes en la selección de su carrera de Tercer Nivel (Universidades, Escuelas Politécnicas e Institutos Superiores).

---

## 🇪🇨 Adaptación al Sistema Educativo Ecuatoriano

- **Niveles de Estudio BGU**:
  - `3.° de Bachillerato (3ero BGU - Graduando)`
  - `2.° de Bachillerato (2do BGU)`
  - `1.° de Bachillerato (1ero BGU)`
  - `Bachillerato Técnico (BT)`
  - `Bachillerato Internacional (BI)`
  - `Bachiller Graduado (Aspirante a la Educación Superior / Proceso SENESCYT)`
- **Departamento de Consejería Estudiantil (DECE)**: Panel para orientadores escolares y formato oficial de informe con firmas institucionales.
- **Títulos de Tercer Nivel de Grado**: Licenciaturas, Ingenierías, Abogado/a de los Tribunales de la República, Médico/a (12 semestres con Internado Rotativo), CPA, etc., conforme al Reglamento de Régimen Académico del CES.
- **Guía de Acceso a la Educación Superior**: Información sobre el Registro Nacional SENESCYT, Universidades y Escuelas Politécnicas (EPN, ESPOL, ESPE, UCE, UG, UTPL, etc.).

1. **Cuestionario Vocacional Interactivo**:
   - **Fase 1: Intereses y Preferencias**: Basado en el modelo psicométrico **RIASEC de John Holland** (Realista, Investigativo, Artístico, Social, Emprendedor y Convencional).
   - **Fase 2: Autoevaluación de Habilidades y Talentos**: Evalúa 6 aptitudes clave (Lógico-Matemática, Verbal/Comunicativa, Espacial/Creativa, Interpersonal/Liderazgo, Técnica/Manual e Investigación Científica).
   - Escala tipo Likert (1 a 5) con interfaz ágil, barra de progreso en tiempo real y mapa de navegación de preguntas.

2. **Motor de Recomendación Inteligente (`RecommendationEngine`)**:
   - Calcula la afinidad vectorial entre el perfil del bachiller y las carreras universitarias en la base de datos.
   - Entrega un porcentaje de compatibilidad (Match %) junto a explicaciones personalizadas del porqué encaja cada opción.
   - Asigna un **Arquetipo Vocacional** (ej. *El Creador Científico y Tecnológico*, *El Líder Transformador*, *El Sanador Humanitario*).

3. **Panel de Resultados y Visualización Gráfica**:
   - Gráfico de **Radar interactivo** para las dimensiones Holland.
   - Gráfico de **Barras horizontales** para las habilidades autopercibidas con **Chart.js**.
   - Lista jerarquizada de carreras recomendadas (Top 6) y sugerencias complementarias.
   - Generación de **Informe Vocacional Imprimible y Exportable a PDF** con código único de validación y espacio de firmas para orientadores escolares y padres de familia.

4. **Catálogo y Fichas de Carreras**:
   - Directorio de **25 carreras universitarias de Tercer Nivel**, organizadas en 7 áreas de conocimiento:
     - 🌾 **Ciencias Agropecuarias y Alimentos**: *Medicina Veterinaria y Zootecnia, Ingeniería Agronómica y Agricultura Sostenible, Ingeniería en Alimentos y Agroindustria, Ingeniería Agropecuaria y Agronegocios*.
     - 🛡️ **Ingeniería y Tecnología**: *Ingeniería en Ciberseguridad, Ingeniería Biomédica y Bioingeniería, Inteligencia Artificial y Ciencia de Datos, Ingeniería de Software, Mecatrónica, Civil, Ambiental*.
     - 🩺 **Ciencias de la Salud**: *Medicina Humana, Enfermería*.
     - 💼 **Negocios y Finanzas**: *Administración de Empresas, Economía, Marketing Digital, Contabilidad y Auditoría (CPA)*.
     - 🎨 **Arte y Diseño**: *Diseño Gráfico, Arquitectura, Gastronomía*.
     - ⚖️ **Ciencias Sociales y Humanidades**: *Derecho, Psicología, Periodismo, Educación*.
     - 🔬 **Ciencias Exactas y Naturales**: *Biología y Biotecnología*.
   - Fichas completas con título de Tercer Nivel otorgado, duración en semestres, materias representativas, campo laboral y perfil del estudiante.

5. **Comparador de Carreras Cara a Cara**:
   - Permite seleccionar 2 o 3 opciones para contrastar simultáneamente duración, salidas profesionales, habilidades exigidas y asignaturas clave.

6. **Panel para Consejería y Orientación Escolar**:
   - Estadísticas globales de estudiantes evaluados, colegios con mayor participación, perfiles predominantes e historial de evaluaciones.

---

## 🏛️ Arquitectura del Sistema (MVC)

```
Prueba1/
├── run.py                         # Punto de entrada de la aplicación
├── config.py                      # Configuración de base de datos y llaves
├── app/
│   ├── __init__.py                # Fábrica de aplicaciones Flask (Application Factory)
│   ├── models/                    # [MODELO] Capa de datos y persistencia
│   │   ├── __init__.py
│   │   ├── database.py            # Esquema SQLite y carga de datos semilla
│   │   ├── career_model.py        # Consultas y filtros de carreras universitarias
│   │   ├── question_model.py      # Banco de preguntas psicométricas
│   │   └── result_model.py        # Almacenamiento de sesiones y resultados de tests
│   ├── services/                  # [SERVICIOS] Lógica de negocio y algoritmos
│   │   ├── __init__.py
│   │   └── recommendation_engine.py # Algoritmo de ponderación y arquetipos
│   ├── controllers/               # [CONTROLADOR] Manejo de peticiones y rutas
│   │   ├── __init__.py
│   │   ├── main_controller.py     # Home, catálogo, ficha y comparador
│   │   ├── test_controller.py     # Registro, cuestionario y procesamiento
│   │   ├── result_controller.py   # Visualización de resultados e impresión
│   │   └── admin_controller.py    # Panel estadístico para orientadores
│   ├── templates/                 # [VISTA] Plantillas HTML Jinja2
│   │   ├── base.html              # Layout general y barra de navegación
│   │   ├── home.html              # Portada para bachilleres
│   │   ├── guide.html             # Guía paso a paso para elegir carrera
│   │   ├── 404.html               # Página de error amigable
│   │   ├── test/
│   │   │   ├── start.html         # Formulario de datos del estudiante
│   │   │   └── quiz.html          # Cuestionario interactivo
│   │   ├── results/
│   │   │   ├── view.html          # Diagnóstico completo con gráficos
│   │   │   ├── search.html        # Recuperación de test por código
│   │   │   └── report_print.html  # Ficha imprimible / PDF
│   │   ├── careers/
│   │   │   ├── index.html         # Directorio con filtros
│   │   │   ├── detail.html        # Ficha técnica
│   │   │   └── compare.html       # Comparador de carreras
│   │   └── admin/
│   │       └── dashboard.html     # Métricas para orientadores
│   └── static/                    # [RECURSOS ESTÁTICOS]
│       ├── css/style.css          # Estilos y reglas de impresión
│       └── js/
│           ├── quiz.js            # Navegación del cuestionario
│           └── charts.js          # Gráficos Chart.js
├── data/
│   └── vocacional.db              # Base de datos SQLite
└── tests/
    ├── test_app.py                # Pruebas unitarias de modelos y rutas
    └── test_e2e.py                # Pruebas de integración de flujo completo
```

---

## 🚀 Puesta en Marcha y Ejecución

### 1. Requisitos
- Python 3.10 o superior (incluye `sqlite3`).
- Librerías Flask incluidas en el proyecto o instalables vía `pip install flask`.

### 2. Ejecutar la Aplicación
En la terminal, ejecuta:

```bash
python3 run.py
```

La aplicación iniciará automáticamente el servidor local en:
👉 **`http://localhost:5000`**

*(La base de datos SQLite con las 18 carreras y 24 preguntas psicométricas se inicializa automáticamente al arrancar por primera vez).*

---

## 🧪 Ejecución de Pruebas Automatizadas

Para verificar el correcto funcionamiento de los modelos, el motor de recomendación y las rutas:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📋 Rutas y Endpoints Principales

| Ruta | Método | Descripción |
|---|---|---|
| `/` | GET | Portada principal y bienvenida para bachilleres |
| `/guia-vocacional` | GET | Consejos y metodología para elegir carrera |
| `/carreras` | GET | Catálogo con buscador y filtros por área |
| `/carreras/<slug>` | GET | Ficha técnica y plan de estudios de la carrera |
| `/comparador` | GET | Herramienta para comparar hasta 3 carreras lado a lado |
| `/test/iniciar` | GET/POST | Registro inicial de datos del estudiante |
| `/test/cuestionario` | GET | Cuestionario vocacional de intereses y habilidades |
| `/test/procesar` | POST | Procesamiento de respuestas y cálculo del test |
| `/resultados/<codigo>` | GET | Vista interactiva de resultados con gráficos Chart.js |
| `/resultados/<codigo>/imprimir` | GET | Informe oficial listo para imprimir o guardar en PDF |
| `/resultados/consultar` | GET/POST | Búsqueda y recuperación de test mediante código |
| `/admin/dashboard` | GET | Panel de control y métricas para orientadores escolares |
