from fastapi import FastAPI,APIRouter,HTTPException
from schemas import CreateBook, CreateUser, UserResponse, UpdateUser,LoginUser
from fastapi import Depends
from database import UserDB,get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import create_access_token,get_current_user_id

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
auth_router = APIRouter(prefix="/users", tags=["users"])

@auth_router.get("/")
def home(db:Session = Depends(get_db)):
    search = db.query(UserDB).all()
    return search

@auth_router.post("/post", response_model = UserResponse)
def CriarUsuario (user:CreateUser, db:Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = UserDB (
       name = user.name,
       hashed_password = hashed_password,
       #admin = user.admin   
    )

    db.add(new_user)
    db.commit()
    return new_user

@auth_router.post("/login")
def LogarUsuario(user:LoginUser, db:Session = Depends(get_db)):
    search = db.query(UserDB).filter(UserDB.name == user.name).first()

    password_check = pwd_context.verify(user.password,search.hashed_password)

    if not password_check:
        raise HTTPException(status_code=403,detail="wrong password")
    token = create_access_token({"user_id": search.user_id})
    return {"token": token, "token_type": "bearer" }


    # pesquisar o usuario com o schema, validar,
# fazer a checagem do hash da senha, validar com if not variavel,
#  criar acesso de token passando o id do usuario com o search.user_id num dicionario



@auth_router.delete("/delete/{id}/")
def DeletarUsuario(id:int,current_user_id:int = Depends(get_current_user_id), db:Session = Depends(get_db)):
    if current_user_id != id:
        raise HTTPException(status_code=403,detail= "You can only delete you account!")
    print("ID recebido:", id, "tipo:", type(id))
    search = db.query(UserDB).filter(UserDB.user_id == id).first()
    if search is None:
        raise HTTPException(status_code="404", detail="user not found")
    
    db.delete(search)
    db.commit()
    return {"msg": "usuario_apagado"}

@auth_router.put("/put/{id}",response_model = UserResponse)
def AtualizarUsuario(id:int,user:UpdateUser,current_user_id:int = Depends(get_current_user_id), db:Session = Depends(get_db)):
    if current_user_id != id:
        raise HTTPException(status_code=403, detail="Tou can only update you account!")
    search = db.query(UserDB).filter(UserDB.user_id == id).first()

    temporary_user = search

    search.name = user.name
    search.password = user.password

    if search is None:
        raise HTTPException(status_code="404", detail="user not found")

    db.commit()

    return temporary_user

#ADICIONAR A FUNÇAO TOKEN NESSA ROTA
#PROXIMO PASSO