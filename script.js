document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('sudoku-board');
    const messageBox = document.getElementById('message-box');
    const newPuzzleBtn = document.getElementById('new-puzzle-btn');
    const solvePuzzleBtn = document.getElementById('solve-puzzle-btn');
    const buildBoardInput = document.getElementById('build-board-input');
    const buildBoardBtn = document.getElementById('build-board-btn');
    const rowInput = document.getElementById('row-input');
    const colInput = document.getElementById('col-input');
    const valueInput = document.getElementById('value-input');
    const insertDigitBtn = document.getElementById('insert-digit-btn');
    const deleteDigitBtn = document.getElementById('delete-digit-btn');
    const quitBtn = document.getElementById('quit-btn');

    let currentBoard = Array(9).fill(0).map(() => Array(9).fill(0));
    let prefilledCells = new Set(); // Stores "row-col" strings for pre-filled cells

    // Function to display messages to the user
    function displayMessage(message, isError = false) {
        messageBox.textContent = message;
        messageBox.className = `mt-4 text-lg font-semibold text-center min-h-[2rem] ${isError ? 'text-red-600' : 'text-gray-700'}`;
    }

    // Function to render the Sudoku board in the UI
    function renderBoard(board) {
        boardElement.innerHTML = ''; // Clear existing board
        prefilledCells.clear(); // Clear pre-filled cells on new render

        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const cell = document.createElement('div');
                cell.classList.add('sudoku-cell', 'flex', 'items-center', 'justify-center', 'text-2xl', 'font-semibold', 'border', 'border-gray-300');
                cell.dataset.row = r;
                cell.dataset.col = c;
                cell.textContent = board[r][c] !== 0 ? board[r][c] : '';

                // Add classes for thicker borders to create 3x3 blocks
                if (r % 3 === 2 && r !== 8) cell.classList.add('border-b-2', 'border-gray-500');
                if (c % 3 === 2 && c !== 8) cell.classList.add('border-r-2', 'border-gray-500');

                // Mark pre-filled cells (those not 0 after initial load/build)
                if (board[r][c] !== 0) {
                    cell.classList.add('prefilled');
                    prefilledCells.add(`${r}-${c}`);
                }

                // Add click listener to select cells for insert/delete
                cell.addEventListener('click', () => {
                    // Remove 'selected' from previously selected cell
                    const currentlySelected = document.querySelector('.sudoku-cell.selected');
                    if (currentlySelected) {
                        currentlySelected.classList.remove('selected');
                    }
                    // Add 'selected' to the clicked cell
                    cell.classList.add('selected');
                    // Populate input fields
                    rowInput.value = r;
                    colInput.value = c;
                    displayMessage(''); // Clear any previous messages
                });

                boardElement.appendChild(cell);
            }
        }
    }

    // Function to fetch the current board state from the backend
    async function fetchBoard() {
        // This function is currently a placeholder.
        // A dedicated /get_board endpoint in app.py would be ideal here.
        // For now, we rely on other operations returning the board or implicit updates.
    }

    // Function to update a single cell in the UI
    function updateCellUI(row, col, value) {
        const cell = boardElement.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        if (cell) {
            cell.textContent = value !== 0 ? value : '';
            // If a cell is inserted/deleted by user, it's not prefilled
            if (value === 0) {
                cell.classList.remove('prefilled');
                prefilledCells.delete(`${row}-${col}`);
            } else {
                // If it's a user-inserted value, it's not prefilled, but editable
                cell.classList.remove('prefilled');
                prefilledCells.delete(`${row}-${col}`);
            }
        }
    }

    // API Call Helper
    async function callApi(endpoint, method = 'POST', body = null) {
        try {
            const options = { method };
            if (body !== null) { // Check for null explicitly, as body can be [] or other falsy but valid values
                options.headers = { 'Content-Type': 'application/json' };
                options.body = JSON.stringify(body);
            }
            const response = await fetch(endpoint, options);

            if (!response.ok) {
                const errorData = await response.json();
                // Check if errorData has 'detail' (FastAPI validation errors)
                if (errorData && errorData.detail) {
                    // If it's a validation error, detail is an array of errors
                    if (Array.isArray(errorData.detail)) {
                        const messages = errorData.detail.map(err => {
                            // Path indicates which field caused the error
                            const field = err.loc && err.loc.length > 1 ? err.loc[1] : 'unknown field';
                            return `${field}: ${err.msg}`;
                        }).join('; ');
                        throw new Error(`Validation Error: ${messages}`);
                    } else if (typeof errorData.detail === 'string') {
                        // For general HTTP errors where detail is a string
                        throw new Error(errorData.detail);
                    }
                }
                // Fallback for other non-OK responses
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error calling ${endpoint}:`, error);
            displayMessage(`Operation failed: ${error.message}`, true);
            return null;
        }
    }

    // Event Listeners

    // 1. Start a new puzzle
    newPuzzleBtn.addEventListener('click', async () => {
        const result = await callApi('/reset', 'POST');
        if (result !== null) {
            currentBoard = Array(9).fill(0).map(() => Array(9).fill(0)); // Reset local board
            renderBoard(currentBoard);
            displayMessage('New puzzle started. Board reset.');
        }
    });

    // 2. Build an entire board
    buildBoardBtn.addEventListener('click', async () => {
        const inputText = buildBoardInput.value.trim();
        if (!inputText) {
            displayMessage('Please enter board data to build.', true);
            return;
        }

        // Split by any whitespace (including newlines and spaces)
        const allDigits = inputText.split(/\s+/).filter(s => s !== '').map(Number);

        // Ensure we have exactly 81 digits
        if (allDigits.length !== 81) {
            displayMessage('Invalid board format. Please enter exactly 81 digits (9 rows of 9).', true);
            return;
        }

        // Reconstruct into a 9x9 array
        const rows = [];
        for (let i = 0; i < 9; i++) {
            const row = allDigits.slice(i * 9, (i + 1) * 9);
            // Validate that all numbers are between 0 and 9
            if (!row.every(num => !isNaN(num) && num >= 0 && num <= 9)) {
                displayMessage('Invalid input. Digits must be between 0 and 9.', true);
                return;
            }
            rows.push(row);
        }

        // --- IMPORTANT CHANGE HERE ---
        // Send the 'rows' array directly as the request body, not wrapped in an object.
        const result = await callApi('/build', 'POST', rows); // Changed from { arr: rows } to rows
        if (result !== null) {
            if (result === true) { // Assuming `build` returns true on success
                currentBoard = rows; // Update local board with the built board
                renderBoard(currentBoard);
                displayMessage('Board successfully built.');
            } else {
                // This case handles a false return from backend's build method
                // which means main.py's build method returned False due to conflicts.
                displayMessage('Board build failed due to invalid input or conflicts detected by the solver.', true);
            }
        }
    });

    // 3. Insert a digit
    insertDigitBtn.addEventListener('click', async () => {
        const row = parseInt(rowInput.value);
        const col = parseInt(colInput.value);
        const value = parseInt(valueInput.value);

        if (isNaN(row) || isNaN(col) || isNaN(value) || row < 0 || row > 8 || col < 0 || col > 8 || value < 1 || value > 9) {
            displayMessage('Please enter valid row (0-8), column (0-8), and digit (1-9).', true);
            return;
        }

        if (prefilledCells.has(`${row}-${col}`)) {
            displayMessage('Cannot insert into a pre-filled cell. These are part of the original puzzle.', true);
            return;
        }

        const result = await callApi('/insert', 'POST', { row, col, value });
        if (result !== null) {
            if (result === true) { // Assuming `insert` returns true on success
                updateCellUI(row, col, value);
                currentBoard[row][col] = value; // Update local board
                displayMessage(`Digit ${value} inserted at (${row}, ${col}).`);
            } else {
                displayMessage('Insertion failed. Check Sudoku rules (row, column, or block conflict).', true);
            }
        }
    });

    // 4. Delete a digit
    deleteDigitBtn.addEventListener('click', async () => {
        const row = parseInt(rowInput.value);
        const col = parseInt(colInput.value);

        if (isNaN(row) || isNaN(col) || row < 0 || row > 8 || col < 0 || col > 8) {
            displayMessage('Please enter valid row (0-8) and column (0-8) to delete.', true);
            return;
        }

        if (prefilledCells.has(`${row}-${col}`)) {
            displayMessage('Cannot delete a pre-filled cell. These are part of the original puzzle.', true);
            return;
        }

        const result = await callApi('/delete', 'POST', { row, col });
        if (result !== null) {
            if (result === true) { // Assuming `delete` returns true on success
                updateCellUI(row, col, 0);
                currentBoard[row][col] = 0; // Update local board
                displayMessage(`Digit at (${row}, ${col}) deleted.`);
            } else {
                displayMessage('Deletion failed.', true);
            }
        }
    });

    // 5. Solve the puzzle
    solvePuzzleBtn.addEventListener('click', async () => {
        displayMessage('Solving puzzle...', false);
        const result = await callApi('/solve', 'POST');
        if (result !== null) {
            if (Array.isArray(result) && result.length === 9 && Array.isArray(result[0])) {
                // If a unique solution (board array) is returned
                currentBoard = result; // Update local board with solved board
                renderBoard(currentBoard); // Re-render with the solved board
                displayMessage('Puzzle solved!');
            } else if (typeof result === 'string') {
                // If a string message (no solution) is returned
                displayMessage(result, true);
            } else if (typeof result === 'object' && result.message && result.solution1 && result.solution2) {
                // If multiple solutions object is returned
                displayMessage(result.message, true);
                // Optionally, display the first solution on the board
                // For showing two solutions, you might need a modal or separate display area.
                // For simplicity, we'll just show the first solution on the board.
                currentBoard = result.solution1;
                renderBoard(currentBoard);
                // You could add logic here to show the second solution in a different way
                // or prompt the user to switch between them.
            } else {
                displayMessage('Solver response unexpected. Check server logs.', true);
            }
        }
    });

    // 6. Quit (client-side only, as the backend is persistent)
    quitBtn.addEventListener('click', () => {
        displayMessage('Exiting Sudoku Solver. Goodbye!', false);
        // In a web environment, "quit" typically means closing the tab or navigating away.
        // We can disable buttons or show a final message.
        newPuzzleBtn.disabled = true;
        solvePuzzleBtn.disabled = true;
        buildBoardBtn.disabled = true;
        insertDigitBtn.disabled = true;
        deleteDigitBtn.disabled = true;
        quitBtn.disabled = true;
        // Optionally, clear the board
        renderBoard(Array(9).fill(0).map(() => Array(9).fill(0)));
    });

    // Initial board render
    renderBoard(currentBoard); // Render an empty board initially
});
