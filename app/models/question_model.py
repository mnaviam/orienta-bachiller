from app.models.database import get_db_connection

class Question:
    """Modelo para representar y consultar las preguntas del Cuestionario Vocacional."""

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM questions ORDER BY order_num ASC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def get_by_section(cls, section):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM questions WHERE section = ? ORDER BY order_num ASC", (section,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def get_grouped_by_section(cls):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM questions ORDER BY section DESC, order_num ASC").fetchall()
        conn.close()
        
        grouped = {
            'interests': [],
            'skills': []
        }
        for r in rows:
            sec = r['section']
            if sec in grouped:
                grouped[sec].append(dict(r))
        return grouped
