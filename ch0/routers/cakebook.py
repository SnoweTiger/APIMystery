from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, status, Depends, Request

from models.engine import Session, get_db
from models.social_media import CakebookEventCheckIn
from schema.cakebook import EventSchema, EventFilterSchema


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


router = APIRouter(tags=["Социальная сеть Cakebook"],
                   dependencies=[Depends(Token())])


@router.get("/event/{event_id}",
            response_model=EventSchema,
            summary='Получить событие по его id')
async def get_event_by_id(event_id: int, session: Session = Depends(get_db)):
    try:
        event = session.query(CakebookEventCheckIn).filter(
            CakebookEventCheckIn.event_id == event_id).first()

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="event id must be int")


@router.get("/events/{person_id}",
            response_model=list[EventSchema],
            summary='Получить 10 последних событий пользователя')
async def get_last_user_events(person_id: int, session: Session = Depends(get_db)):
    try:
        events = session.query(CakebookEventCheckIn).filter(
            CakebookEventCheckIn.person_id == person_id).all()

        if not events or len(events) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
        return events

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="person_id must be int")


@router.post("/events",
             response_model=list[EventSchema],
             summary='Получить все события пользователя согласно критериям в теле')
async def get_filtered_user_events(filters: EventFilterSchema, session: Session = Depends(get_db)):

    events = session.query(CakebookEventCheckIn).filter(
        CakebookEventCheckIn.person_id == filters.person_id
    )
    if filters.event_name:
        events = events.filter(
            CakebookEventCheckIn.event_name.contains(filters.event_name))
    if filters.start_date:
        events = events.filter(CakebookEventCheckIn.date >= filters.start_date)
    if filters.end_date:
        events = events.filter(CakebookEventCheckIn.date <= filters.end_date)

    events = events.all()
    if not events or len(events) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
    return events
