from fastapi import FastAPI
from fastapi.responses import FileResponse
from main import Game

game = Game()
app = FastAPI()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/reset")
async def reset():
    game.reset()


@app.post("/insert")
async def insert(row, col, value):
    return game.insert(row, col, value)


@app.post("/delete")
async def delete(row, col):
    return game.delete(row, col)


@app.post("/build")
async def build(arr):
    return game.build(arr)


@app.post("/solve")
async def solve():
    return game.solve()
