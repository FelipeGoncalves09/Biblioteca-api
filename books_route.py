from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import CreateBook, UpdateBook, BookResponse,ShowResponse
from database import BookDB, get_db, UserDB, LoanDB
from google_book_api import buscar_livro
from auth import get_current_user_id

auth_router = APIRouter(prefix="/books", tags=["books"])

# --- Lista todos os livros com o status de disponibilidade ---
@auth_router.get("/", response_model=list[ShowResponse])
def livros(db: Session = Depends(get_db)):
    search = db.query(BookDB).all()

    # --- Empréstimos sem data de devolução são os livros que ainda estão emprestados ---
    search_available = db.query(LoanDB).filter(LoanDB.return_date == None).all()

    # --- Guarda só os ids dos livros emprestados---
    book_id_loan = set()
    for loaned in search_available:
        book_id_loan.add(loaned.book_id)

    # --- Cria a resposta ---
    resposta = []
    for livro in search:
        resposta.append({
            "book_id": livro.book_id,
            "name": livro.name,
            "author": livro.author,
            "available": livro.book_id not in book_id_loan,
            "synopsis": livro.synopsis
        })

    return resposta


# --- Adiciona um livro (somente admin) ---
@auth_router.post("/post", response_model=BookResponse)
async def Adicionar_livro(book: CreateBook, current_user_id=Depends(get_current_user_id), db: Session = Depends(get_db)):
    current_admin = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()

    if current_user_id != id:
        if current_admin.admin == False:
            raise HTTPException(status_code=403, detail="Not autorized!")

        # --- Busca os dados do livro na API externa com base no título ---
        titulo, autor, sinopse, capa = await buscar_livro(book.title)
        new_book = BookDB(
            name=titulo,
            author=autor,
            synopsis=sinopse,
            cover_url=capa
        )

    # --- Se a API não encontrar o livro, nao vai salvar ---
    if titulo is None:
        raise HTTPException(status_code=404, detail="Book not found!")

    db.add(new_book)
    db.commit()
    return new_book


# --- Atualiza um livro existente (somente admin) ---
@auth_router.put("/update/{id}", response_model=BookResponse)
def Put_user(id: int, book: UpdateBook, current_user_id=Depends(get_current_user_id), db: Session = Depends(get_db)):
    current_user = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()

    if current_user.admin == False:
        raise HTTPException(status_code=403, detail="NOT AUTHORIZED!")

    search = db.query(BookDB).filter(BookDB.book_id == id).first()
    if search is None:
        raise HTTPException(status_code=404, detail="Book not found")

    search.name = book.name
    search.author = book.author
    search.loaned = book.loaned
    db.commit()
    return search


# --- Apaga um livro (somente admin) ---
@auth_router.delete("/delete/{id}")
def Delete_user(id: int, current_user_id=Depends(get_current_user_id), db: Session = Depends(get_db)):
    current_user = db.query(UserDB).filter(UserDB.user_id == current_user_id).first()

    if current_user.admin == False:
        raise HTTPException(status_code=403, detail="NOT AUTHORIZED!")

    search = db.query(BookDB).filter(BookDB.book_id == id).first()
    if search is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(search)
    db.commit()
    return {"msg": "LIVRO APAGADO COM SUCESSO"}