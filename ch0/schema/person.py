from pydantic import BaseModel


class PersonSchema(BaseModel):
    id: int
    name: str
    license_id: int
    address_number: int
    address_street_name: str
    ssn: int
