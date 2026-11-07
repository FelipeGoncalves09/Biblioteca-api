import os
import httpx
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")

# --- Busca o livro na api do google books pelo titulo ---
async def buscar_livro(title: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={API_KEY}"

    async with httpx.AsyncClient() as client:
        resposta = await client.get(url)
        # --- transforma a resposta em json pra eu conseguir percorrer ---
        dados = resposta.json()
        # --- print so pra ver oq a api ta devolvendo quando der erro ---
        print(dados)

    # --- se nao achou nada, vai devolver None ---
    if dados.get("totalItems", 0) == 0:
        print("Nenhum livro encontrado.")
        
        return None, None, None, None

    # --- pega so o primeiro resultado e separa os dados necessários ---
    info = dados["items"][0]["volumeInfo"]
    titulo = info["title"]
    autor = info["authors"][0]
    # --- esses dois nem sempre vem, por isso o .get() ---
    sinopse = info.get("description")
    capa = info.get("imageLinks", {}).get("thumbnail")

    return titulo, autor, sinopse, capa