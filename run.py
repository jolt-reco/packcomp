from app import create_app
from flask_migrate import upgrade
from app.seeds import ensure_seed_data

app = create_app()

with app.app_context():
    upgrade()
    ensure_seed_data()

if __name__ == "__main__":
    app.run(port=8000)