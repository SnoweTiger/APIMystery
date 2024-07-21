from fastapi import APIRouter, status, HTTPException, Depends

from models.engine import Session, get_db
from models.police import Users
from schema.auth import LoginSchema, LoginResponseSchema
from auth.auth_handler import verify_password, signJWT, hash_password
from auth.auth_bearer import JWTBearer

router = APIRouter(tags=["Авторизация полиция"])


@router.post("/login", response_model=LoginResponseSchema)
async def login(login_user: LoginSchema, session: Session = Depends(get_db)):
    try:
        user = session.query(Users).filter(
            Users.login == login_user.login).scalar()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="1Not valid Login or Password")

        if not verify_password(password=login_user.password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="2Not valid Login or Password")

        return signJWT(id=user.id, name=user.login)

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Non valid Login or Password")


@router.post("/user", status_code=status.HTTP_201_CREATED,  dependencies=[Depends(JWTBearer())])
async def create_user(user: LoginSchema,  session: Session = Depends(get_db)):
    users = session.query(Users).all()
    logins = [u.login for u in users]
    if user.login in logins:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Login must be unique")
    try:
        new_user = Users(
            login=user.login,
            password=hash_password(user.password)
        )
        session.add(new_user)
        session.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error create user")
