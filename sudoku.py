import sys

class Cell:

    def __init__(self, value, row, column, box):
        self.value = value
        self.notes = []
        self.row = row
        self.column = column
        self.box = box


class Sudoku:

    def __init__(self, file):
        self.fields = [None] * 81

        with open(file, 'r') as file:
            number_string = file.read().strip()
        number_list = [int(digit) for digit in number_string]
        for i in range(len(number_list)):
            row = i // 9 + 1
            column = i % 9 + 1
            box = 3 * ((row - 1) // 3) + ((column - 1) // 3) + 1
            self.fields[i] = Cell(number_list[i], row, column, box)

    def solve(self):
        self.make_notes()

        is_notes = True
        is_box = True
        is_row = True
        is_col = True

        while is_col or is_row or is_box or is_notes:
            is_notes = self.is_there_single_note()
            if is_notes:
                self.replace_single_notes()

            is_row = self.is_there_single_row()
            if is_row:
                self.replace_single_rows()

            is_col = self.is_there_single_col()
            if is_col:
                self.replace_single_cols()

            is_box = self.is_there_single_box()
            if is_box:
                self.replace_single_box()

    def make_notes(self):
        fields = self.fields
        for value in range(1, 10, 1):
            value_rows = []
            value_cols = []
            value_box = []
            for i in range(len(fields)):
                if fields[i].value == value:
                    value_rows.append(fields[i].row)
                    value_cols.append(fields[i].column)
                    value_box.append(fields[i].box)
            for i in range(len(fields)):
                if fields[i].value == 0:
                    if fields[i].row not in value_rows and fields[i].column not in value_cols and fields[i].box not in value_box:
                        fields[i].notes.append(value)

    def replace_single_notes(self):
        fields = self.fields
        for i in range(len(fields)):
            if len(fields[i].notes) == 1:
                value = fields[i].notes[0]
                row = fields[i].row
                column = fields[i].column
                box = fields[i].box
                self.put_value_and_remove_notes(value, row, column, box, i)

    def replace_single_rows(self):
        fields = self.fields
        for r in range(1, 10, 1):
            all_notes = []
            for col in range(1, 10, 1):
                index = (r - 1) * 9 + col - 1
                all_notes = all_notes + fields[index].notes
            counts = [0] * 9
            for i in range(len(all_notes)):
                counts[all_notes[i] - 1] += 1

            for j in range(len(counts)):
                if counts[j] == 1:
                    value = j + 1
                    for col in range(1, 10, 1):
                        index = (r - 1) * 9 + col - 1
                        if value in fields[index].notes:
                            column = col
                            row = r
                            box = fields[index].box
                            self.put_value_and_remove_notes(value, row, column, box, index)
                            break

    def replace_single_cols(self):
        fields = self.fields
        for col in range(1, 10, 1):
            all_notes = []
            for r in range(1, 10, 1):
                index = (r - 1) * 9 + col - 1
                all_notes = all_notes + fields[index].notes
            counts = [0] * 9
            for i in range(len(all_notes)):
                counts[all_notes[i] - 1] += 1

            for j in range(len(counts)):
                if counts[j] == 1:
                    value = j + 1
                    for r in range(1, 10, 1):
                        index = (r - 1) * 9 + col - 1
                        if value in fields[index].notes:
                            column = col
                            row = r
                            box = fields[index].box
                            self.put_value_and_remove_notes(value, row, column, box, index)
                            break

    def replace_single_box(self):
        fields = self.fields
        for box in range(1, 10, 1):
            all_notes = []
            for r in range(1, 10, 1):
                for col in range(1, 10, 1):
                    if 3 * ((r - 1) // 3) + ((col - 1) // 3) + 1 == box:
                        index = (r - 1) * 9 + col - 1
                        all_notes = all_notes + fields[index].notes
            counts = [0] * 9
            for i in range(len(all_notes)):
                counts[all_notes[i] - 1] += 1

            for j in range(len(counts)):
                if counts[j] == 1:
                    value = j + 1
                    found = False
                    for r in range(1, 10, 1):
                        for col in range(1, 10, 1):
                            if 3 * ((r - 1) // 3) + ((col - 1) // 3) + 1 == box:
                                index = (r - 1) * 9 + col - 1
                                if value in fields[index].notes:
                                    column = col
                                    row = r
                                    self.put_value_and_remove_notes(value, row, column, box, index)
                                    found = True
                                    break
                        if found:
                            break

    def is_there_single_note(self):
        fields = self.fields
        for i in range(len(fields)):
            if len(fields[i].notes) == 1:
                return True
        return False

    def is_there_single_row(self):
        fields = self.fields
        for r in range(1, 10, 1):
            all_notes = []
            for col in range(1, 10, 1):
                index = (r - 1) * 9 + col - 1
                all_notes = all_notes + fields[index].notes
            counts = [0] * 9
            for i in range(len(all_notes)):
                counts[all_notes[i] - 1] += 1
            if 1 in counts:
                return True
        return False

    def is_there_single_col(self):
        fields = self.fields
        for col in range(1, 10, 1):
            all_notes = []
            for r in range(1, 10, 1):
                index = (r - 1) * 9 + col - 1
                all_notes = all_notes + fields[index].notes
            counts = [0] * 9
            for i in range(len(all_notes)):
                counts[all_notes[i] - 1] += 1
            if 1 in counts:
                return True
        return False

    def is_there_single_box(self):
        fields = self.fields
        for box in range(1, 10, 1):
            all_notes = []
            for r in range(1, 10, 1):
                for col in range(1, 10, 1):
                    if 3 * ((r - 1) // 3) + ((col - 1) // 3) + 1 == box:
                        index = (r - 1) * 9 + col - 1
                        all_notes = all_notes + fields[index].notes
            counts = [0] * 9
            for i in range(len(all_notes)):
                counts[all_notes[i] - 1] += 1
            if 1 in counts:
                return True
        return False

    def put_value_and_remove_notes(self, value, row, column, box, i):
        fields = self.fields
        fields[i] = Cell(value, row, column, box)

        for col in range(1, 10, 1):
            if col != column:
                index = (row - 1) * 9 + col - 1
                if value in fields[index].notes:
                    fields[index].notes.remove(value)

        for r in range(1, 10, 1):
            if r != row:
                index = (r - 1) * 9 + column - 1
                if value in fields[index].notes:
                    fields[index].notes.remove(value)

        for r in range(1, 10, 1):
            for col in range(1, 10, 1):
                if 3 * ((r - 1) // 3) + ((col - 1) // 3) + 1 == box:
                    if r != row or col != column:
                        index = (r - 1) * 9 + col - 1
                        if value in fields[index].notes:
                            fields[index].notes.remove(value)

sudoku = Sudoku("task.txt")
sudoku.solve()

numbers = [0] * 81
for i in range(len(sudoku.fields)):
    numbers[i] = sudoku.fields[i].value
with open('solution.txt', 'w') as file:
    for number in numbers:
        file.write(f"{number}")


'''
solved = 0
not_solved = 0
with open('sudoku.csv', 'r') as csv_file:
    for line in csv_file:
        with open('task.txt', 'w') as task, open('solution2.txt', 'w') as sol:
            t, s = line.strip().split(',')
            task.write(t)
            sol.write(s)

        sudoku = Sudoku("task.txt")
        sudoku.solve()

        numbers = [0] * 81
        for i in range(len(sudoku.fields)):
            numbers[i] = sudoku.fields[i].value
        with open('solution.txt', 'w') as file:
            for number in numbers:
                file.write(f"{number}")

        with open('solution.txt', 'r') as f1, open('solution2.txt', 'r') as f2:
            are_equal = f1.read() == f2.read()  # Compare file contents
            if are_equal:
                solved+=1
            else:
                not_solved+=1

        if solved == 5000:
            print(solved / (solved + not_solved))
            sys.exit("stop")

print(solved/(solved+not_solved))
'''

'''
k = 0
for i in range(len(sudoku.fields)):
    k += 1
    if k == 10:
        print("\n")
        k = 1

    # Format each element to use a fixed-width space (e.g., 10 characters wide)
    print(f"{str(sudoku.fields[i].notes):<14},{str(sudoku.fields[i].value):<1}", end="      ")
'''
