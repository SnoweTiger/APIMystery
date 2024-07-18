from pydantic import BaseModel
from typing import Optional


class MembershipSchema(BaseModel):
    id: str
    person_id: int
    name: str
    membership_start_date: int
    membership_status: str


class SearchMembershipSchema(BaseModel):
    person_id: Optional[int] = None
    person_name: Optional[str] = None


class SearchCheckInSchema(BaseModel):
    check_in_date: int
    from_time: Optional[int] = None
    to_time: Optional[int] = None


class CheckInSchema(BaseModel):
    check_in_date: int
    check_in_time: int
    check_out_time: int


class CheckInFullSchema(CheckInSchema):
    membership_id: str


class MembershipOutSchema(MembershipSchema):
    check_ins: list[Optional[CheckInSchema]]

    class Config:
        orm_mode = True
