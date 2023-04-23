from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.login import login_router

app = FastAPI()
app.title = "My Movie"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(login_router)

Base.metadata.create_all(bind=engine)

# Middleware no tan formal:
# class JWTBearer(HTTPBearer):
#     async def __call__(self, request: Request):
#         auth = await super().__call__(request)
#         data = validate_token(auth.credentials)
#         if data['email'] != 'admin@gmail.com':
#             raise HTTPException(status_code=403, detail="Credenciales no válidas")
# SE ENCUENTRA AHORA EN CARPETA MIDDLEWARES

movies = [
    {
        "id": 1,
        "title": 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven los Na´vi',
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        "id": 2,
        "title": 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven los Na´vi',
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    }
]

#Creando el primer EndPoint
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')
