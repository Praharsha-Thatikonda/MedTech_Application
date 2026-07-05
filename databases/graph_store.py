try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

class GraphStore:
    """
    Manages the Graph Database (Neo4j) for Knowledge Graphs.
    Maps relationships between entities (e.g., Doctor -WORKS_AT-> Hospital).
    """
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = None
        
        if GraphDatabase:
            try:
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
                print(f"[GraphStore] Neo4j driver initialized for {uri}")
            except Exception as e:
                # Silent fail if server not running, to not break app
                print(f"[GraphStore] Neo4j connection failed (Is server running?): {e}")
        else:
            print("[GraphStore] neo4j driver not installed. Graph features disabled.")

    def close(self):
        if self.driver:
            self.driver.close()

    def add_doctor_hospital_link(self, doctor_name, hospital_name):
        """
        Creates a relationship: (Doctor)-[:WORKS_AT]->(Hospital)
        """
        if not self.driver:
            return
            
        query = (
            "MERGE (d:Doctor {name: $doc_name}) "
            "MERGE (h:Hospital {name: $hosp_name}) "
            "MERGE (d)-[:WORKS_AT]->(h)"
        )
        try:
            with self.driver.session() as session:
                session.run(query, doc_name=doctor_name, hosp_name=hospital_name)
        except Exception as e:
            print(f"[GraphStore] Query failed: {e}")

    def find_hospital_for_doctor(self, doctor_name):
        """
        Finds where a doctor works using graph traversal.
        """
        if not self.driver:
            return None
            
        query = (
            "MATCH (d:Doctor {name: $doc_name})-[:WORKS_AT]->(h:Hospital) "
            "RETURN h.name AS hospital"
        )
        try:
            with self.driver.session() as session:
                result = session.run(query, doc_name=doctor_name)
                record = result.single()
                return record["hospital"] if record else None
        except Exception as e:
            print(f"[GraphStore] Query failed: {e}")
            return None

# Singleton
graph_store = GraphStore()
