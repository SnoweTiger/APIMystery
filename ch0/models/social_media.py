from sqlalchemy import Column,  Integer, String, DateTime, ForeignKey

from models.engine import Base


class FacebookEventCheckIn(Base):
    __tablename__ = "facebook_event_checkin"

    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    date = Column(Integer, nullable=False)

    person_id = Column(Integer, ForeignKey("person.id"))
