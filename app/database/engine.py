from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = "postgresql://slm_user:slm@127.0.0.1:5432/slm-db"

engine = create_engine(
    POSTGRES_URL, pool_pre_ping=True, connect_args={"options": "-c timezone=utc"}
)
session = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)
