# Sudoku Solver — Human Like

A compact, human-style Sudoku solver that works by keeping **notes (candidates)** in each empty cell and repeatedly applying classic logic techniques. If pure logic stalls, it tries a tentative value (with backtracking) to finish.

---

## How to run

1. Put your puzzle in `task.txt` as **81 digits in a single line** (row-major order).

   * Use digits `1–9` for given numbers and `0` for empty cells.
   * Example

     ```
     000109083000302900930008400060810000028095074400000008200480500504000816800006000
     ```

2. Run:

   ```bash
   python sudoku.py --task path/to/task.txt --solution path/to/solution.txt
   ```

3. The program will write the final solution to `solution.txt` as **81 digits**.

---

## What the solver does (step by step)

### 1) Parse & model the grid

* The file is read into 81 `Cell` objects stored in a flat list `fields[0..80]`.
* Each `Cell` knows its `row` (1–9), `column` (1–9), `box` (1–9), `value` (0 if empty) and `notes` (candidate values for cell; empty list if cell is not empty).
* Three index maps define the peer groups:

  * `ROW_IDX[r]` → indices of row *r*
  * `COL_IDX[c]` → indices of column *c*
  * `BOX_IDX[b]` → indices of 3×3 box *b*
* A dictionary `val_to_cells` groups cells by value:
  `val_to_cells[1]...val_to_cells[9]` are lists of placed digits; `val_to_cells[0]` is the list of **empty** cells.

### 2) Make initial notes (candidates)

* For every empty cell, the solver writes `notes = [d]` for each digit `d` not already present in its **row, column, or box**.

### 3) Iterate logical techniques until no empties remain

Inside a loop, these techniques run in order; whenever a value is placed, the solver updates peer notes immediately.

1. **Naked Singles** – if a cell has exactly **one** note, place that value.
2. **Hidden Singles (in any unit)** – for each **row, column, and box**, if some digit can go in **exactly one** position within that unit, place it there.
3. **Pointing Pairs/Triples (Box–Line reduction)** – for each **box**, if all candidates of a digit lie on a **single row** inside that box, remove that digit from other cells of that row **outside** the box (similarly for a single column).
4. **Naked Sets in a box (pairs/triples/quads)** – inside each **unit (row/column/box)**, if **n** digits each appear in exactly **n** common cells (for n = 2, 3, 4), lock those cells to exactly that set and remove all other notes from them.

The loop measures progress by:

* how many empty cells remain, and
* the total count of notes across empty cells.

If any technique reduced empties or notes, the loop restarts from step (**1**).

### 4) Last resort: guess with backtracking

If **no technique makes progress**:

* Pick the first empty cell and take its first candidate.
* **Clone** the whole Sudoku, place that tentative value, and try to solve the clone recursively.

  * If the clone solves, accept its state as the solution.
  * If it fails, remove that candidate from the original cell and continue (loop starts again).

### 5) Finish

When there are **no empty cells**, the puzzle is solved and written to `solution.txt`.

---

## I/O details

* **Input**: `.txt file` with exactly **81 characters**, each `0–9`.
  `0` means empty. Any other length or invalid chars will raise an error.
* **Output (file)**: `solution.txt` with 81 digits of the solved grid.

---

## Notes & Tips

* Puzzles should be valid and solvable.
* Backtracking is only used in extreme cases – for example, when there is more than one possible solution. Typical puzzles (even those at the "Extreme" level from [sudoku.com](https://sudoku.com/extreme/)) can be solved without backtracking.
* If a Sudoku puzzle has more than one solution, only the first one found will be saved in `solution.txt`.

---


Happy solving! 🧩
