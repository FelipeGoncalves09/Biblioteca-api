import httpx
import asyncio

async def buscar_livro(title: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key=AIzaSyAzS4eqqU97v02rBPqNmLAYJe2FTNvDxNQ"
    
    async with httpx.AsyncClient() as client:
        resposta = await client.get(url)
        dados = resposta.json()

    if dados.get("totalItems", 0) == 0:
        print("Nenhum livro encontrado.")
        return None, None

    titulo = dados["items"][0]["volumeInfo"]["title"]
    autor = dados["items"][0]["volumeInfo"]["authors"][0]
    return titulo, autor
    


'''titulo, autor = asyncio.run(buscar_livro(titulo_livro))
print(titulo)
print(autor)'''