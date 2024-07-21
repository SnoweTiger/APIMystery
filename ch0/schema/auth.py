from pydantic import BaseModel
from datetime import datetime


class LoginSchema(BaseModel):
    login: str
    password: str


class LoginResponseSchema(BaseModel):
    name: str
    token: str
    expires: datetime
