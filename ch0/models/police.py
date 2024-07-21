from sqlalchemy import Column, Integer, String, ForeignKey

from models.engine import Base


class CrimeSceneReport(Base):
    __tablename__ = "crime_scene_report"

    date = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    city = Column(String, nullable=False)


class Interview(Base):
    __tablename__ = "interview"

    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey(
        "person.passport"), nullable=False)


# class Judge(Base):
#     __tablename__ = "judge"

#     id = Column(Integer, primary_key=True, index=True)
#     user = Column(Integer, nullable=False)
#     value = Column(String, nullable=False)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
