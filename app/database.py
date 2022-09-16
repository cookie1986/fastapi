'''CREATES DB, IF IT DOESN'T ALREADY EXIST'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# old - code for connecting to database using raw sql instead of sqalchemy
# while True:
#     try:
#         conn =  psycopg2.connect(
#             host = 'localhost', 
#             database='fastapi', 
#             user='postgres', 
#             password='dc8294dc8294!!', 
#             cursor_factory=RealDictCursor
#             )
#         cursor = conn.cursor()
#         print("successfully connected to database")
#         break

#     except Exception as error:
#         print("connecting to database failed")
#         print("the error was: ", error)
#         time.sleep(2)