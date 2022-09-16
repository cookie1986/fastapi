from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote


# models.Base.metadata.create_all(bind=engine) # NOT NEEDED IF CREATED TABLES THROUGH ALEMBIC

app = FastAPI()

# list of domains that can talk to API
origins = [
    "https://www.google.com"
    ]

app.middleware(
    CORSMiddleware,
    allow_origins=[], # what domains are allowed to talk to API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Welcome to my test root API!!!!"}