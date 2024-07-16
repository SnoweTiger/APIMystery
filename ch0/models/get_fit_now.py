from sqlalchemy import Column,  Integer, String, DateTime, ForeignKey

from models.engine import Base


class Member(Base):
    __tablename__ = "get_fit_now_member"

    id = Column(Integer, primary_key=True, index=True)
    membership_start_date = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    membership_status = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey(
        "person.id"), index=True)


class CheckIn(Base):
    __tablename__ = "get_fit_now_check_in"

    id = Column(Integer, primary_key=True, index=True)
    check_id_date = Column(Integer, nullable=False)
    check_id_time = Column(Integer, nullable=False)
    check_out_date = Column(Integer, nullable=False)

    membership_id = Column(Integer, ForeignKey(
        "get_fit_now_member.id"), index=True)
