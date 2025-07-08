from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from typing import List  # Import List for type hinting

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
    return True  # Return a simple success indicator


@app.post("/insert")
async def insert(row: int, col: int, value: int):
    # The insert method in main.py already returns True/False
    return game.insert(row, col, value)


@app.post("/delete")
async def delete(row: int, col: int):
    # The delete method in main.py already returns True/False
    return game.delete(row, col)


@app.post("/build")
async def build(arr: List[List[int]] = Body(...)):  # Explicitly type as List of List of ints
    # The build method in main.py already returns True/False
    return game.build(arr)


@app.post("/solve")
async def solve():
    # When solving, the main.py's solve method prints to console and modifies
    # the internal board. To send the result back to the UI, we need to
    # capture the solved board or a message.
    # If no solution or multiple solutions, main.py prints messages.
    # We need to adapt this to return a structured response.

    # Create a temporary Game instance or pass the current board to a solver function
    # to avoid modifying the main game.board prematurely for solution display logic.
    # However, based on the current main.py, game.solve() already handles
    # restoring the original board after finding solutions.

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
