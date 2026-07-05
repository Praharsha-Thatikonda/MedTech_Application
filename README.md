# MedTech Application - Framework Implementations

This project contains three separate backend implementations for a Medical Application, demonstrating how to achieve similar functionality using different Python web frameworks: **FastAPI**, **Django**, and **Flask**.

## 🚀 General Application Features

All implementations share a common set of frontend templates and general features:
-   **Dashboard**: Overview of user health, upcoming appointments, and simulated data.
-   **Chat Interface**: AI-assisted medical chat.
-   **Doctors & Hospitals**: Listings of medical professionals and facilities.
-   **Profile**: User profile management.
-   **AI Lab & Maps**: Additional simulated features.

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
