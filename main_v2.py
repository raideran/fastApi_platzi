from fastapi import FastAPI, Body, Path, Query, status, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# 127.0.0.1:5000/docs
app.title = "My first fast api app"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    # id: int | None = None
    id: Optional[int] = None
    # title: str = Field(default="Mi película", min_length=5, max_length=15)
    # overview: str = Field(default="Descripción de la película", min_length=15, max_length=50)
    # year: int = Field(default=2022, le=2022)
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi Película",
                "overview": "Desc de la película",
                "year": 2022,
                "rating": 5,
                "category": "Acción",
            }
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción",
    },
    {
        "id": 2,
        "title": "Freddy",
        "overview": "Malo en el barrio",
        "year": "1980",
        "rating": 6.5,
        "category": "Horror",
    },
]

# uvicorn main:app --reload --port 5000 --host 0.0.0.0


@app.get("/", tags=["home"])
def home():
    return HTMLResponse("<h1> Hello World! </h1>")


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)


@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends((JWTBearer()))])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).get(id)
    # for item in movies:
    #     if item["id"] == id:
    #         return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie id {id} not found")
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    # return JSONResponse(content=[], status_code=status.HTTP_404_NOT_FOUND)
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie id {id} not found")


@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    data = list(filter(lambda x: x["category"].lower() == category.lower(), movies))
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    # movies.append(movie.model_dump())
    response = {"message": f"Movie {movie.title} added successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id: int, movie_data: Movie) -> dict:
    for movie in movies:        
        if movie["id"] == id:
            movie["title"] = movie_data.title
            movie["overview"] = movie_data.overview
            movie["year"] = movie_data.year
            movie["rating"] = movie_data.rating
            movie["category"] = movie_data.category

    response = {"message": f"Movie {movie_data.title} updated successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
    response = {"message": f"Movie deleted successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
