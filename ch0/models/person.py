from sqlalchemy import Column,  Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from models.engine import Base


class DriverLicense(Base):
    __tablename__ = "driver_license"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

    eye_color = Column(String, nullable=False)
    hair_color = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    # person = relationship("Person", viewonly=True)


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    registration_plate = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)

    driver_license_id = Column(Integer, ForeignKey("driver_license.id"))


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    passport = Column(Integer, unique=True, nullable=False)
    address_number = Column(Integer, nullable=False)
    address_street = Column(String, nullable=False)

    driver_license_id = Column(Integer, ForeignKey("driver_license.id"))


class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    passport = Column(Integer, ForeignKey(
        "person.passport"), nullable=False)
    annual_income = Column(Float, nullable=False)
