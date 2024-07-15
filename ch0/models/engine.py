from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///api_mystery.sqlite")

Session = sessionmaker(bind=engine)

Base = declarative_base()


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
