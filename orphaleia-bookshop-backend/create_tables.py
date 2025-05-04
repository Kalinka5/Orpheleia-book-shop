import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.session import engine
from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal

def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    # Initialize database with seed data
    db = SessionLocal()
    try:
        print("Initializing database with seed data...")
        init_db(db)
        print("Database initialized successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    main() 