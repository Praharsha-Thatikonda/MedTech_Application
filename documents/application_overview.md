# MedTech AI - Application Overview

## 1. Introduction
MedTech AI is a next-generation medical assistance platform designed to demonstrate the power of **Agentic AI** in healthcare. It provides a unified interface for symptom analysis, doctor discovery, emergency transportation, and AI-driven medical advice.

The unique architectural feature of this project is its **Multi-Framework Support**. The exact same application features are implemented across three popular Python frameworks—**Django, Flask, and FastAPI**—sharing a single "Brain" (Backend) and "Memory" (Database).

## 2. Architecture Diagram

```mermaid
graph TD
    User[User Interface] -->|HTTP| FW[Framework Layer]
    
    subgraph "Framework Layer (Choose One)"
        Django[Django Server :8002]
        Flask[Flask App :5001]
        FastAPI[FastAPI Server :8003]
    end
    
    subgraph "Shared Backend Services"
        LLM[LLM Service (Gemma 4B)]
        Triage[Triage Service]
        Geo[Geo Service]
        Search[Search Engine]
    end
    
    subgraph "Database Hub"
        Central[Medical Main DB (SQL) - Doctors/Hospitals]
        Vector[ChromaDB (Vector) - Knowledge Base]
        Graph[Neo4j (Graph) - Relationships]
        Cache[Redis (Cache) - Sessions]
    end
    
    FW --> LLM
    FW --> Triage
    FW --> Geo
    LLM --> Vector
    FW --> Central
```

## 3. Core Features

### 🧠 Dr. AI Assistant
A context-aware chatbot powered by the **Gemma 2/3 (4B)** model.
- **RAG (Retrieval Augmented Generation)**: Fetches real medical data and local doctor info to ground its answers.
- **Triage**: Detects emergencies (e.g., "Heart Attack") and instantly overrides chat to show hospitals.

### 🏥 Doctor & Hospital Directory
- **Search**: Find specialists by name, location, or condition.
- **Availability**: Real-time status indicators (Available/Busy).
- **Localization**: Data is tailored to Indian metros (Mumbai, Delhi, Bangalore).

### 🚑 Emergency Transportation
- **Live Map**: Integrated Leaflet.js map for tracking ambulances.
- **Booking**: "Uber-like" interface for booking Ambulances, Patient Transport, or Air Ambulances.
- **SOS**: One-touch connection to emergency services (108).

### 📍 Interactive Map
- **Geo-filters**: Filter markers by Hospital, Clinic, or Pharmacy.
- **Distance Calculation**: Automatically sorts results by proximity to the user.

## 4. Shared Database Hub
The application uses a centralized `databases/` folder to ensure data consistency across all frameworks.
- **`medical_main.db` (SQLite)**: The master list of Doctors and Hospitals.
- **`chroma_db/`**: Stores embeddings of medical textbooks/wikis for the AI to "read".
- **`medical_chat.db` (Per Framework)**: Keeps user session history isolated per framework.

## 5. Setup & Usage

### Global Prerequisites
1. **Python 3.10+** installed.
2. **NVIDIA GPU** (Optional but recommended for LLM speed).

### Installation
1. Clone the repository.
2. Install shared requirements:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure `torch`, `llama-cpp-python`, `flask`, `django`, `fastapi`, `uvicorn` are installed)*

### Data Initialization
Before running, initialize the central database:
```bash
python databases/init_db.py
```

### Running the Apps
- **Flask**: `python flask/app.py`
- **Django**: `python manage.py runserver 8002` (inside `django/`)
- **FastAPI**: `uvicorn main:app --reload` (inside `fast api/`)

## 6. Troubleshooting
- **LLM Not Loading?**: Ensure you have the `models/` directory populated with the `.gguf` file.
- **Database Error?**: Run `init_db.py` to reset the SQL tables.
- **Port Conflict?**: Kill existing python processes or change the port flags (e.g., `--port 8004`).
