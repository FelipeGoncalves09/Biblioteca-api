from fastapi import FastAPI,APIRouter,HTTPException
from schemas import CreateLoan, LoanResponse
from fastapi import Depends
from database import LoanDB,get_db,UserDB
from sqlalchemy.orm import Session
from datetime import datetime
from auth import get_current_user_id

auth_router = APIRouter(prefix="/loan", tags=["loan"])

@auth_router.get("/", response_model = list[LoanResponse])
def Home(current_user_id = Depends(get_current_user_id),db:Session = Depends(get_db)):
    current_admin = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()
    if current_user_id != id:
            if current_admin.admin == False:
                raise HTTPException(status_code=403, detail="Not Autorized!")
    search =  db.query(LoanDB).all()
    return search

@auth_router.get("/me")
def MyLoans(current_user_id = Depends(get_current_user_id), db:Session = Depends(get_db)):
    search = db.query(LoanDB).filter(LoanDB.user_id == current_user_id).all()
    return search
    

@auth_router.get("/getloanlate", response_model = list[LoanResponse])
def LoanLate(current_user_id = Depends(get_current_user_id),db:Session = Depends(get_db)):
    current_admin = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()
    if current_user_id != id:
            if current_admin.admin == False:
                raise HTTPException(status_code=403, detail="Not Autorized!")
    search =  db.query(LoanDB).filter(LoanDB.return_date == None, LoanDB.expiration_date < datetime.now()).all()
    return search

@auth_router.post("/post",  response_model = LoanResponse)
def Loan_book(loan:CreateLoan,current_user_id = Depends(get_current_user_id),db:Session = Depends(get_db)):
    current_admin = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()
    if current_user_id != id:
        if current_admin.admin == False:
            raise HTTPException(status_code=403, detail="Not Autorized!")
    search = db.query(LoanDB).filter(LoanDB.book_id == loan.book_id,LoanDB.return_date == None ).first()
    if search is not None:
        raise HTTPException(status_code=409, detail="There is alreary a user that loaned this book")
    

    new_loan = LoanDB(
        user_id = loan.user_id,
        book_id = loan.book_id
    )

    db.add(new_loan)
    db.commit()

    return new_loan


@auth_router.put("/return/{id}")
def Return_book(id:int,current_user_id = Depends(get_current_user_id), db:Session = Depends(get_db)):
    current_admin = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()
    if current_admin.admin == False:
            raise HTTPException(status_code=403, detail="Not Autorized!")
    search = db.query(LoanDB).filter(LoanDB.loan_id == id).first()

    if search is None:
        raise HTTPException(status_code=404, detail="Loan not found!")
    if search.return_date is not None:
        raise HTTPException(status_code=400, detail="The book was returned successfully")

    search.return_date = datetime.now()

    db.commit()
    return {"response": "the loan return was a success!"}

