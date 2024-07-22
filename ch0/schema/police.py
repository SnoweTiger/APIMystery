from pydantic import BaseModel
from typing import Optional


class ReportSchema(BaseModel):
    id: int
    date: int
    type: str
    description: str
    city: str


class ReportFiltersSchema(BaseModel):
    date_from: Optional[int] = None
    date_to: Optional[int] = None
    type:  Optional[str] = None
    city: Optional[str] = None


class ChargeSuspectSchema(BaseModel):
    suspect_id: int
    suspect_name: str
    report_id: int


class InterviewSchema(BaseModel):
    id: int
    person_id: int
    transcript: str
