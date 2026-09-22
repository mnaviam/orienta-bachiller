import os
import sys
import unittest

# Incluir ruta raíz y librerías
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
lib_dir = os.path.join(root_dir, 'lib')
for p in [root_dir, lib_dir]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from app import create_app
from app.models.career_model import Career
from app.models.question_model import Question
from app.models.result_model import TestResult
from app.services.recommendation_engine import RecommendationEngine

class TestLiveSystemFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_homepage_and_navigation(self):
        """Verifica que la página principal cargue y contenga los elementos de BGU Ecuador."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'OrientaBachiller', res.data)
        self.assertIn('Especial para Estudiantes de Bachillerato (BGU • Ecuador)'.encode('utf-8'), res.data)
        self.assertIn(b'Hacer Test Vocacional', res.data)
        self.assertIn(b'Cat', res.data)
        print("✅ Test 1: Portada y navegación inicial funcionan correctamente.")

    def test_02_guide_ecuador(self):
        """Verifica la guía vocacional adaptada a Ecuador (LOES, CES, SENESCYT, BGU)."""
        res = self.client.get('/guia-vocacional')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Estructura de la Educación Superior en el Ecuador'.encode('utf-8'), res.data)
        self.assertIn('SENESCYT'.encode('utf-8'), res.data)
        self.assertIn('Bachillerato (BGU / BT)'.encode('utf-8'), res.data)
        print("✅ Test 2: Guía BGU Ecuador y Educación Superior verificada.")

    def test_03_career_catalog_and_filters(self):
        """Verifica el catálogo de carreras con buscador y filtros por área."""
        # Catálogo general
        res = self.client.get('/carreras')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Cat', res.data)

        # Filtro de categoría: Ciencias de la Salud
        res_cat = self.client.get('/carreras?category=Ciencias+de+la+Salud')
        self.assertEqual(res_cat.status_code, 200)
        self.assertIn(b'Medicina Humana', res_cat.data)
        self.assertIn(b'Enfermer', res_cat.data)

        # Búsqueda por palabra clave: "Software"
        res_search = self.client.get('/carreras?search=Software')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Ingenier', res_search.data)
        print("✅ Test 3: Catálogo, filtros por categoría y buscador validados.")

    def test_04_career_details_and_comparator(self):
        """Verifica la ficha técnica de una carrera y el comparador cara a cara."""
        # Ficha técnica
        res = self.client.get('/carreras/ingenieria-software-sistemas')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Ingeniero/a en Software (Tercer Nivel de Grado)'.encode('utf-8'), res.data)
        self.assertIn('Campo Laboral'.encode('utf-8'), res.data or b'donde')

        # Comparador de 3 carreras
        with self.app.app_context():
            careers = Career.get_all()
            c1, c2, c3 = careers[0]['id'], careers[1]['id'], careers[2]['id']

        res_comp = self.client.get(f'/comparador?c1={c1}&c2={c2}&c3={c3}')
        self.assertEqual(res_comp.status_code, 200)
        self.assertIn(b'Aspecto', res_comp.data)
        self.assertIn(careers[0]['name'].encode('utf-8'), res_comp.data)
        self.assertIn(careers[1]['name'].encode('utf-8'), res_comp.data)
        print("✅ Test 4: Fichas técnicas y Comparador de Carreras validados.")

    def test_05_profile_simulation_tech(self):
        """Simula a un estudiante de 3ero BGU con perfil Tecnológico/Ingeniería."""
        # Paso 1: Iniciar sesión del estudiante
        student_data = {
            'student_name': 'Mateo Morales',
            'student_school': 'U.E. Fiscal San Gabriel (Quito)',
            'student_grade': '3.° de Bachillerato (3ero BGU - Graduando)',
            'student_age': '17',
            'student_email': 'mateo.morales@ejemplo.ec'
        }
        res_init = self.client.post('/test/iniciar', data=student_data, follow_redirects=True)
        self.assertEqual(res_init.status_code, 200)
        self.assertIn(b'Mateo Morales', res_init.data)

        # Paso 2: Responder cuestionario (Máximo puntaje en R, I y Habilidad Lógica/Técnica)
        with self.app.app_context():
            questions = Question.get_all()

        form_payload = dict(student_data)
        for q in questions:
            if q['dimension'] in ['R', 'I', 'logic_math', 'technical_manual']:
                form_payload[f"q_{q['id']}"] = "5"
            else:
                form_payload[f"q_{q['id']}"] = "1"

        res_proc = self.client.post('/test/procesar', data=form_payload, follow_redirects=True)
        self.assertEqual(res_proc.status_code, 200)
        self.assertIn(b'Informe Vocacional', res_proc.data)
        self.assertIn(b'Mateo Morales', res_proc.data)
        self.assertIn('Ingeniería'.encode('utf-8'), res_proc.data)

        # Obtener código del estudiante evaluado
        with self.app.app_context():
            recent_list = TestResult.get_recent(20)
            target = next(r for r in recent_list if r['student_name'] == 'Mateo Morales')
            code = target['code']

        # Verificar Informe Imprimible (PDF)
        res_print = self.client.get(f'/resultados/{code}/imprimir')
        self.assertEqual(res_print.status_code, 200)
        self.assertIn('Consejería Estudiantil (DECE)'.encode('utf-8'), res_print.data)
        self.assertIn('Representante Legal'.encode('utf-8'), res_print.data)

        # Consultar por código
        res_search = self.client.post('/resultados/consultar', data={'code': code}, follow_redirects=True)
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Mateo Morales', res_search.data)
        print(f"✅ Test 5: Perfil Tecnológico evaluado exitosamente (Código generado: {code}).")

    def test_06_profile_simulation_health(self):
        """Simula a una estudiante de Bachillerato Técnico con vocación médica."""
        student_data = {
            'student_name': 'Valeria Zambrano',
            'student_school': 'U.E. Vicente Rocafuerte (Guayaquil)',
            'student_grade': 'Bachillerato Técnico (BT)',
            'student_age': '18',
            'student_email': 'valeria.z@ejemplo.ec'
        }
        with self.app.app_context():
            questions = Question.get_all()

        form_payload = dict(student_data)
        for q in questions:
            if q['dimension'] in ['S', 'I', 'scientific_research', 'social_leadership']:
                form_payload[f"q_{q['id']}"] = "5"
            else:
                form_payload[f"q_{q['id']}"] = "1"

        res_proc = self.client.post('/test/procesar', data=form_payload, follow_redirects=True)
        self.assertEqual(res_proc.status_code, 200)
        self.assertIn(b'Valeria Zambrano', res_proc.data)
        self.assertIn('Medicina Humana'.encode('utf-8'), res_proc.data)
        print("✅ Test 6: Perfil de Salud evaluado exitosamente (Medicina recomendada).")

    def test_07_admin_dashboard(self):
        """Verifica que el panel del orientador DECE reporte las métricas actualizadas."""
        res = self.client.get('/admin/dashboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Consejería Estudiantil (DECE)'.encode('utf-8'), res.data)
        self.assertIn('Total Bachilleres Evaluados'.encode('utf-8'), res.data)
        self.assertIn('Mateo Morales'.encode('utf-8'), res.data)
        self.assertIn('Valeria Zambrano'.encode('utf-8'), res.data)
        print("✅ Test 7: Panel DECE con estadísticas en vivo verificado.")

if __name__ == '__main__':
    unittest.main()
