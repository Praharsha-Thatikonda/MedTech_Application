# MedTech Application - Framework Implementations

This project contains three separate backend implementations for a Medical Application, demonstrating how to achieve similar functionality using different Python web frameworks: **FastAPI**, **Django**, and **Flask**.

## 🚀 Detailed Application Features

All implementations share a common set of frontend templates and core functionality. Key features include:

- **📊 Interactive Dashboard**: A centralized hub displaying the user's health overview, upcoming appointments, and access to recent chat sessions.
- **🤖 AI-Powered Medical Chat**: An intelligent chat interface (`/api/chat`) powered by a shared Large Language Model (LLM) service. The AI is context-aware, integrating data about local doctors and hospitals, and includes simulated image attachment handling.
- **🩺 Doctor Directory**: A comprehensive listing of medical professionals fetched from a centralized SQL database. Includes details like specialties, live status, experience, ratings, and contact info.
- **🏥 Hospital Locator**: A directory of medical facilities showing operational hours, emergency status (e.g., 24/7, Trauma Center), and locations.
- **👤 User Profile Management**: Displays and manages patient information such as blood type, pre-existing conditions, age, and contact details.
- **🧪 AI Lab & Advanced Routing**: Features dedicated pages for simulated advanced medical analysis (`/ailab`), geographical mapping (`/map`), and patient transportation logistics (`/transportation`).
- **🌱 Automatic Database Seeding**: On startup, the applications automatically seed the local SQLite database with mock users, doctors, hospitals, and chat sessions so you can start testing immediately.
- **🧩 Shared Core Logic**: The projects demonstrate modularity by sharing core Python logic across frameworks, such as the `llm_service.py` for AI text generation and `databases/sql_manager.py` for querying.

## 📁 Project Structure

The project is divided into three main folders, each containing a standalone application:

### ⚡ 1. FastAPI Implementation (`fast api/`)
Leverages modern Python features like type hints, Pydantic models, and asynchronous request handling for high performance.
-   **Database**: SQLite (`medical.db`) with SQLAlchemy ORM.
-   **Templating**: Jinja2
-   **Key Features**: Automatic database seeding, REST endpoints for chat/simulations, and Async support.
-   **How to run**:
    ```bash
    cd "fast api"
    pip install fastapi "uvicorn[standard]" sqlalchemy jinja2 pydantic
    uvicorn main:app --reload
    ```
    Access at `http://127.0.0.1:8000`. Auto-generated docs available at `/docs`.

### 🛡️ 2. Django Implementation (`django/`)
Robust implementation using the high-level Django web framework that encourages rapid development and clean design.
-   **Project Name**: `medical_project`
-   **Key Features**: Standard Django project layout, scalable architecture, and built-in management tools.
-   **How to run**:
    ```bash
    cd django
    pip install django
    python manage.py runserver
    ```
    Access at `http://127.0.0.1:8000`.

### 🍃 3. Flask Implementation (`flask/`)
Lightweight WSGI web application implementation, designed to be simple and easy to get started with.
-   **Templating**: Jinja2 (Built-in)
-   **Key Features**: Simple routing using decorators, direct HTML rendering, and minimal overhead.
-   **How to run**:
    ```bash
    cd flask
    pip install flask
    python app.py
    ```
    Access at `http://127.0.0.1:5001`.

## 📸 Screenshots

Here are some screenshots of the MedTech Application in action:

<div align="center">
  <img src="pics/Screenshot 2026-01-04 162518.png" width="45%" />
  <img src="pics/Screenshot 2026-01-09 172742.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 102438.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 102519.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 102638.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 102731.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 102816.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 102932.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 103127.png" width="45%" />
  <img src="pics/Screenshot 2026-05-09 104030.png" width="45%" />
  <img src="pics/Screenshot 2026-05-31 115117.png" width="45%" />
  <img src="pics/Screenshot 2026-07-05 121631.png" width="45%" />
</div>

## Getting Started

Navigate to the specific framework folder you wish to run and follow the detailed instructions above.
