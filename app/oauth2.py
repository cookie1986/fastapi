'''BACKGROUND LOGIC FOR AUTHORISING USERS WITH FASTAPI'''
from http.client import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models, config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # taken from URL of login path operator

# SECRET KEY - RESIDES ON SERVER ONLY
SECRET_KEY = config.settings.SECRET_KEY

# algorithm
ALGORITHM = config.settings.ALGORITHM

# token expiry
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINS

# creates jwt token to login
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# verifies if jwt token is authentic
def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError: 
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db) # make request to database
    ):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials', headers={'WWW-Authenticate':'Bearer'})

    # sends token to be authenticated
    token = verify_access_token(token, credentials_exception)

    # returns the user id (email add in this case) if token is authentic
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user