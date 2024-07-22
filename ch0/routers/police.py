from fastapi import APIRouter, status, HTTPException, Depends

from models.engine import Session, get_db
from models.person import Person, DriverLicense
from schema.person import PersonSchema, SearchPersonSchema, DriverLicenseSchema, SearchDriverLicenseSchema, CarSchema, SearchCarSchema
from schema.police import ReportSchema, ReportFiltersSchema, InterviewSchema, ChargeSuspectSchema
from models.police import CrimeSceneReport, Interview
from auth.auth_bearer import JWTBearer


TARGET_PERSON_ID = 64562

router = APIRouter(tags=["База полиция"], dependencies=[Depends(JWTBearer())])


@router.get("/report/{date}", response_model=list[ReportSchema],
            summary='Поиск отчеты с места преступления по дате')
async def get_report_by_date(date: int, session: Session = Depends(get_db)):

    reports = session.query(CrimeSceneReport).filter(
        CrimeSceneReport.date == date).all()

    if not reports or len(reports) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reports not found")
    return reports


@router.post("/report/search", response_model=list[ReportSchema],
             summary='Поиск отчеты с места преступления по фильтрам')
async def search_report(filters: ReportFiltersSchema, session: Session = Depends(get_db)):

    if (not filters.date_from and not filters.date_to and not filters.city and not filters.type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="at least one filter must be set")

    reports = session.query(CrimeSceneReport)

    if filters.date_from:
        reports = reports.filter(CrimeSceneReport.date >= filters.date_from)
    if filters.date_to:
        reports = reports.filter(CrimeSceneReport.date <= filters.date_to)
    if filters.type:
        reports = reports.filter(CrimeSceneReport.type.contains(filters.type))
    if filters.city:
        reports = reports.filter(CrimeSceneReport.city.contains(filters.city))

    reports = reports.all()

    if not reports or len(reports) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return reports


@router.patch("/report", summary='Выдвинуть обвинение подозреваемому')
async def charge_suspect(result: ChargeSuspectSchema, session: Session = Depends(get_db)) -> dict:

    suspect = session.query(Person).get(result.suspect_id)
    if not suspect or suspect.name != result.suspect_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Не верно. Попробуйте еще раз.")

    report = session.query(CrimeSceneReport).get(result.report_id)
    if not report or report.type != 'theft' or report.date != 20251029:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Не верно. Попробуйте еще раз.")

    criminal = session.query(Person).get(TARGET_PERSON_ID)

    if suspect != criminal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Не верно. Попробуйте еще раз.")

    return {"detail": "Поздравляю! Вы поймали преступника."}


@router.get("/interview/id/{id}", response_model=InterviewSchema, summary='Получить интервью по его id')
async def get_interview_by_id(id: int, session: Session = Depends(get_db)):

    interview = session.query(Interview).get(id)

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found")
    return interview


@router.get("/interview/person/{person_id}", response_model=list[InterviewSchema], summary='Получить все интервью персонажа')
async def get_interview_by_id(person_id: int, session: Session = Depends(get_db)):

    interview = session.query(Interview).filter(
        Interview.person_id == person_id).all()

    if not interview or len(interview) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found")
    return interview


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

    if (not params.name and not params.driver_license and not params.address and not params.ssn):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="at least one filter must be set")

    query = session.query(Person)
    if params.name:
        query = query.filter(Person.name.contains(params.name))

    if params.address:
        query = query.filter(
            (Person.address_street_name.contains(params.address))
        )

    if params.driver_license:
        query = query.filter(Person.license_id == params.driver_license)

    if params.ssn:
        query = query.filter(Person.ssn == params.ssn)

    query = query.all()
    if not query or len(query) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return query


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
             summary='Найти все ВУ по критериям')
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


@router.post("/car/search", response_model=list[CarSchema],
             tags=['Авто'],
             summary='Поиск автомобиля по критериям')
async def search_car_by_filters(filters: SearchCarSchema, session: Session = Depends(get_db)):

    if (not filters.car_make and not filters.car_model and not filters.plate_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="at least one filter must be set")

    cars = session.query(
        DriverLicense.id.label('driver_license'),
        DriverLicense.car_model,
        DriverLicense.car_make,
        DriverLicense.plate_number,
    )

    if filters.plate_number:
        cars = cars.filter(
            DriverLicense.plate_number.contains(filters.plate_number))

    if filters.car_make:
        cars = cars.filter(
            DriverLicense.car_make.contains(filters.car_make))

    if filters.car_model:
        cars = cars.filter(
            DriverLicense.car_model.contains(filters.car_model))

    cars = cars.all()

    if not cars or len(cars) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver license not found")
    return cars


@router.get("/car/{plate_number}", response_model=list[CarSchema],
            tags=['Авто'],
            summary='Поиск автомобиля по номеру или его части')
async def search_car_by_plate(plate_number: str, session: Session = Depends(get_db)):

    if (not plate_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="plate number left")

    cars = session.query(
        DriverLicense.id.label('driver_license'),
        DriverLicense.car_model,
        DriverLicense.car_make,
        DriverLicense.plate_number,
    )

    cars = cars.filter(
        DriverLicense.plate_number.contains(plate_number.upper()))

    cars = cars.all()

    if not cars or len(cars) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cars not found")
    return cars
