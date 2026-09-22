import json
from app.models.database import get_db_connection

class Career:
    """Modelo para representar y consultar las Carreras Universitarias."""
    
    @staticmethod
    def _parse_row(row):
        if not row:
            return None
        item = dict(row)
        # Parsear JSON fields
        for field in ['labor_market', 'key_skills', 'typical_subjects', 'reasons_to_study']:
            if field in item and isinstance(item[field], str):
                try:
                    item[field] = json.loads(item[field])
                except Exception:
                    item[field] = []
        return item

    @classmethod
    def get_all(cls, category=None, search_term=None):
        conn = get_db_connection()
        query = "SELECT * FROM careers WHERE 1=1"
        params = []

        if category and category != 'all':
            query += " AND category = ?"
            params.append(category)

        if search_term:
            query += " AND (name LIKE ? OR short_description LIKE ? OR category LIKE ?)"
            term = f"%{search_term}%"
            params.extend([term, term, term])

        query += " ORDER BY name ASC"
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [cls._parse_row(r) for r in rows]

    @classmethod
    def get_by_id(cls, career_id):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM careers WHERE id = ?", (career_id,)).fetchone()
        conn.close()
        return cls._parse_row(row)

    @classmethod
    def get_by_slug(cls, slug):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM careers WHERE slug = ?", (slug,)).fetchone()
        conn.close()
        return cls._parse_row(row)

    @classmethod
    def get_categories(cls):
        conn = get_db_connection()
        rows = conn.execute("SELECT DISTINCT category FROM careers ORDER BY category ASC").fetchall()
        conn.close()
        return [r['category'] for r in rows]

    @classmethod
    def get_multiple_by_ids(cls, ids):
        if not ids:
            return []
        conn = get_db_connection()
        placeholders = ','.join('?' for _ in ids)
        rows = conn.execute(f"SELECT * FROM careers WHERE id IN ({placeholders})", ids).fetchall()
        conn.close()
        careers_dict = {r['id']: cls._parse_row(r) for r in rows}
        return [careers_dict[cid] for cid in ids if cid in careers_dict]
