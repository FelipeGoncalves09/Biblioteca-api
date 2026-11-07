from main import app
from fastapi.testclient import TestClient
import random
client = TestClient(app)

# -- Testes automatizados específicos --

#-- teste de criaçao do usuario
def test_create_user():
    response = client.post("/users/post", json={"name": f"felipe {random.randint(1, 10000)}", "password": "testt"})
    print(response.json())
    assert response.status_code == 200
    