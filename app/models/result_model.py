import json
import uuid
from datetime import datetime
from app.models.database import get_db_connection

class TestResult:
    """Modelo para guardar y consultar los resultados de tests vocacionales."""

    @staticmethod
    def _parse_row(row):
        if not row:
            return None
        item = dict(row)
        for field in ['riasec_scores_json', 'skill_scores_json', 'recommended_careers_json', 'answers_json']:
            if field in item and isinstance(item[field], str):
                try:
                    # Usamos nombres limpios sin el sufijo _json para comodidad de las vistas
                    clean_name = field.replace('_json', '')
                    item[clean_name] = json.loads(item[field])
                except Exception:
                    clean_name = field.replace('_json', '')
                    item[clean_name] = {}
        return item

    @classmethod
    def save(cls, student_data, riasec_scores, skill_scores, dominant_profile, dominant_profile_desc, recommended_careers, raw_answers):
        code = str(uuid.uuid4())[:8].upper()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO test_results (
            code, student_name, student_school, student_grade, student_email, student_age,
            riasec_scores_json, skill_scores_json, dominant_profile, dominant_profile_desc,
            recommended_careers_json, answers_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            code,
            student_data.get('name', 'Estudiante Bachiller'),
            student_data.get('school', ''),
            student_data.get('grade', ''),
            student_data.get('email', ''),
            int(student_data.get('age', 17)) if student_data.get('age') else 17,
            json.dumps(riasec_scores),
            json.dumps(skill_scores),
            dominant_profile,
            dominant_profile_desc,
            json.dumps(recommended_careers),
            json.dumps(raw_answers)
        ))
        conn.commit()
        conn.close()
        return code

    @classmethod
    def get_by_code(cls, code):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM test_results WHERE code = ?", (code,)).fetchone()
        conn.close()
        return cls._parse_row(row)

    @classmethod
    def get_recent(cls, limit=10):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM test_results ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [cls._parse_row(r) for r in rows]

    @classmethod
    def get_stats(cls):
        conn = get_db_connection()
        total_tests = conn.execute("SELECT COUNT(*) as count FROM test_results").fetchone()['count']
        
        # Conteo por perfil dominante
        profiles = conn.execute('''
            SELECT dominant_profile, COUNT(*) as count 
            FROM test_results 
            GROUP BY dominant_profile 
            ORDER BY count DESC
        ''').fetchall()
        
        # Conteo de escuelas
        schools = conn.execute('''
            SELECT student_school, COUNT(*) as count 
            FROM test_results 
            WHERE student_school IS NOT NULL AND student_school != ''
            GROUP BY student_school 
            ORDER BY count DESC LIMIT 5
        ''').fetchall()

        conn.close()
        return {
            'total_tests': total_tests,
            'profiles': [dict(p) for p in profiles],
            'top_schools': [dict(s) for s in schools]
        }
