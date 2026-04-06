import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "analytics_db")
    user = os.getenv("DB_USER", "analytics_user")
    password = os.getenv("DB_PASSWORD", "analytics_pass")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(url)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()