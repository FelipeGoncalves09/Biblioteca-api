from sqlalchemy import  Float,Integer, Boolean, String,Column, create_engine,delete,ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker,declarative_base,Session,relationship
from datetime import datetime, timedelta, timezone

DATABASE_URL = "sqlite:///./biblioteca.db" # O BANCO VAI RODAR NA PASTA LOCAL "///"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # cria, conversa e traduz para o banco de dados
local_session = sessionmaker(bind=engine)

base = declarative_base()

class UserDB(base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    user_order  = relationship("LoanDB", back_populates="user")

class BookDB(base):
    __tablename__ = "books"

    book_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, default="unknown")
    book_order = relationship("LoanDB", back_populates="book")

class LoanDB(base):
    __tablename__ = "loan"
    loan_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    loan_date = Column(DateTime,nullable=False, default=datetime.now)
    return_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=False, default=lambda:datetime.now() + timedelta(days=15))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer,ForeignKey("books.book_id"))
    user = relationship("UserDB", back_populates="user_order")
    book = relationship("BookDB", back_populates="book_order")


base.metadata.create_all(bind=engine)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

        #amanha terminar o banco, contruir o main e os schemas

        
