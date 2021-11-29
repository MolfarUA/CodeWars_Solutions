class Nonogram:

    def __init__ (self, clues):
        self._clues = clues
        pass

    def get_col (self, c, solution):
        row = [x[c] for x in solution]
        return row

    def test_row (self, row, clue):
        result = []
        seq_cnt = 0
        for val in row:
            if val == 1:
                seq_cnt += 1
            else:
                if seq_cnt > 0:
                    result += [seq_cnt]
                seq_cnt = 0
        if seq_cnt > 0:
            result += [seq_cnt]
        return (list(clue) == result)

    def generate_sols (self, row, clue):
        row_sols = [[]]
        for val in row:
            if val == -1:
                for i in range (len(row_sols)):
                    row_sols += [row_sols[i] + [1]]
                    row_sols[i] += [0]
            else:
                for i in range(len(row_sols)):
                    row_sols[i] += [val]

        valid_sols = []
        for sol in row_sols:
            if self.test_row (sol, clue):
                valid_sols += [sol]
        return valid_sols


    def solve (self):
        W = len (self._clues[0])
        H = len (self._clues[1])
        solution = [[-1]*W for x in range(H)]

        while any (-1 in x for x in solution):
            for c,clue in enumerate(self._clues[0]):
                row = self.get_col(c, solution)
                row_sols = self.generate_sols(row, clue)
                for i in range (len(row)):
                    if row[i] == -1:
                        cell_options = [sol[i] for sol in row_sols]
                        if len(set(cell_options)) == 1:
                            solution[i][c] = cell_options[0]

            for r,clue in enumerate (self._clues[1]):
                row = solution[r]
                row_sols = self.generate_sols(row, clue)
                for i in range (len(row)):
                    if row[i] == -1:
                        cell_options = [sol[i] for sol in row_sols]
                        if len(set(cell_options)) == 1:
                            solution[r][i] = cell_options[0]

        return tuple (tuple(row) for row in solution)

clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
         ((1,), (2,), (3,), (2, 1), (4,)))

ans = ((0, 0, 1, 0, 0),
       (1, 1, 0, 0, 0),
       (0, 1, 1, 1, 0),
       (1, 1, 0, 1, 0),
       (0, 1, 1, 1, 1))

print (Nonogram(clues).solve() == ans)

clues = (((1,), (3,), (1,), (3, 1), (3, 1)),
         ((3,), (2,), (2, 2), (1,), (1, 2)))

ans = ((0, 0, 1, 1, 1),
       (0, 0, 0, 1, 1),
       (1, 1, 0, 1, 1),
       (0, 1, 0, 0, 0),
       (0, 1, 0, 1, 1))

print (Nonogram(clues).solve() == ans)

clues = (((3,), (2,), (1, 1), (2,), (4,)),
         ((2,), (3, 1), (1, 2), (3,), (1,)))

ans = ((1, 1, 0, 0, 0),
       (1, 1, 1, 0, 1),
       (1, 0, 0, 1, 1),
       (0, 0, 1, 1, 1),
       (0, 0, 0, 0, 1))

print (Nonogram(clues).solve() == ans)
