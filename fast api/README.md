# Medical App - FastAPI Implementation

This directory contains the **FastAPI** version of the Medical Application. It leverages modern Python features like type hints, Pydantic models, and asynchronous request handling for high performance.

## Application Info

-   **Framework**: FastAPI
-   **Database**: SQLite (`medical.db`)
-   **ORM**: SQLAlchemy
-   **Templating**: Jinja2
-   **Entry Point**: `main.py`

### Key Features
-   **Automatic Database Seeding**: On startup, the application checks for and creates initial data for Users, Doctors, Hospitals, and Chat Sessions.
-   **API Endpoints**: Includes REST endpoints for chat interactions (`/api/chat`) and simulations (`/api/analyze`).
-   **Async Support**: Utilizes `async/await` for non-blocking route handlers.

## Usage Guide

### Prerequisites
Ensure you have Python installed. You will need to install the required dependencies.

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy jinja2 pydantic
```

### Running the Application

1.  Navigate to this directory:
    ```bash
    cd "fast api"
    ```

2.  Start the development server using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    *   `main`: Refers to the file `main.py`.
    *   `app`: Refers to the `app = FastAPI()` object inside `main.py`.
    *   `--reload`: Enables auto-reload on code changes (useful for development).

3.  Open your browser and navigate to:
    *   **App**: `http://127.0.0.1:8000`
    *   **Auto-generated Docs**: `http://127.0.0.1:8000/docs`

### Project Structure
-   `main.py`: The core application file containing routes and startup logic.
-   `models.py`: SQLAlchemy database models.
-   `templates/`: HTML files for the frontend.
-   `static/`: CSS, JavaScript, and images.
