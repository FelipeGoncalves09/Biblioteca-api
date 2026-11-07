from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas import CreateBook, CreateUser, UserResponse, UpdateUser, LoginUser
from database import UserDB, get_db
from auth import create_access_token, get_current_user_id

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router = APIRouter(prefix="/users", tags=["users"])


# --- lista todos os usuarios ---
@auth_router.get("/", response_model=list[UserResponse])
def home(db: Session = Depends(get_db)):
    search = db.query(UserDB).all()
    return search


# --- cadastra um usuario novo ---
@auth_router.post("/post", response_model=UserResponse)
def CriarUsuario(user: CreateUser, db: Session = Depends(get_db)):
    # --- a senha nunca é salva pura, so o hash ---
    hashed_password = pwd_context.hash(user.password)
    new_user = UserDB(
        name=user.name,
        hashed_password=hashed_password,
        #admin = user.admin
    )
    db.add(new_user)
    db.commit()
    return new_user


# --- login: confere a senha e devolve o token ---
@auth_router.post("/login")
def LogarUsuario(user: LoginUser, db: Session = Depends(get_db)):
    search = db.query(UserDB).filter(UserDB.name == user.name).first()
    if search is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # --- compara a senha digitada com o hash salvo no banco ---
    password_check = pwd_context.verify(user.password, search.hashed_password)
    if not password_check:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # --- cria o token guardando o id de quem logou ---
    token = create_access_token({"user_id": search.user_id})
    return {"token": token, "token_type": "bearer"}


# --- apaga um usuario (so a propria conta) ---
@auth_router.delete("/delete/{id}/")
def DeletarUsuario(id: int, current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # --- o id do token tem que ser o mesmo id da rota ---
    if current_user_id != id:
        raise HTTPException(status_code=403, detail="You can only delete you account!")

    print("ID recebido:", id, "tipo:", type(id))

    search = db.query(UserDB).filter(UserDB.user_id == id).first()
    if search is None:
        raise HTTPException(status_code=404, detail="user not found")

    db.delete(search)
    db.commit()
    return {"msg": "usuario_apagado"}


# --- atualiza um usuario (so a propria conta) ---
@auth_router.put("/put/{id}", response_model=UserResponse)
def AtualizarUsuario(id: int, user: UpdateUser, current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # --- o id do token tem que ser o mesmo id da rota ---
    if current_user_id != id:
        raise HTTPException(status_code=403, detail="Tou can only update you account!")

    search = db.query(UserDB).filter(UserDB.user_id == id).first()
    if search is None:
        raise HTTPException(status_code=404, detail="user not found")

    temporary_user = search

    search.name = user.name
    search.password = user.password

    if search is None:
        raise HTTPException(status_code=404, detail="user not found")

    db.commit()

    return temporary_user