from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from user_route import auth_router
app.include_router(auth_router)

from books_route import auth_router
app.include_router(auth_router)

from loan_route import auth_router
app.include_router(auth_router)



origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

