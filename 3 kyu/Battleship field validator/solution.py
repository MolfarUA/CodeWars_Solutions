from itertools import product
from collections import Counter

def is_in_field(field, i, j):
    return i in range(0, len(field)) and j in range(0, len(field[0]))

def get_row_neighbors(field, i, j):
    return [field[i][j+d] for d in [-1, 1] if is_in_field(field, i, j+d)]

def get_col_neighbors(field, i, j):
    return [field[i+d][j] for d in [-1, 1] if is_in_field(field, i+d, j)]

def get_neighbors(field, i, j):
    return get_row_neighbors(field, i, j) + get_col_neighbors(field, i, j)

def get_corner_neigbors(field, i, j):
    return [field[i+d[0]][j+d[1]] for d in product([-1, 1], [-1, 1]) if is_in_field(field, i+d[0], j+d[1])]

def is_empty(field, i, j, f):
    neighbors = f(field, i, j)
    return len(neighbors) == neighbors.count(0)

def is_row_empty(field, i, j): return is_empty(field, i, j, get_row_neighbors)

def is_col_empty(field, i, j): return is_empty(field, i, j, get_col_neighbors)

def is_corner_empty(field, i, j): return is_empty(field, i, j, get_corner_neigbors)

def validate_battlefield(field):
    ships = {
        1: {"name": "Submarine", "number": 4},
        2: {"name": "Destroyer", "number": 3},
        3: {"name": "Crusier", "number": 2},
        4: {"name": "Battleship", "number": 1},
    }
    ship_counter = Counter()
    def check(field, is_trans, ignore_submarine):
        if is_trans: field = list(zip(*field))
        for i in range(len(field)):
            count = 0
            for j in range(len(field[0])):
                if field[i][j] == 1:
                    if not is_corner_empty(field, i, j):
                        return False
                    if not is_row_empty(field, i, j) and not is_col_empty(field, i, j):
                        return False
                    if is_col_empty(field, i, j): count += 1
                if (field[i][j] == 0 or j == len(field[0])-1) and count > 0:
                    if not count in ships:
                        return False
                    if not(count == 1 and ignore_submarine):
                        ship_counter[ships[count]["name"]] += 1
                    count = 0
        return True

    check(field, False, True)  # check row
    check(field, True, False)  # check col
    for ship in ships.values():
        if ship_counter[ship["name"]] != ship["number"]:
            return False
    return True

battleField = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# battleField = [[1,0,0]]
# battleField = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 1, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 1]]
print(validate_battlefield(battleField))
