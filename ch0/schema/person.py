from pydantic import BaseModel
from typing import Optional


class PersonSchema(BaseModel):
    id: int
    name: str
    license_id: Optional[int] = None
    address_number: int
    address_street_name: str
    ssn: Optional[int] = None


class SearchPersonSchema(BaseModel):
    name: Optional[str] = None
    driver_license: Optional[int] = None
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


class SearchCarSchema(BaseModel):
    plate_number: Optional[str] = None
    car_make: Optional[str] = None
    car_model: Optional[str] = None


class CarSchema(BaseModel):
    plate_number: str
    car_make: str
    car_model: str
    driver_license: int
