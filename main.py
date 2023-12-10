import string
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {"PokemonCardsAPI": "Welcome!"}

@app.get('/Decklist')
async def decklist():
    return {"Enter decklist as a query string"}

@app.get('/Decklist/{decklist_id}')
async def decklist(decklist_id: str):
    return {"decklist": decklist_id}
