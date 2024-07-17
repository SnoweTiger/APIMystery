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
    name: Optional[str] = None


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
