# Medical App - Django Implementation

This directory contains the **Django** version of the Medical Application. Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

## Application Info

-   **Framework**: Django
-   **Project Name**: `medical_project`
-   **Entry Point**: `manage.py`
-   **Port**: 8000 (Default)

### Key Features
-   **Standard Structure**: Follows the standard Django project layout.
-   **Management Script**: Uses `manage.py` for administrative tasks like running the server or handling migrations.
-   **Scalability**: Built on Django's robust architecture.

## Usage Guide

### Prerequisites
Ensure you have Python installed. Install Django:

```bash
pip install django
```

### Running the Application

1.  Navigate to this directory:
    ```bash
    cd django
    ```

2.  Run the development server:
    ```bash
    python manage.py runserver
    ```

3.  Open your browser and navigate to:
    *   **App**: `http://127.0.0.1:8000`

### Project Structure
-   `manage.py`: A command-line utility that lets you interact with this Django project.
-   `medical_project/`: The actual Python package for your project.
-   `templates/`: HTML files for the frontend (configured in settings).
-   `static/`: CSS, JavaScript, and images.
