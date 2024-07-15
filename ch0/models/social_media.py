from sqlalchemy import Column,  Integer, String, DateTime, ForeignKey

from models.engine import Base


class FKEventCheckIn(Base):
    __tablename__ = "vk_event_checkin"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey(
        "person.id"), index=True)
