
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_CONFIG

engine = create_engine(
    url="postgresql://{0}:{1}@{2}/{3}".format(
        DB_CONFIG["user"],
        DB_CONFIG["password"],
        DB_CONFIG["host"],
        DB_CONFIG["database"],
    )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()