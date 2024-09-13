from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


app = FastAPI()

# 127.0.0.1:5000/docs
app.title = "My first fast api app"
app.version = "0.0.1"

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


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return None


@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str):
    return list(filter(lambda x: x["category"].lower() == category.lower(), movies))


@app.post("/movies", tags=["movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    movies.append(
        {
            "id": id,
            "title": title,
            "overview": overview,
            "year": year,
            "rating": rating,
            "category": category,
        }        
    )
    return {"message": f"Movie {title} added successfully"}


@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    for movie in movies:
        if movie["id"] == id:
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating
            movie["category"] = category            
            
    return {"message": f"Movie {title} updated successfully"}
    

@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
           movies.remove(movie)
            
    return {"message": f"Movie deleted successfully"}
    