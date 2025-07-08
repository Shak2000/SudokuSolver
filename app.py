from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from typing import List  # Import List for type hinting
from pydantic import BaseModel  # Import BaseModel for defining request body structure

from main import Game

game = Game()
app = FastAPI()


# Define Pydantic models for request bodies
class InsertRequest(BaseModel):
    row: int
    col: int
    value: int


class DeleteRequest(BaseModel):
    row: int
    col: int


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
    return True  # Return a simple success indicator


@app.post("/insert")
async def insert(request: InsertRequest):  # Use Pydantic model for request body
    return game.insert(request.row, request.col, request.value)


@app.post("/delete")
async def delete(request: DeleteRequest):  # Use Pydantic model for request body
    return game.delete(request.row, request.col)


@app.post("/build")
async def build(arr: List[List[int]] = Body(...)):  # Explicitly type as nested List of ints
    # The build method in main.py already returns True/False
    return game.build(arr)


@app.post("/solve")
async def solve():
    game.solve()  # This will update game.board if unique solution, or populate game.solutions

    if len(game.solutions) == 1:
        # If a unique solution is found, return the solved board
        return game.solutions[0]
    elif len(game.solutions) == 0:
        return "No solutions exist for this Sudoku puzzle."
    else:
        # If multiple solutions, return a message and the first two solutions
        return {
            "message": "Multiple solutions exist for this Sudoku puzzle.",
            "solution1": game.solutions[0],
            "solution2": game.solutions[1]
        }
