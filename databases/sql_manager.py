from sqlalchemy import create_engine, text
import os

class SQLManager:
    """
    Manages Relational Database connections for structured facts.
    Supports converting natural language questions to SQL (simulated).
    """
    def __init__(self, db_url=None):
        # Default to the centralized medical_main.db
        if not db_url:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'medical_main.db')
            db_url = f"sqlite:///{db_path}"
        
        self.engine = create_engine(db_url)
        print(f"[SQLManager] Connected to {db_url}")

    def execute_query(self, sql_query, params=None):
        """
        Executes a raw SQL query safely.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query), params or {})
                # Try to fetch all if it's a select
                if result.returns_rows:
                    return [dict(row._mapping) for row in result]
                return {"status": "success", "rows_effected": result.rowcount}
        except Exception as e:
            return {"error": str(e)}

    def get_all_doctors(self):
        return self.execute_query("SELECT * FROM doctors")

    def get_all_hospitals(self):
        return self.execute_query("SELECT * FROM hospitals")
        
    def text_to_sql_simulation(self, nl_question):
        """
        Simulates an Agent converting Text -> SQL.
        In a real app, this would use the LLM to generate the SQL.
        """
        nl_question = nl_question.lower()
        if "how many doctors" in nl_question:
            return "SELECT COUNT(*) as count FROM doctors"
        elif "list all hospitals" in nl_question:
            return "SELECT name, location FROM hospitals"
        elif "available doctors" in nl_question:
            return "SELECT name FROM doctors WHERE status='Available'"
        else:
            return None

# Singleton
sql_manager = SQLManager()
