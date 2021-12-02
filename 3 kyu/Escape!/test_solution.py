@test.describe('All tests')
def full_tests():
    from collections import deque
    from random import randint, choice, random, randrange, shuffle
    from itertools import cycle


    def my_escape(grid):
        amount = 0
        squares = {}
        for y, row in enumerate(grid):
            for x, sq in enumerate(row):
                pos = x + 1j * y
                squares[pos] = sq
                if sq == '@':
                    start = pos
                elif sq == '$':
                    end = pos
                elif sq.islower():
                    amount += 1
        open_ = deque()  # [(pos, keys, moves)]
        open_.append((start, frozenset(), 1))
        past = set()
        while open_:
            current, keys, moves = open_.popleft()
            if current == end and len(keys) == amount:
                return moves
            for move in (1, -1, 1j, -1j):
                new_pos = current + move
                new_sq = squares.get(new_pos, '#')
                new_keys = (keys | {new_sq}) if new_sq.islower() else keys
                if new_sq == '#' or (new_pos, new_keys) in past or new_sq.isupper() and new_sq.lower() not in keys:
                    continue
                open_.append((new_pos, new_keys, moves + 1))
                past.add((new_pos, new_keys))
        return None


    def simulate(grid, moves):
        px, py = moves[0]
        
        width = len(grid[0])
        height = len(grid)
        
        if not (0 <= px < width and 0 <= py < height):
            return f"First move doesn't start on the correct position: Position {moves[0]} is out of bounds."

        if grid[py][px] != '@':
            return f"First move doesn't start on the correct position: Position {moves[0]} is a {repr(grid[py][px])}"

        keys = set()
        for i, move in enumerate(moves[1:], 1):
            nx, ny = move

            if not (0 <= nx < width and 0 <= ny < height):
                return f'Moved out of bounds (out of the grid): {move}'

            dist_moved = abs(nx - px) + abs(ny - py) 
            if dist_moved == 0:
                return f"Haven't moved anywhere. Last position: {moves[i - 1]}, next position: {move}"
            elif dist_moved > 1:
                return f'Moved more than one step. Last position: {moves[i - 1]}, next position: {move}'

            sq_val = grid[ny][nx]
            if sq_val == 'X':
                return f'Moved into wall: {move}'
            elif sq_val.islower():
                keys.add(sq_val)
            elif sq_val.isupper() and sq_val.lower() not in keys:
                return f'Walked through door without key: {move}'

            px = nx
            py = ny

        if grid[py][px] != '$':
            return f'Last move doesn\'t end on the correct position: Position {moves[-1]} is a {repr(grid[py][px])}'

        return None

    def tester(grid):
        least_moves = my_escape(grid)
        solution = escape(grid)
        if isinstance(solution, list) and len(solution) == 0:
            test.fail('You returned an empty list.\n' + (f'The correct answer has a solution of {least_moves} moves.' if least_moves else 'The grid was unsolvable.'))
            return

        if least_moves is None:
            if solution is None:
                test.pass_()
            else:
                test.fail(f'Your solution was: {solution}\nHowever, the grid was unsolvable.')
            return
        elif solution is None:
            test.fail(f'You returned None. However a solution was avaliable in {least_moves} moves.')
            return

        try:
            sim = simulate(grid, solution)
        except Exception:
            test.fail(f'The format of your solution is incorrect: {solution}.\nThe correct answer has a solution of {least_moves} moves.')
            return

        if sim:
            test.fail(f'Your solution was: {solution}\nThere was an error with your solution: {sim}.')
        elif len(solution) != least_moves:
            test.fail(f'Your solution was: {solution}\nYou took {len(solution)} moves but the optimal solution takes {least_moves} moves.')
        else:
            test.pass_()

    def gen_grid(size, full_rand=True):
        if size == 1:
            width = randint(5, 10)
            height = randint(5, 10)
        elif size == 2:
            width = randint(10, 25)
            height = randint(10, 25)
        elif size == 3:
            width = randint(25, 50)
            height = randint(25, 50)

        density = random() * .75 if full_rand else .95
        grid = [['#' if random() < density else '.' for _ in range(width)] for _ in range(height)]
        doors_number = randint(size - 1, 4 if size == 1 else 7)
        ALL_DOORS = 'aAbBcCdDeEfFgGhH'

        if full_rand:
            items = set('@$' + ALL_DOORS[:doors_number * 2])
            for item in items:
                ry = rx = None
                while ry is None or grid[ry][rx] in items:
                    ry = randrange(height)
                    rx = randrange(width)
                grid[ry][rx] = item

        else:
            rand_lim = .2 if size == 1 else .08 if size == 2 else .03
            items = ['@'] + list(ALL_DOORS[:doors_number * 2]) + ['$']
            px = randrange(width)
            py = randrange(height)
            past = deque(maxlen=3)
            while items:
                px, py = choice([(px + dx, py + dy) for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)) if 0 <= px + dx < width and 0 <= py + dy < height and (px + dx, py + dy) not in past])
                if grid[py][px] in '#.':
                    if random() < rand_lim:
                        grid[py][px] = items.pop()
                    else:
                        grid[py][px] = '.'
                past.append((px, py))
        return tuple(''.join(row) for row in grid)
                    

    @test.it('Sample tests')
    def sample_tests():
        grid1 = (
            '@...',
            '##.#',
            '$..#'
        )
        grid2 = (
            '.a..',
            '##@#',
            '$A.#'
        )
        grid3 = (
            'aB..',
            '##@#',
            '$Ab#'
        )
        grid4 = (
            '...B...',
            '#$#..#a',
            '##...##',
            'b##.@#.',
            '..A....'
        )
        grid5 = (
            '..a.$',
            'A####',
            '...@.'
        )
        grid6 = (
            '..a..###.@',
            '#B####....',
            '...####.##',
            '...Ab$#.#e',
            '...####.#.',
            '.....E....',
        )
        grid7 = (
            '.#a.C..',
            '.####..',
            'b#.@...',
            'B#...##',
            '.#c.#$.',
            '....A..'
        )
        grid8 = (
            '.c###a.#.b..',
            '#B###..@...#',
            '....##D#.###',
            '.......#A#$.',
            '########.#..',
            '..d......C..'
        )

        grids = [grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8]

        for grid in grids:
            tester(grid)

    def get_order():
        order = [bool(i & 1) for i in range(6)]
        shuffle(order)
        order = cycle(order)
        return order

    @test.it('Smaller random tests')
    def small_tests():
        order = get_order()
        for i in range(31):
            tester(gen_grid(1, next(order)))

    @test.it('Medium random tests')
    def med_tests():
        order = get_order()
        for i in range(31):
            tester(gen_grid(2, next(order)))

    @test.it('Larger random tests')
    def large_tests():
        order = get_order()
        for i in range(31):
            tester(gen_grid(3, next(order)))
