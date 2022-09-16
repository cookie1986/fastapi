from passlib.context import CryptContext

# for generating password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

# for verifying password matches stored hashed password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)