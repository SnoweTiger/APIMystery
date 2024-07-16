from fastapi import APIRouter, HTTPException, status, Depends

# from auth.auth_bearer import JWTBearer
from models import Person
from models.engine import Session, get_db
import schema

# router = APIRouter(tags=["Client"], dependencies=[Depends(JWTBearer())])
router = APIRouter(tags=["Police"])


@router.get("/person/all", response_model=list[schema.PersonSchema])
async def get_all_persons(session: Session = Depends(get_db)):
    persons = session.query(Person).limit(10).all()
    return persons


@router.get("/person/bySSN/{ssn}", response_model=list[schema.PersonSchema])
async def get_persons_by_ssn(ssn: int, session: Session = Depends(get_db)):
    persons = session.query(Person).filter(Person.ssn == ssn).all()
    return persons


# @router.post("/person/search", response_model=list[schema.PersonSchema])
# async def search_persons(session: Session = Depends(get_db)):
#     persons = session.query(Person).all()
#     return persons
