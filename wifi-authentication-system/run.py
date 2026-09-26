"""
Entry point for local development.

    python run.py

For production, run behind a WSGI server instead, e.g.:

    gunicorn "run:app" --bind 0.0.0.0:5000
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
