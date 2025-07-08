# Sudoku Solver

A full-featured Sudoku solver with both web interface and command-line interface. This application allows you to input Sudoku puzzles, solve them automatically, and interact with the board through an intuitive web UI or terminal interface.

## Features

- **Web Interface**: Modern, responsive web UI with interactive Sudoku board
- **Command-Line Interface**: Terminal-based interaction for puzzle solving
- **Multiple Input Methods**: 
  - Build entire boards from text input
  - Insert/delete individual digits
  - Click-to-select cells in web interface
- **Intelligent Solver**: 
  - Detects unique solutions
  - Identifies when no solution exists
  - Warns when multiple solutions are possible
- **Validation**: Real-time validation of Sudoku rules (row, column, and 3x3 block constraints)
- **Visual Feedback**: Clear distinction between pre-filled and user-entered cells

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Fonts**: Inter (Google Fonts)

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone or download the project files**
   ```bash
   # Ensure you have all these files in your project directory:
   # - main.py
   # - app.py
   # - index.html
   # - styles.css
   # - script.js
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the application**
   ```bash
   uvicorn app:app --reload
   ```

4. **Access the web interface**
   - Open your browser and navigate to `http://localhost:8000`
   - The web interface will load automatically

## Usage

### Web Interface

#### Starting a New Puzzle
1. Click **"New Puzzle"** to reset the board to empty state
2. Use the board building or manual input methods to create your puzzle

#### Building a Complete Board
1. In the **"Build Board"** section, enter 81 digits (9 rows × 9 columns)
2. Use `0` for empty cells, digits `1-9` for filled cells
3. Format: Space or newline-separated digits
4. Example input:
   ```
   5 3 0 0 7 0 0 0 0
   6 0 0 1 9 5 0 0 0
   0 9 8 0 0 0 0 6 0
   8 0 0 0 6 0 0 0 3
   4 0 0 8 0 3 0 0 1
   7 0 0 0 2 0 0 0 6
   0 6 0 0 0 0 2 8 0
   0 0 0 4 1 9 0 0 5
   0 0 0 0 8 0 0 7 9
   ```
5. Click **"Build Board"** to load the puzzle

#### Manual Cell Input
1. **Click any cell** on the board to select it (highlighted in blue)
2. The row and column inputs will auto-populate
3. Enter a digit (1-9) in the **"Value"** field
4. Click **"Insert Digit"** to place the number
5. Click **"Delete Digit"** to remove a number from the selected cell

#### Solving the Puzzle
1. Click **"Solve Puzzle"** to automatically solve the current board
2. The solver will:
   - Find the unique solution (if one exists)
   - Display "No solutions exist" if unsolvable
   - Show multiple solutions if the puzzle is ambiguous

### Command-Line Interface

Run the standalone version:
```bash
python main.py
```

#### Menu Options:
1. **Start a new puzzle** - Reset the board
2. **Build an entire board** - Input 9 rows of 9 digits
3. **Insert a digit** - Add a number to specific coordinates
4. **Delete a digit** - Remove a number from specific coordinates
5. **Solve the puzzle** - Run the automatic solver
6. **Quit** - Exit the program

## File Structure

```
sudoku-solver/
├── main.py          # Core game logic and CLI interface
├── app.py           # FastAPI web server and API endpoints
├── index.html       # Web interface structure
├── styles.css       # Custom styling and board layout
├── script.js        # Frontend JavaScript logic
└── README.md        # This file
```

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Serves the main web interface
- `GET /styles.css` - Serves the stylesheet
- `GET /script.js` - Serves the JavaScript file
- `POST /reset` - Resets the game board
- `POST /build` - Builds a board from 9×9 array
- `POST /insert` - Inserts a digit at specified position
- `POST /delete` - Deletes a digit at specified position
- `POST /solve` - Solves the current puzzle

## Game Rules

Standard Sudoku rules apply:

1. **Grid**: 9×9 grid divided into nine 3×3 sub-grids
2. **Numbers**: Use digits 1-9 only
3. **Row Rule**: Each row must contain each digit 1-9 exactly once
4. **Column Rule**: Each column must contain each digit 1-9 exactly once
5. **Box Rule**: Each 3×3 sub-grid must contain each digit 1-9 exactly once

## Algorithm

The solver uses a **backtracking algorithm**:

1. Find the first empty cell
2. Try digits 1-9 in that cell
3. Check if the digit violates Sudoku rules
4. If valid, recursively solve the rest of the puzzle
5. If no digit works, backtrack and try the next possibility
6. Continue until solution is found or all possibilities are exhausted

## Troubleshooting

### Common Issues

**"No solutions exist"**
- Check that your input follows Sudoku rules
- Ensure no duplicate numbers in rows, columns, or 3×3 boxes

**"Multiple solutions exist"**
- The puzzle is under-constrained
- Add more clues to create a unique solution

**Board won't build**
- Verify you have exactly 81 digits
- Check that all digits are between 0-9
- Ensure no conflicts in the initial setup

**Server won't start**
- Verify FastAPI and uvicorn are installed
- Check that port 8000 is not in use
- Ensure all required files are in the same directory

### Development

To modify or extend the application:

1. **Backend changes**: Edit `main.py` for game logic, `app.py` for API endpoints
2. **Frontend changes**: Modify `index.html` for structure, `styles.css` for appearance, `script.js` for behavior
3. **Testing**: Use the command-line interface for debugging game logic
4. **Restart**: Use `uvicorn app:app --reload` for auto-reloading during development

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the [MIT License](LICENSE).
