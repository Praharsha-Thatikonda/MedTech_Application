# Flask Framework Documentation - MedTech AI

## 1. Overview
The Flask implementation provides a lightweight, flexible version of the MedTech AI application. It is designed for simplicity and ease of extension, making it ideal for microservices or rapid prototyping.

## 2. Project Structure
```text
f_two/
├── flask/
│   ├── app.py              # Main Application Entry Point
│   ├── models.py           # SQLAlchemy Models for Local User DB
│   ├── medical_chat.db     # Local User/Session Database
│   ├── static/             # CSS/JS Assets
│   └── templates/          # HTML Templates (Jinja2)
│       ├── index.html      # Main Dashboard
│       ├── doctors.html    # Doctors List
│       ├── ...
```

## 3. Configuration & Setup

### Prerequisites
- Python 3.10+
- Dependencies: `flask`, `sqlalchemy`

### Installation
1. Navigate to the project root:
   ```bash
   cd f_two
   ```
2. Install dependencies:
   ```bash
   pip install flask sqlalchemy
   ```

## 4. Running the Application
To start the Flask development server:
```bash
python flask/app.py
```
By default, it runs on **Port 5001**: `http://localhost:5001/`

## 5. Key Components

### Application Logic (`app.py`)
- **App Factory**: Initializes the Flask app and SQLAlchemy engine.
- **Routes**:
    - `@app.route('/')`: Serves the main SPA (Single Page Application).
    - `@app.route('/api/chat')`: JSON endpoint for AI interaction.
- **Database Connection**: Establishes a connection to `medical_chat.db` for storing chat logs.

### Database Architecture
- **User Data**: Stored locally in `medical_chat.db` (Chat Logs, User Profile).
- **Application Data**: Doctors and Hospitals are fetched from the *Central DB* (`databases/medical_main.db`) using the `sql_manager` utility.

## 6. Features Implemented
- **Blueprints**: (Optional) Structure ready for modularization.
- **Jinja2 Templating**: Dynamic HTML rendering.
- **Session Management**: Lightweight cookie-based sessions.
- **Mock Data Loading**: Capable of falling back to `data_loader.py` if databases are offline.

## 7. Integration with Shared Services
Flask shares the core "Brain" of the application with Django and FastAPI:
- **LLM Service**: Imported from `..llm_service`.
- **Vector DB**: Accesses the shared `chroma_db` for RAG.
