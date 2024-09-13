from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Session, engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()


# SQLModel es una alternativa del creador de FastAPI a SQLAlchemy

# 127.0.0.1:5000/docs
app.title = "My first fast api app"
app.version = "0.0.1"


app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)



# uvicorn main:app --reload --port 5000 --host 0.0.0.0


@app.get("/", tags=["home"])
def home():
    return HTMLResponse("<h1> Hello World! </h1>")





