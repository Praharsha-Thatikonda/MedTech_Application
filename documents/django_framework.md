# Django Framework Documentation - MedTech AI

## 1. Overview
The Django implementation of MedTech AI serves as the robust, full-stack version of the application. It leverages Django's "batteries-included" philosophy to provide a secure, scalable web server with built-in admin capabilities.

## 2. Project Structure
```text
f_two/
├── django/
│   ├── medical_project/    # Project Configuration
│   │   ├── settings.py     # Global settings (Apps, Middleware, DB)
│   │   ├── urls.py         # Main URL routing
│   │   ├── wsgi.py         # WSGI entry point
│   │   └── asgi.py         # ASGI entry point
│   ├── db.sqlite3          # Local User/Session Database
│   ├── manage.py           # Evaluation script
│   └── templates/          # HTML Templates (Jinja2/Django Template Language)
│       ├── index.html      # Main Dashboard
│       ├── map.html        # Interactive Map
│       ├── transportation.html # Emergency Transport
│       ├── ...
```

## 3. Configuration & Setup

### Prerequisites
- Python 3.10+
- Dependencies: `django`, `sqlalchemy`, `chromadb` (for shared DBs)

### Installation
1. Navigate to the project root:
   ```bash
   cd f_two/django
   ```
2. Install dependencies (if not already installed via global requirements):
   ```bash
   pip install django
   ```

### Database Configuration
The Django app uses a **Hybrid Database Model**:
1.  **Local DB (`db.sqlite3`)**: Managed via `settings.py`. Stores User sessions, Admin users, and Auth data.
2.  **Central DB (`databases/medical_main.db`)**: Accessed via `sql_manager`. Stores read-only application data like Doctors and Hospitals.

## 4. Running the Server
To start the development server:
```bash
python manage.py runserver 8002
```
Access the application at: `http://localhost:8002/`

## 5. Key Components

### Views (`views.py`)
- **`index(request)`**: Renders the main chat interface.
- **`doctors(request)`**: Fetches doctor list from the *Central DB* and renders the directory.
- **`chat_api(request)`**: Handles AJAX POST requests from the chat interface. It acts as a bridge to the shared `llm_service.py`.

### URLs (`urls.py`)
Maps browser paths to views:
- `/` -> Index
- `/doctors` -> Doctors Directory
- `/api/chat` -> AI Chat Endpoint
- `/transportation` -> Emergency Booking

## 6. Features Implemented
- **Admin Interface**: Accessible via `/admin` (Default Django feature).
- **CSRF Protection**: Native security enabled (except on API endpoints marked `@csrf_exempt` for testing).
- **Template Inheritance**: Uses a base layout for consistent UI.
- **Static Files**: Serves CSS/JS from the global `static` directory.

## 7. Integration with Shared Services
Django imports the `backend` and `databases` modules from the parent directory by dynamically appending `sys.path`. This allows it to use:
- `llm_service`: For AI generation.
- `geo_service`: For location sorting.
- `sql_manager`: For accessing the shared doctor database.
