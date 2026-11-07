from main import app
from fastapi.testclient import TestClient
import random
from auth import create_access_token,get_current_user_id
client = TestClient(app)

#  funçao que finge que o admin de id 1 está logado
def admin_falso():
    return 1   
app.dependency_overrides[get_current_user_id] = admin_falso

# -- Testes automatizados específicos --

#teste para ver se eu coseguiria emprestar um livro que ja foi emprestado
def test_if_book_is_already_loaned():
    response = client.post("/loan/post",  json={"user_id": 1, "book_id": 1})
    print(response.json())
    assert response.status_code == 503




