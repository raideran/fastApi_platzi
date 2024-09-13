from routers.movie import MovieModel
from schemas.movie import Movie
from fastapi import status, HTTPException

class MovieService:

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).get(id)
        return result

    def get_movie_by_category(self, category):
        result = (
            self.db.query(MovieModel).filter(MovieModel.category == category).all()
        )
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()

    def update_movie(self, id, movie_data:Movie):
        result = self.get_movie(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie id {id} not found"
            )

        result.title = movie_data.title
        result.overview = movie_data.overview
        result.year = movie_data.year
        result.rating = movie_data.rating
        result.category = movie_data.category

        self.db.commit()

    def delete_movie(self, id):
        result = self.get_movie(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie id {id} not found"
            )

        self.db.delete(result)
        self.db.commit()