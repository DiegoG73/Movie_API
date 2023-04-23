from fastapi import Depends, Path, Query
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from fastapi import APIRouter
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=15)
    overview: str = Field(min_length=2, max_length=500)
    year: int = Field(le=2025)
    rating: float = Field(ge = 0, le=10)
    category: str = Field(min_length=3, max_length=15)
    
    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Mi película',
                'overview': 'Vista previa',
                'year': 2025,
                'rating': 10,
                'category': 'Acción'
            }
        }


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=404)
def get_movie(id: int = Path(ge=1, le=9999999999999999999999)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(status_code=404, content=jsonable_encoder(result))

# Parámetros Query
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result))


# Método POST:
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": 'Se ha registrado la película'})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    MovieService(db).update_movie(id, movie)
    db.commit()
    
    return JSONResponse(status_code=200, content={"message": 'Se ha modificado la película'})
        
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró la película"})
    MovieService(db).delete_movie(id)    
    return JSONResponse(status_code=200, content={"message": 'Se ha eliminado la película'})