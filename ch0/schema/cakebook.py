from pydantic import BaseModel
from typing import Optional


class EventSchema(BaseModel):
    event_id: int
    person_id: int
    date: int
    event_name: str


class EventFilterSchema(BaseModel):
    person_id: int
    start_date: Optional[int] = None
    end_date: Optional[int] = None
    event_name: Optional[str] = None
