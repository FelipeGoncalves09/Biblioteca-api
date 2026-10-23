# Biblioteca API

API REST para gerenciamento de uma biblioteca, com cadastro de usuários, autenticação, catálogo de livros integrado à API do Google Books e controle de empréstimos. Inclui um front-end simples (HTML, CSS e JavaScript) para uso e administração.

Fiz este projeto para praticar desenvolvimento back-end com Python, indo além do CRUD básico: autenticação com JWT, consumo de uma API externa e regras de negócio (empréstimos).

## Funcionalidades

- Cadastro e login de usuários com autenticação via token JWT
- Senhas armazenadas com hash (bcrypt)
- Perfil de administrador com permissões separadas das de usuário comum
- Busca de livros pela API do Google Books e cadastro no catálogo
- CRUD de livros
- Controle de empréstimos (emprestar, devolver e consultar "meus empréstimos")
- Validação de dados de entrada e saída com Pydantic
- Documentação interativa automática via Swagger UI
- Front-end com telas de login, listagem de livros, meus empréstimos e painel administrativo

## Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web para construção da API
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para modelagem e acesso ao banco de dados
- **[Pydantic](https://docs.pydantic.dev/)** — validação de dados de entrada e saída
- **[python-jose](https://github.com/mpdavis/python-jose)** e **[passlib](https://passlib.readthedocs.io/)** — JWT e hash de senhas
- **[HTTPX](https://www.python-httpx.org/)** — consumo da API do Google Books
- **[Uvicorn](https://www.uvicorn.org/)** — servidor ASGI
- **SQLite** — banco de dados local
- **HTML, CSS e JavaScript** — front-end

## Estrutura do projeto

```
biblioteca-api/
├── main.py              # ponto de entrada, registra as rotas
├── database.py          # configuração do banco, models e da sessão
├── schemas.py           # schemas Pydantic (validação de entrada/saída)
├── auth.py              # autenticação, JWT e hash de senhas
├── user_route.py        # rotas de usuários
├── books_route.py       # rotas de livros
├── loan_route.py        # rotas de empréstimos
├── google_book_api.py   # integração com a API do Google Books
├── login.html           # tela de login
├── livros.html          # listagem e busca de livros
├── meus.html            # empréstimos do usuário
├── admin.html           # painel administrativo
├── app.js               # lógica do front-end
├── style.css            # estilos
├── .env.example         # modelo das variáveis de ambiente
└── requirements.txt     # dependências do projeto
```

## Como rodar localmente

1. Clone o repositório:

```
git clone https://github.com/FelipeGoncalves09/biblioteca-api.git
cd biblioteca-api
```

2. Crie e ative um ambiente virtual:

```
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Crie o arquivo `.env` a partir do modelo e preencha com seus valores:

```
copy .env.example .env
```

5. Rode o servidor:

```
uvicorn main:app --reload
```

6. Acesse a documentação interativa em:

```
http://localhost:8000/docs
```

## Variáveis de ambiente

| Variável | Descrição |
| -------- | --------- |
| `GOOGLE_BOOKS_API_KEY` | Chave da API do Google Books |
| `SECRET_KEY` | Chave usada para assinar os tokens JWT |

## Endpoints principais

> A lista completa e atualizada está na documentação interativa em `/docs`.

### Usuários (`/users`)

| Método | Rota | Descrição |
| ------ | ---- | --------- |
| GET | `/users/` | Rota inicial de usuários |
| POST | `/users/post` | Cria um novo usuário |
| POST | `/users/login` | Faz login e retorna o token JWT |
| PUT | `/users/put/{id}` | Atualiza um usuário |
| DELETE | `/users/delete/{id}/` | Remove um usuário |

### Livros (`/books`)

| Método | Rota | Descrição |
| ------ | ---- | --------- |
| GET | `/books/` | Lista os livros do catálogo |
| POST | `/books/post` | Adiciona um livro |
| PUT | `/books/update/{id}` | Atualiza um livro |
| DELETE | `/books/delete/{id}` | Remove um livro |

### Empréstimos (`/loan`)

| Método | Rota | Descrição |
| ------ | ---- | --------- |
| GET | `/loan/homeLoan` | Rota inicial de empréstimos |
| GET | `/loan/me` | Lista os empréstimos do usuário autenticado |
| GET | `/loan/getloanlate` | Lista os empréstimos em atraso |
| POST | `/loan/post` | Realiza o empréstimo de um livro |
| PUT | `/loan/return/{id}` | Registra a devolução de um livro |

## Sobre o projeto

Construí esta API para praticar como as partes de um back-end real se conectam: autenticação, permissões, banco de dados relacional, consumo de API externa e regras de negócio. Evoluindo a partir da [Restaurante API](https://github.com/FelipeGoncalves09/Restaurante-api), meu foco foi entender cada camada da aplicação em vez de apenas seguir tutoriais.

## Roadmap

- [x] Autenticação de usuários (JWT)
- [x] Integração com a API do Google Books
- [x] Controle de empréstimos
- [ ] Testes automatizados (pytest)
- [ ] Separar o projeto em pastas (routers, models, schemas)
- [ ] Docker
- [ ] Migrations com Alembic
- [ ] Deploy em produção
