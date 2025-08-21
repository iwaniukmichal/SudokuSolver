import argparse
from itertools import combinations
import numpy as np
import copy


ROW_IDX = {1: [0, 1, 2, 3, 4, 5, 6, 7, 8],
           2: [9, 10, 11, 12, 13, 14, 15, 16, 17],
           3: [18, 19, 20, 21, 22, 23, 24, 25, 26],
           4: [27, 28, 29, 30, 31, 32, 33, 34, 35],
           5: [36, 37, 38, 39, 40, 41, 42, 43, 44],
           6: [45, 46, 47, 48, 49, 50, 51, 52, 53],
           7: [54, 55, 56, 57, 58, 59, 60, 61, 62],
           8: [63, 64, 65, 66, 67, 68, 69, 70, 71],
           9: [72, 73, 74, 75, 76, 77, 78, 79, 80],
           }


COL_IDX = {1: [0, 9, 18, 27, 36, 45, 54, 63, 72],
           2: [1, 10, 19, 28, 37, 46, 55, 64, 73],
           3: [2, 11, 20, 29, 38, 47, 56, 65, 74],
           4: [3, 12, 21, 30, 39, 48, 57, 66, 75],
           5: [4, 13, 22, 31, 40, 49, 58, 67, 76],
           6: [5, 14, 23, 32, 41, 50, 59, 68, 77],
           7: [6, 15, 24, 33, 42, 51, 60, 69, 78],
           8: [7, 16, 25, 34, 43, 52, 61, 70, 79],
           9: [8, 17, 26, 35, 44, 53, 62, 71, 80]
           }


BOX_IDX = {1: [0, 1, 2, 9, 10, 11, 18, 19, 20],
           2: [3, 4, 5, 12, 13, 14, 21, 22, 23],
           3: [6, 7, 8, 15, 16, 17, 24, 25, 26],
           4: [27, 28, 29, 36, 37, 38, 45, 46, 47],
           5: [30, 31, 32, 39, 40, 41, 48, 49, 50],
           6: [33, 34, 35, 42, 43, 44, 51, 52, 53],
           7: [54, 55, 56, 63, 64, 65, 72, 73, 74],
           8: [57, 58, 59, 66, 67, 68, 75, 76, 77],
           9: [60, 61, 62, 69, 70, 71, 78, 79, 80]
           }


class Cell:
    def __init__(self, value, row, column, box, idx):
        self.value = value
        self.notes = []
        self.row = row
        self.column = column
        self.box = box
        self.idx = idx


class Sudoku:

    def __init__(self, file):
        self.fields = [None] * 81
        self.val_to_cells = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
        }

        with open(file, 'r') as file:
            number_string = file.read().strip()
        number_list = [int(digit) for digit in number_string]
        assert len(number_list) == 81

        for i in range(81):

            row = i // 9 + 1
            column = i % 9 + 1
            box = 3 * ((row - 1) // 3) + ((column - 1) // 3) + 1

            value = number_list[i]
            cell = Cell(value, row, column, box, i)

            self.fields[i] = cell
            self.val_to_cells[value].append(cell)

        self.make_notes()

    def solve(self):

        while self.val_to_cells[0]:
            prev = len(self.val_to_cells[0])

            self.replace_single_notes()
            self.replace_single_note_in_block()

            curr = len(self.val_to_cells[0])
            if prev == curr:
                number_of_notes0 = sum(len(cell.notes)
                                       for cell in self.val_to_cells[0])
                self.replace_line()
                self.replace_n_notes(n=2)
                self.replace_n_notes(n=3)
                self.replace_n_notes(n=4)
                number_of_notes1 = sum(len(cell.notes)
                                       for cell in self.val_to_cells[0])

                if number_of_notes1 == 0:
                    is_empty_cells = self.val_to_cells[0]
                    return not is_empty_cells, self  # If no empty cells, Sudoku is solved

                if number_of_notes0 == number_of_notes1:
                    print("No progress made, trying to put a value from notes")
                    empty_cell = self.val_to_cells[0][0]

                    sudoku_alt = copy.deepcopy(self)

                    if not empty_cell.notes:
                        return False, self

                    val = empty_cell.notes[0]

                    sudoku_alt.put_value_and_remove_notes(
                        sudoku_alt.val_to_cells[0][0], val)

                    is_alt_solved, _ = sudoku_alt.solve()

                    if is_alt_solved:
                        self = sudoku_alt
                        return True, self
                    else:
                        self.val_to_cells[0][0].notes.remove(val)
                else:
                    print(
                        f"Progress made: {prev} -> {curr}, notes: {number_of_notes0} -> {number_of_notes1}")
        return True, self

    def __str__(self):
        value_width = 3
        notes_width = 6
        s1 = '|         |' * 9 + "\n"
        s2 = '|---------|' * 9 + "\n"

        lines = []
        lines.append(s2)

        for i in range(9):
            row_parts = []
            for j in range(9):
                cell = self.fields[i * 9 + j]
                value_str = cell.value
                notes_str = "".join(map(str, cell.notes)) if cell.notes else ""
                row_parts.append(
                    f"|{value_str:<{value_width}}{notes_str:<{notes_width}}|")
            lines.append("".join(row_parts) + "\n")
            lines.append(s1)
            lines.append(s2)

        return "".join(lines)

    def make_notes(self):
        forbidden_dict = {
            1: {"rows": [], "cols": [], "box": []},
            2: {"rows": [], "cols": [], "box": []},
            3: {"rows": [], "cols": [], "box": []},
            4: {"rows": [], "cols": [], "box": []},
            5: {"rows": [], "cols": [], "box": []},
            6: {"rows": [], "cols": [], "box": []},
            7: {"rows": [], "cols": [], "box": []},
            8: {"rows": [], "cols": [], "box": []},
            9: {"rows": [], "cols": [], "box": []},
        }

        for value in range(1, 10, 1):
            cells_value = self.val_to_cells[value]
            for cell in cells_value:
                forbidden_dict[value]['rows'].append(cell.row)
                forbidden_dict[value]['cols'].append(cell.column)
                forbidden_dict[value]['box'].append(cell.box)

        for value in range(1, 10, 1):

            empty_cells = self.val_to_cells[0]
            forbiden_dict_value = forbidden_dict[value]

            for cell in empty_cells:
                if cell.row in forbiden_dict_value["rows"] or cell.column in forbiden_dict_value['cols'] or cell.box in forbiden_dict_value['box']:
                    continue
                else:
                    cell.notes.append(value)

    def replace_single_notes(self):
        empty_cells = self.val_to_cells[0]
        for cell in empty_cells:
            if len(cell.notes) == 1:
                value = cell.notes[0]
                self.put_value_and_remove_notes(cell, value)

    def replace_single_note_in_block(self):

        for k in range(1, 10, 1):
            self.replace_single_note_in_block_from_index_list(BOX_IDX[k])
            self.replace_single_note_in_block_from_index_list(COL_IDX[k])
            self.replace_single_note_in_block_from_index_list(ROW_IDX[k])

    def replace_line(self):
        for k in range(1, 10, 1):
            box_indexes = BOX_IDX[k]
            self.remove_notes_from_line(box_indexes)

    def remove_notes_from_line(self, box_indexes):
        notes_value_to_idx = self.get_notes_value_to_idx(box_indexes)

        for val, idx_list in notes_value_to_idx.items():
            if len(idx_list) > 3 or len(idx_list) == 0:
                continue
            r = np.array(idx_list) // 9 + 1
            is_same_row = r.min() == r.max()
            c = np.array(idx_list) % 9 + 1
            is_same_column = c.min() == c.max()

            if is_same_row:
                row = r[0]
                row_indexes = ROW_IDX[row]

                remove_indexes = set(row_indexes) - set(box_indexes)
                self.remove_value_from_notes(remove_indexes, val)

            if is_same_column:
                column = c[0]
                col_indexes = COL_IDX[column]

                remove_indexes = set(col_indexes) - set(box_indexes)
                self.remove_value_from_notes(remove_indexes, val)

    def replace_single_note_in_block_from_index_list(self, indexes):
        fields = self.fields

        notes_value_to_idx = self.get_notes_value_to_idx(indexes)

        for val in notes_value_to_idx.keys():
            idx_list = notes_value_to_idx[val]
            if len(idx_list) == 1:
                idx = idx_list[0]
                value = val
                cell = fields[idx]
                self.put_value_and_remove_notes(cell, value)

    def get_notes_value_to_idx(self, indexes):
        fields = self.fields
        notes_value_to_idx = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
        }

        for index in indexes:
            notes = fields[index].notes
            for val in notes:
                notes_value_to_idx[val].append(index)

        return notes_value_to_idx

    def put_value_and_remove_notes(self, cell, value):
        # powinno zawsze byc przy normalnym rozwiazywaniu
        if cell in self.val_to_cells[0]:
            self.val_to_cells[0].remove(cell)

        cell.value = value
        cell.notes = []

        row_indexes = ROW_IDX[cell.row]
        col_indexes = COL_IDX[cell.column]
        box_indexes = BOX_IDX[cell.box]

        self.remove_value_from_notes(row_indexes, value)
        self.remove_value_from_notes(col_indexes, value)
        self.remove_value_from_notes(box_indexes, value)

    def remove_value_from_notes(self, indexes, value):
        fields = self.fields
        for index in indexes:
            if value in fields[index].notes:
                fields[index].notes.remove(value)

    def replace_n_notes(self, n):
        for k in range(1, 10, 1):
            self.set_n_notes(BOX_IDX[k], n)
            self.set_n_notes(ROW_IDX[k], n)
            self.set_n_notes(COL_IDX[k], n)

    def set_n_notes(self, box_indexes, n):
        fields = self.fields
        notes_value_to_idx = self.get_notes_value_to_idx(box_indexes)

        n_notes = {}
        for val in range(1, 10, 1):
            idx_list = notes_value_to_idx[val]
            if len(idx_list) == n:
                n_notes[val] = idx_list

        n_notes_comparations = list(combinations(n_notes, n))
        for vals in n_notes_comparations:
            ncomp = {val: n_notes[val] for val in vals}

            idxs = list(ncomp.values())
            ref = set(idxs[0])

            if all(set(i) == ref for i in idxs):
                for idx in ref:
                    fields[idx].notes = list(vals)


def main():
    parser = argparse.ArgumentParser(
        description="Solve a Sudoku puzzle from a file.")
    parser.add_argument(
        "task", help="Path to the Sudoku task file (e.g., task.txt)")
    parser.add_argument(
        "solution", help="Path where the solved Sudoku will be saved (e.g., solution.txt)")
    args = parser.parse_args()

    sudoku = Sudoku(args.task_file)
    is_solved, sudoku = sudoku.solve()

    solution = [cell.value for cell in sudoku.fields]
    with open(args.solution_file, 'w') as file:
        for number in solution:
            file.write(f"{number}")


if __name__ == "__main__":
    main()

