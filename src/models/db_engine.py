import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.consts import DB_DIR, ACTORS_DB_FILE

DB_PATH = os.path.join(os.path.dirname(__file__), "..", DB_DIR, ACTORS_DB_FILE)
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
