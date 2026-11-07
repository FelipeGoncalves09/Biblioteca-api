from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  


# --- Configuração de hash de senha ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Configuração do JWT ---
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Diz ao FastAPI onde fica a rota de login, pra ele saber pedir o token no /docs ---
security_scheme = HTTPBearer()

# --- Fábrica de Token ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Leitor de Token: usado como "porteiro" nas rotas protegidas ---
def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #pq codificar e decodificar no jwt?
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")