import os
import sys
import unittest
import tempfile

# Asegurar librerías en path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
lib_dir = os.path.join(root_dir, 'lib')
for p in [root_dir, lib_dir]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from app import create_app
from app.models.career_model import Career
from app.models.question_model import Question
from app.services.recommendation_engine import RecommendationEngine
from config import Config

class TestModernCareers(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        class TestConfig(Config):
            TESTING = True
            DATABASE_PATH = self.db_path
            SECRET_KEY = 'test-secret'

        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_cybersecurity_career_presence_and_detail(self):
        """Verifica la existencia y ficha técnica de Ingeniería en Ciberseguridad."""
        with self.app.app_context():
            career = Career.get_by_slug('ingenieria-ciberseguridad')
            self.assertIsNotNone(career)
            self.assertEqual(career['name'], 'Ingeniería en Ciberseguridad y Seguridad de la Información')
            self.assertIn('Hacking', str(career['key_skills']))
            self.assertIn('SOC', str(career['labor_market']))

        res = self.client.get('/carreras/ingenieria-ciberseguridad')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Ciberseguridad'.encode('utf-8'), res.data)

    def test_biomedical_engineering_presence_and_detail(self):
        """Verifica la existencia y ficha técnica de Ingeniería Biomédica."""
        with self.app.app_context():
            career = Career.get_by_slug('ingenieria-biomedica-bioingenieria')
            self.assertIsNotNone(career)
            self.assertEqual(career['name'], 'Ingeniería Biomédica y Bioingeniería')
            self.assertIn('Dispositivos Médicos', str(career['key_skills']))
            self.assertIn('Hospitales', str(career['labor_market']))

        res = self.client.get('/carreras/ingenieria-biomedica-bioingenieria')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Biomédica'.encode('utf-8'), res.data)

    def test_cybersecurity_recommendation_matching(self):
        """Simula respuestas de un bachiller con perfil de Ciberseguridad (I, C, R, Lógica, Técnica)."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                # Ciberseguridad valora alto: I (investigativo), C (convencional/normativo), R (técnico) y lógica/técnica
                if q['dimension'] in ['I', 'C', 'R', 'logic_math', 'technical_manual', 'scientific_research']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_career_names = [c['name'] for c in result['top_careers']]
            self.assertIn('Ingeniería en Ciberseguridad y Seguridad de la Información', top_career_names)
            
            cyber_match = next(c for c in result['ranked_careers'] if c['slug'] == 'ingenieria-ciberseguridad')
            self.assertGreaterEqual(cyber_match['match_percentage'], 80.0)

    def test_biomedical_engineering_recommendation_matching(self):
        """Simula respuestas de un bachiller con perfil Biomédico (I, R, S, Técnica, Científica)."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                # Biomédica valora: I (investigación), R (técnica/física), S (salud/impacto humano) y destreza técnica/científica
                if q['dimension'] in ['I', 'R', 'S', 'scientific_research', 'technical_manual', 'logic_math']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_career_names = [c['name'] for c in result['top_careers']]
            self.assertIn('Ingeniería Biomédica y Bioingeniería', top_career_names)
            
            biomed_match = next(c for c in result['ranked_careers'] if c['slug'] == 'ingenieria-biomedica-bioingenieria')
            self.assertGreaterEqual(biomed_match['match_percentage'], 80.0)

if __name__ == '__main__':
    unittest.main()
