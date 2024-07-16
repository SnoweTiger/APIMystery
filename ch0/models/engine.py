from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# DB_FILE = 'api_mystery.sqlite'
DB_FILE = 'sql-murder-mystery.db'

engine = create_engine(f"sqlite:///{DB_FILE}")

Session = sessionmaker(bind=engine)

Base = declarative_base()


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
