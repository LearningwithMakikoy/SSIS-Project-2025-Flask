from app import create_app
from app.database import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("✅ PostgreSQL connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", e)
