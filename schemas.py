from pydantic import BaseModel
from datetime import datetime



#USUARIO -----------------------------------------------------------

class CreateUser(BaseModel):
        name: str
        password: str

        class Config:
            from_attributes = True

class LoginUser(BaseModel):
        name: str
        password: str
        
        
        class Config:
            from_attributes = True
     

class UserResponse(BaseModel):
        name: str
        user_id:int

        class Config:
            from_attributes = True

class DeleteUser (BaseModel):
        user_id: int

class UpdateUser (BaseModel):
    name: str
    password: str
     
    class Config:
        from_attributes = True

# Livro -----------------------------------------------------------------


class CreateBook(BaseModel):
    title: str
    

class UpdateBook(BaseModel):
    name: str
    author: str
    loaned: bool


class BookResponse(BaseModel):
    name: str
    author: str
    synopsis: str | None = None
    cover_url: str | None = None

class ShowResponse(BaseModel):
    name: str
    author: str
    book_id: int
    synopsis: str | None = None
    cover_url: str | None = None
    available: bool
    
    

# EMPRESTAR -------------------------------------------------------------
class CreateLoan(BaseModel):
    user_id: int
    book_id: int

    class Config:
        from_attributes = True

class LoanResponse(BaseModel):
    loan_id: int
    loan_date: datetime
    return_date: datetime | None
    expiration_date: datetime
    user_id: int
    book_id: int
    class Config:
        from_attributes = True
