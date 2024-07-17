from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, status, Depends, Request


from models.get_fit_now import Membership, CheckIn
from models.engine import Session, get_db
from schema.get_fit_now import MembershipOutSchema, MembershipSchema, CheckInSchema

API_TOKEN = 'd901050d-07ec-4990-a05c-ab2178e2e09c'


class Token(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Token, self).__call__(request)
        if credentials:
            # if not credentials.scheme == "Bearer":
            #     raise HTTPException(
            #         status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
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
            summary='Получить событие по его id')
async def get_membership_by_id(id: str, session: Session = Depends(get_db)):
    event = session.query(Membership).filter(Membership.id == id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event
