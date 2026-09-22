import os
import sys
import unittest
import tempfile
import json

# Asegurar que el directorio raíz y ./lib estén en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
lib_dir = os.path.join(root_dir, 'lib')

for path in [root_dir, lib_dir]:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

from app import create_app
from app.models.database import init_db, get_db_connection
from app.models.career_model import Career
from app.models.question_model import Question
from app.models.result_model import TestResult
from app.services.recommendation_engine import RecommendationEngine
from config import Config

class TestOrientaBachiller(unittest.TestCase):

    def setUp(self):
        # Base de datos temporal para pruebas
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        class TestConfig(Config):
            TESTING = True
            DATABASE_PATH = self.db_path
            SECRET_KEY = 'test-secret-key'

        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_database_seeding(self):
        """Verifica que las tablas se inicialicen y tengan datos semilla."""
        with self.app.app_context():
            careers = Career.get_all()
            self.assertGreaterEqual(len(careers), 10, "Debe haber al menos 10 carreras cargadas")
            
            questions = Question.get_all()
            self.assertGreaterEqual(len(questions), 20, "Debe haber al menos 20 preguntas en el test")
            
            categories = Career.get_categories()
            self.assertIn('Ingeniería y Tecnología', categories)
            self.assertIn('Ciencias de la Salud', categories)

    def test_recommendation_engine_technology(self):
        """Verifica que un perfil con altos puntajes en R, I y lógica sea recomendado a Tecnología/Ingeniería."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                if q['dimension'] in ['R', 'I', 'logic_math', 'technical_manual']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            self.assertIn('ranked_careers', result)
            self.assertGreater(len(result['ranked_careers']), 0)
            
            top_career = result['top_careers'][0]
            self.assertIn(top_career['category'], ['Ingeniería y Tecnología', 'Ciencias Exactas y Naturales'])
            self.assertGreaterEqual(top_career['match_percentage'], 80)

    def test_recommendation_engine_health(self):
        """Verifica que un perfil con altos puntajes en S, I y ciencias sea recomendado a Salud."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                if q['dimension'] in ['S', 'I', 'scientific_research', 'social_leadership']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_career = result['top_careers'][0]
            self.assertIn(top_career['category'], ['Ciencias de la Salud', 'Ciencias Sociales y Humanidades'])

    def test_test_result_save_and_retrieve(self):
        """Verifica el guardado y consulta de resultados en la base de datos."""
        with self.app.app_context():
            student = {
                'name': 'Carlos Mendoza',
                'school': 'Instituto Nacional',
                'grade': '11° Grado',
                'age': 17,
                'email': 'carlos@ejemplo.com'
            }
            riasec = {'percentages': {'R': 80, 'I': 90, 'A': 30, 'S': 40, 'E': 50, 'C': 60}, 'dominant_dims': ['I', 'R']}
            skills = {'percentages': {'logic_math': 95, 'verbal': 60}}
            profile = 'El Creador Científico y Tecnológico'
            desc = 'Descripción de prueba'
            careers = [{'id': 1, 'name': 'Ingeniería de Software', 'match_percentage': 95.5}]
            
            code = TestResult.save(student, riasec, skills, profile, desc, careers, {})
            self.assertIsNotNone(code)
            self.assertEqual(len(code), 8)

            saved = TestResult.get_by_code(code)
            self.assertIsNotNone(saved)
            self.assertEqual(saved['student_name'], 'Carlos Mendoza')
            self.assertEqual(saved['dominant_profile'], profile)

    def test_http_routes(self):
        """Prueba que todas las rutas principales respondan HTTP 200."""
        # Home
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OrientaBachiller', response.data)

        # Guía
        response = self.client.get('/guia-vocacional')
        self.assertEqual(response.status_code, 200)

        # Catálogo
        response = self.client.get('/carreras')
        self.assertEqual(response.status_code, 200)

        # Detalle de Carrera
        response = self.client.get('/carreras/ingenieria-software-sistemas')
        self.assertEqual(response.status_code, 200)

        # Comparador
        response = self.client.get('/comparador')
        self.assertEqual(response.status_code, 200)

        # Iniciar Test
        response = self.client.get('/test/iniciar')
        self.assertEqual(response.status_code, 200)

        # Dashboard Admin
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)

        # Búsqueda de Resultados
        response = self.client.get('/resultados/consultar')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
