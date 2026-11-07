import httpx
import asyncio



async def buscar_livro():
    termo = input("Digite o título: ")
    
    url = f"https://openlibrary.org/search.json?title={termo}"
    
    async with httpx.AsyncClient() as client:
        resposta = await client.get(url)
        dados = resposta.json()

        info = dados["docs"][0]
        autor = info.get("author_name")
        titulo = info["title"]
        sinopse = info.get("description")
        capa = info.get("imageLinks", {}).get("thumbnail")  

    return(autor, titulo, sinopse,capa)


        

