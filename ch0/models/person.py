from sqlalchemy import Column, Integer, String, ForeignKey

from models.engine import Base


class DriverLicense(Base):
    __tablename__ = "drivers_license"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

    eye_color = Column(String, nullable=False)
    hair_color = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    plate_number = Column(String, nullable=False)
    car_make = Column(String, nullable=False)
    car_model = Column(String, nullable=False)


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_id = Column(Integer, ForeignKey("drivers_license.id"))
    address_number = Column(Integer, nullable=False)
    address_street_name = Column(String, nullable=False)
    ssn = Column(Integer, unique=True, nullable=False)


class Income(Base):
    __tablename__ = "income"

    ssn = Column(Integer, ForeignKey("person.ssn"), primary_key=True)
    annual_income = Column(Integer, nullable=False)
