from fastapi import APIRouter, status, HTTPException, Depends

from models.engine import Session, get_db
from models.person import Person, DriverLicense
from schema.person import PersonSchema, SearchPersonSchema, DriverLicenseSchema, SearchDriverLicenseSchema

# router = APIRouter(tags=["Client"], dependencies=[Depends(JWTBearer())])
router = APIRouter(tags=["База полиция"])


@router.get("/person/all", response_model=list[PersonSchema],
            tags=['Персонаж'],
            summary='Получить всех персонажей')
async def get_all_persons(session: Session = Depends(get_db)):

    persons = session.query(Person).limit(10).all()

    if not persons or len(persons) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return persons


@router.get("/person/ssn/{ssn}", response_model=PersonSchema,
            tags=['Персонаж'],
            summary='Получить персонажа по его SSN')
async def get_persons_by_ssn(ssn: int, session: Session = Depends(get_db)):

    persons = session.query(Person).filter(Person.ssn == ssn).first()

    if not persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return persons


@router.post("/person/search", response_model=list[PersonSchema],
             tags=['Персонаж'],
             summary='Получить персонажа по критериям в теле запроса')
async def search_persons(params: SearchPersonSchema, session: Session = Depends(get_db)):

    if (not params.name and not params.license_id and not params.address and not params.ssn):
        return []

    query = session.query(Person)
    if params.name:
        query = query.filter(Person.name.contains(params.name))

    if params.address:
        query = query.filter(
            (Person.address_street_name.contains(params.address))
        )

    if params.license_id:
        query = query.filter(Person.license_id == params.license_id)

    if params.ssn:
        query = query.filter(Person.ssn == params.ssn)

    if not query or len(query) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return query.all()


@router.get("/driver_license/all", response_model=list[DriverLicenseSchema],
            tags=['Водительские удостоверения'],
            summary='Получить все ВУ')
async def get_all_driver_licenses(session: Session = Depends(get_db)):

    query = session.query(DriverLicense).limit(10).all()

    if not query or len(query) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver license not found")
    return query


@router.get("/driver_license/{driver_license_id}", response_model=DriverLicenseSchema,
            tags=['Водительские удостоверения'],
            summary='Получить ВУ по его номеру')
async def get_driver_license_by_id(driver_license_id: int, session: Session = Depends(get_db)):

    query = session.query(DriverLicense).get(driver_license_id)

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver license not found")
    return query


@router.post("/driver_license/search", response_model=list[DriverLicenseSchema],
             tags=['Водительские удостоверения'],
             summary='Найти все ВУ по критериям в теле запроса')
async def search_driver_license(params: SearchDriverLicenseSchema, session: Session = Depends(get_db)):

    if (
        not params.age and not params.height and
        not params.eye_color and not params.hair_color and
        not params.gender
    ):
        return []

    query = session.query(DriverLicense)
    if params.age:
        query = query.filter(DriverLicense.age == params.age)

    if params.height:
        query = query.filter(DriverLicense.height == params.height)

    if params.eye_color:
        query = query.filter(DriverLicense.eye_color == params.eye_color)

    if params.hair_color:
        query = query.filter(DriverLicense.hair_color == params.hair_color)

    if params.gender:
        query = query.filter(DriverLicense.gender == params.gender)

    if not query or len(query) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver license not found")
    return query.all()
