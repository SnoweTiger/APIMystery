from sqlalchemy import Column,  Integer, String, DateTime, ForeignKey

from models.engine import Base


class Membership(Base):
    __tablename__ = "membership"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey(
        "person.id"), index=True)


class CheckIn(Base):
    __tablename__ = "membership"

    id = Column(Integer, primary_key=True, index=True)
    checkIn = Column(DateTime, nullable=False)
    checkOut = Column(DateTime, nullable=False)

    membership = Column(Integer, ForeignKey(
        "membership.id"), index=True)
