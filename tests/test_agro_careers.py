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

class TestAgroAndFoodCareers(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        class TestConfig(Config):
            TESTING = True
            DATABASE_PATH = self.db_path
            SECRET_KEY = 'test-secret-agro'

        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_agro_category_and_careers_presence(self):
        """Verifica que la categoría de Agropecuaria y Alimentos contenga las 4 carreras."""
        with self.app.app_context():
            categories = Career.get_categories()
            self.assertIn('Ciencias Agropecuarias y Alimentos', categories)

            agro_careers = Career.get_all(category='Ciencias Agropecuarias y Alimentos')
            slugs = [c['slug'] for c in agro_careers]
            self.assertIn('medicina-veterinaria-zootecnia', slugs)
            self.assertIn('ingenieria-agronomica', slugs)
            self.assertIn('ingenieria-alimentos-agroindustria', slugs)
            self.assertIn('ingenieria-agropecuaria-agronegocios', slugs)

    def test_veterinary_recommendation_matching(self):
        """Simula a un estudiante con vocación veterinaria y cuidado animal (R, I, S)."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                if q['dimension'] in ['R', 'I', 'S', 'scientific_research', 'technical_manual']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_names = [c['name'] for c in result['top_careers']]
            self.assertIn('Medicina Veterinaria y Zootecnia', top_names)
            
            vet_match = next(c for c in result['ranked_careers'] if c['slug'] == 'medicina-veterinaria-zootecnia')
            self.assertGreaterEqual(vet_match['match_percentage'], 80.0)

    def test_agronomy_recommendation_matching(self):
        """Simula a un estudiante con vocación agronómica, cultivos y campo (R, I, Técnica, Científica)."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                if q['dimension'] in ['R', 'I', 'technical_manual', 'scientific_research', 'logic_math']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_names = [c['name'] for c in result['top_careers']]
            self.assertIn('Ingeniería Agronómica y Agricultura Sostenible', top_names)
            
            agro_match = next(c for c in result['ranked_careers'] if c['slug'] == 'ingenieria-agronomica')
            self.assertGreaterEqual(agro_match['match_percentage'], 80.0)

    def test_food_engineering_recommendation_matching(self):
        """Simula a un estudiante con vocación de industria de alimentos (I, C, R, Química/Científica)."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                if q['dimension'] in ['I', 'C', 'R', 'scientific_research', 'technical_manual']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_names = [c['name'] for c in result['top_careers']]
            self.assertIn('Ingeniería en Alimentos y Agroindustria', top_names)

    def test_agribusiness_recommendation_matching(self):
        """Simula a un estudiante con perfil agropecuario emprendedor (R, E, Liderazgo)."""
        with self.app.app_context():
            questions = Question.get_all()
            answers = {}
            for q in questions:
                if q['dimension'] in ['R', 'E', 'social_leadership', 'logic_math']:
                    answers[f"q_{q['id']}"] = 5
                else:
                    answers[f"q_{q['id']}"] = 1

            result = RecommendationEngine.process_test(answers)
            top_names = [c['name'] for c in result['top_careers']]
            self.assertIn('Ingeniería Agropecuaria y Agronegocios', top_names)
            self.assertEqual(result['dominant_profile'], 'El Productor y Líder Agroindustrial')

if __name__ == '__main__':
    unittest.main()
