from sqlalchemy import Column,  Integer, String, DateTime, ForeignKey

from models.engine import Base


class CrimeSceneReport(Base):
    __tablename__ = "crime_scene_report"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, nullable=False)
    type = Column(String, nullable=False)
    city = Column(String, nullable=False)
    text = Column(String, nullable=False)


class Interrogation(Base):
    __tablename__ = "interrogation"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)

    passport = Column(Integer, ForeignKey(
        "person.passport"), nullable=False)


class Judge(Base):
    __tablename__ = "judge"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, nullable=False)
    value = Column(String, nullable=False)
