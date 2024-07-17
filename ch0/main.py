from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models.engine import Base, engine
from models import CakebookEventCheckIn
from models.engine import Session, get_db
from sqlalchemy import insert

import routers

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    # "http://192.168.0.110:5000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"message": "pong"}

app.include_router(routers.police, prefix="/police/api")
app.include_router(routers.cakebook, prefix="/cakebook/api")


def start():
    uvicorn.run('main:app', host='localhost', port=5000, reload=True)


# Run the API with uvicorn
if __name__ == "__main__":

    start()
