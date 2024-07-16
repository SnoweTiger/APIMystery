from pydantic import BaseModel
from typing import Optional


class PersonSchema(BaseModel):
    id: int
    name: str
    license_id: int
    address_number: int
    address_street_name: str
    ssn: int


class SearchPersonSchema(BaseModel):
    name: Optional[str] = None
    license_id: Optional[int] = None
    address: Optional[str] = None
    ssn: Optional[int] = None


class DriverLicenseSchema(BaseModel):
    id: int
    age: int
    height: int
    eye_color: str
    hair_color: str
    gender: str


class SearchDriverLicenseSchema(BaseModel):
    age: Optional[int] = None
    height: Optional[int] = None
    eye_color: Optional[str] = None
    hair_color: Optional[str] = None
    gender: Optional[str] = None
