from sqlalchemy import Column,  Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.engine import Base


class Membership(Base):
    __tablename__ = "get_fit_now_member"

    id = Column(String, primary_key=True, index=True)
    membership_start_date = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    membership_status = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey(
        "person.id"), index=True)

    check_ins = relationship("CheckIn")


class CheckIn(Base):
    __tablename__ = "get_fit_now_check_in"
    id = Column(Integer, primary_key=True, index=True)
    check_in_date = Column(Integer, nullable=False)
    check_in_time = Column(Integer, nullable=False)
    check_out_time = Column(Integer, nullable=False)

    membership_id = Column(String, ForeignKey("get_fit_now_member.id"))
