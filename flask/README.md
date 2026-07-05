# Medical App - Flask Implementation

This directory contains the **Flask** version of the Medical Application. Flask is a lightweight WSGI web application framework, designed to be simple and easy to get started with.

## Application Info

-   **Framework**: Flask
-   **Templating**: Jinja2 (Built-in)
-   **Entry Point**: `app.py`
-   **Port**: 5001 (Configured to avoid conflicts with other local servers)

### Key Features
-   **Simple Routing**: clearly defined routes using the `@app.route` decorator.
-   **Direct Rendering**: Serves HTML templates directly.
-   **Lightweight**: Minimal overhead and dependencies.

## Usage Guide

### Prerequisites
Ensure you have Python installed. Install Flask:

```bash
pip install flask
```

### Running the Application

1.  Navigate to this directory:
    ```bash
    cd flask
    ```

2.  Run the application directly using Python:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to:
    *   **App**: `http://127.0.0.1:5001`

### Project Structure
-   `app.py`: The main application file containing all route definitions and logic.
-   `templates/`: HTML files for the frontend.
-   `static/`: CSS, JavaScript, and images.
