# FastAPI Framework Documentation - MedTech AI

## 1. Overview
The FastAPI implementation is the high-performance, async-native version of MedTech AI. It is optimized for speed, automatic documentation (Swagger UI), and handling concurrent requests, making it the "Production-Ready" API choice.

## 2. Project Structure
```text
f_two/
├── fast api/  (Note: space in folder name)
│   ├── main.py             # Main Application Entry Point
│   ├── models.py           # Pydantic & SQLAlchemy Models
│   ├── medical_chat.db     # Local User/Session Database
│   ├── static/             # Static Assets
│   └── templates/          # Jinja2 Templates
```

## 3. Configuration & Setup

### Prerequisites
- Python 3.10+
- Dependencies: `fastapi`, `uvicorn`, `sqlalchemy`, `jinja2`

### Installation
1. Navigate to the project root:
   ```bash
   cd f_two/fast api
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

## 4. Running the Server
FastAPI requires an ASGI server (Uvicorn) to run.
```bash
python -m uvicorn main:app --port 8003 --reload
```
- **App URL**: `http://localhost:8003/`
- **Auto-Docs**: `http://localhost:8003/docs` (Swagger UI)

## 5. Key Components

### Main Application (`main.py`)
- **Async Endpoints**: All routes are defined with `async def`, allowing non-blocking I/O.
- **Dependency Injection**: Uses `Depends(get_db)` to manage database sessions efficiently.
- **Pydantic Models**: Strictly validates all incoming JSON data (e.g., Chat Requests).

### Database Integration
- **Local DB**: Uses SQLAlchemy with `databases/medical_chat.db` for async-friendly user logging.
- **Central DB**: Imports `sql_manager` to read shared Doctor/Hospital data synchronously (or asynchronously if configured).

## 6. Features Implemented
- **Automatic API Documentation**: Swagger UI and ReDoc generated automatically.
- **Type Safety**: Full Python type hinting support.
- **WebSocket Ready**: Infrastructure in place for real-time chat (future upgrade).
- **High Concurrency**: Capable of handling thousands of requests per second.

## 7. Integration with Shared Services
FastAPI integrates deeply with the shared backend:
- **Triage Service**: Runs symptom analysis logic.
- **Geo Service**: Calculates distances asynchronously.
- **LLM Service**: Calls the Gemma model for responses.
