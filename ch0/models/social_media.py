from sqlalchemy import Column, Integer, String, ForeignKey

from models.engine import Base


class CakebookEventCheckIn(Base):
    __tablename__ = "cakebook_event_checkin"

    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    date = Column(Integer, nullable=False)

    person_id = Column(Integer, ForeignKey("person.id"))
