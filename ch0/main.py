from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def start():
    uvicorn.run('main:app', host='localhost', port=5000, reload=True)


# Run the API with uvicorn
if __name__ == "__main__":
    start()
