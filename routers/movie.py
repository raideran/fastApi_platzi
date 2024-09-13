from fastapi import APIRouter
from fastapi import Path, Query, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends((JWTBearer()))],
)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(
        content=jsonable_encoder(result), status_code=status.HTTP_200_OK
    )


@movie_router.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie id {id} not found"
        )
    return JSONResponse(
        content=jsonable_encoder(result), status_code=status.HTTP_200_OK
    )


@movie_router.get(
    "/movies/",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(
        content=jsonable_encoder(result), status_code=status.HTTP_200_OK
    )


@movie_router.post(
    "/movies", tags=["movies"], response_model=dict, status_code=status.HTTP_201_CREATED
)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)        
    response = {"message": f"Movie {movie.title} added successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@movie_router.put(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK
)
def update_movie(id: int, movie_data: Movie) -> dict:
    db = Session()
    MovieService(db).update_movie(id, movie_data)
    response = {"message": f"Movie {movie_data.title} updated successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@movie_router.delete(
    "/movies/{id}", tags=["movies"], response_model=dict, status_code=status.HTTP_200_OK
)
def delete_movie(id: int) -> dict:
    db = Session()
    MovieService(db).delete_movie(id)
    response = {"message": f"Movie deleted successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
