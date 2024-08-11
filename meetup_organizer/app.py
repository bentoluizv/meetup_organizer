from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meetup_organizer.routers import auth, users

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def index():
    return {'message': 'Hello World'}


app.include_router(auth.router)
app.include_router(users.router)
