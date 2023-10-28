from sqlalchemy import create_engine, Engine

from backend.database.dsn import build_dsn

def get_db() -> Engine:
    return create_engine(build_dsn())
