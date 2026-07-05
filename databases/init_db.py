import sqlite3
import os
import sys

# Add parent dir to path to import backend mock data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.data_loader import get_mock_data

def init_sql_db():
    db_path = os.path.join(os.path.dirname(__file__), 'medical_main.db')
    
    # Remove existing to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"[Init] Creating Main SQL Database at: {db_path}")
    
    # 1. Doctors Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        specialty TEXT,
        location TEXT,
        lat REAL,
        lon REAL,
        status TEXT,
        rating REAL
    )
    ''')
    
    # 2. Hospitals Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hospitals (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT,
        lat REAL,
        lon REAL,
        type TEXT,
        open_hours TEXT
    )
    ''')
    
    # 3. Populate from Data Loader
    data = get_mock_data()
    
    print("[Init] Seeding Doctors...")
    for d in data['doctors']:
        cursor.execute('''
        INSERT INTO doctors (id, name, specialty, location, lat, lon, status, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (d['id'], d['name'], d['specialty'], d['location'], d['coords'][0], d['coords'][1], d['status'], d['rating']))

    print("[Init] Seeding Hospitals...")
    for h in data['hospitals']:
        cursor.execute('''
        INSERT INTO hospitals (id, name, location, lat, lon, type, open_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (h['id'], h['name'], h['location'], h['coords'][0], h['coords'][1], h['type'], h['open_hours']))
        
    conn.commit()
    conn.close()
    print("[Init] SQL Database Ready.")

def init_vector_db():
    try:
        import chromadb
        print("[Init] initializing Vector Database (Chroma)...")
        db_path = os.path.join(os.path.dirname(__file__), 'chroma_db')
        
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection("medical_knowledge")
        
        # Add some basic medical knowledge
        docs = [
            "Chest pain can be a sign of heart attack. Immediate attention needed.",
            "Migraines are severe headaches often accompanied by nausea and light sensitivity.",
            "Diabetes management involves monitoring blood sugar and insulin.",
            "Hypertension (high blood pressure) is a risk factor for stroke.",
            "Normal body temperature is around 98.6°F (37°C)."
        ]
        ids = [f"med_fact_{i}" for i in range(len(docs))]
        
        collection.add(
            documents=docs,
            ids=ids
        )
        print(f"[Init] Vector Database seeded with {len(docs)} documents.")
        
    except ImportError:
        print("[Init] ChromaDB not installed. Skipping Vector DB creation.")
    except Exception as e:
        print(f"[Init] Vector DB Error: {e}")

if __name__ == "__main__":
    init_sql_db()
    init_vector_db()
