from jwt import encode, decode
from passlib.context import CryptContext
from time import time
# import os

# JWT_ALGORITHM = os.getenv("algorithm")
# JWT_LIFE_TIME_SEC = int(os.getenv("life_time_min")) * 60
# JWT_SECRET = os.getenv("secret")
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_LIFE_TIME_SEC = 60 * 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signJWT(id: int, name: str) -> dict[str, str]:
    expires = time() + JWT_LIFE_TIME_SEC
    payload = {"user_id": id, "expires": expires}
    token = encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"name": name, "token": token, "expires": expires}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return {}
    return decoded_token if decoded_token["expires"] >= time() else None


def hash_password(password: str) -> CryptContext:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> CryptContext:
    return pwd_context.verify(password, hashed_password)
