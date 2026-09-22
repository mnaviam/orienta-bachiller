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
from app.models.career_model import Career
from app.models.question_model import Question
from app.models.result_model import TestResult
from app.services.recommendation_engine import RecommendationEngine
from config import Config

class TestOrientaBachillerE2E(unittest.TestCase):

    def setUp(self):
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

    def test_complete_student_flow(self):
        """Prueba de flujo completo: inicio de test, envío de cuestionario y visualización de informe."""
        # 1. Paso 1: Iniciar test
        start_resp = self.client.post('/test/iniciar', data={
            'student_name': 'Sofía Valencia',
            'student_school': 'U.E. Fiscal Mejía (Quito)',
            'student_grade': '3.° de Bachillerato (3ero BGU - Graduando)',
            'student_age': '17',
            'student_email': 'sofia@example.com'
        }, follow_redirects=True)
        self.assertEqual(start_resp.status_code, 200)
        self.assertIn(b'Sof', start_resp.data)

        # 2. Cargar preguntas
        with self.app.app_context():
            questions = Question.get_all()

        form_data = {
            'student_name': 'Sofía Valencia',
            'student_school': 'U.E. Fiscal Mejía (Quito)',
            'student_grade': '3.° de Bachillerato (3ero BGU - Graduando)',
            'student_age': '17',
            'student_email': 'sofia@example.com'
        }
        for q in questions:
            form_data[f"q_{q['id']}"] = "4"

        # 3. Enviar respuestas
        process_resp = self.client.post('/test/procesar', data=form_data, follow_redirects=True)
        self.assertEqual(process_resp.status_code, 200)
        self.assertIn(b'Informe Vocacional', process_resp.data)
        self.assertIn(b'Sof', process_resp.data)

        # 4. Obtener código generado y probar búsqueda
        with self.app.app_context():
            recent = TestResult.get_recent(1)
            self.assertEqual(len(recent), 1)
            code = recent[0]['code']

        # 5. Probar vista de impresión
        print_resp = self.client.get(f'/resultados/{code}/imprimir')
        self.assertEqual(print_resp.status_code, 200)
        self.assertIn('Informe de Orientación'.encode('utf-8'), print_resp.data)
        self.assertIn(b'OrientaBachiller', print_resp.data)

        # 6. Probar consulta por código
        search_resp = self.client.post('/resultados/consultar', data={'code': code}, follow_redirects=True)
        self.assertEqual(search_resp.status_code, 200)
        self.assertIn(code.encode(), search_resp.data)

    def test_career_comparator(self):
        """Prueba el comparador con 2 y 3 carreras."""
        with self.app.app_context():
            careers = Career.get_all()
            c1, c2 = careers[0]['id'], careers[1]['id']

        resp = self.client.get(f'/comparador?c1={c1}&c2={c2}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Aspecto', resp.data)
        self.assertIn(b'Comparador de Carreras', resp.data)

if __name__ == '__main__':
    unittest.main()
