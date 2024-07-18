from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, status, Depends, Request

from models.engine import Session, get_db
from models.get_fit_now import Membership, CheckIn
from schema.get_fit_now import MembershipOutSchema, SearchMembershipSchema, CheckInFullSchema, SearchCheckInSchema


API_TOKEN = 'd901050d-07ec-4990-a05c-ab2178e2e09c'


class Token(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Token, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            if not self.verify_token(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def verify_token(self, token: str) -> bool:
        isTokenValid: bool = False
        if token == API_TOKEN:
            isTokenValid = True
        return isTokenValid


router = APIRouter(tags=["GetFitNow"], dependencies=[Depends(Token())])


@router.get("/membership/{id}",
            response_model=MembershipOutSchema,
            summary='Получить членство в клубе по его id')
async def get_membership_by_id(id: str, session: Session = Depends(get_db)):

    event = session.query(Membership).filter(Membership.id == id).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.post("/membership",
             response_model=list[MembershipOutSchema],
             summary='Найти членство в клубе по персонажу')
async def get_membership_by_person(filter: SearchMembershipSchema, session: Session = Depends(get_db)):

    event = session.query(Membership)

    if not filter.person_id and not filter.person_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request must contains person_id or person_name")

    event = session.query(Membership)

    if filter.person_id:
        event = event.filter(Membership.person_id == filter.person_id)
    else:
        event = event.filter(Membership.name.contains(filter.person_name))

    event = event.all()
    if not event or len(event) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.get("/checkin/{id}",
            response_model=CheckInFullSchema,
            summary='Поиск регистрации члена клуба по критериям в теле')
async def get_check_in_by_date(id: int, session: Session = Depends(get_db)):

    check_ins = session.query(CheckIn).get(id)

    if not check_ins:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Check in not found")
    return check_ins


@router.post("/checkin",
             response_model=list[CheckInFullSchema],
             summary='Поиск зарегистрированных членов клуба по критериям в теле')
async def get_check_in_by_date(filter: SearchCheckInSchema, session: Session = Depends(get_db)):

    check_ins = session.query(CheckIn)

    check_ins = check_ins.filter(
        CheckIn.check_in_date == filter.check_in_date)

    if filter.from_time:
        check_ins = check_ins.filter(
            (CheckIn.check_in_time >= filter.from_time) |
            (CheckIn.check_out_time >= filter.from_time)
        )

    if filter.to_time:
        check_ins = check_ins.filter(
            (CheckIn.check_in_time <= filter.to_time) |
            (CheckIn.check_out_time <= filter.to_time)
        )

    check_ins = check_ins.all()
    if not check_ins or len(check_ins) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Check in not found")
    return check_ins
