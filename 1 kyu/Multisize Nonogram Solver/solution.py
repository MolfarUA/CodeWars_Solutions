from itertools import repeat, groupby, count, chain
import random


def solve(*args):
    return tuple(map(tuple, Nonogram(*args).solve()))


class Memo:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            ans = self.func(*args)
            self.cache[args] = ans
            return ans


class Nonogram:

    __slots__ = ['W', 'H', 'no_of_lines', 'col_clues', 'row_clues',
                 'grid', 'to_linesolve', 'grid_changed', 'solved_lines',
                 'prev_states']

    def __init__(self, clues, width, height):
        self.W, self.H = width, height
        self.no_of_lines = width + height
        self.col_clues, self.row_clues = clues

        self.grid = [[-1 for _ in range(width)] for _ in range(height)]

        self.to_linesolve = sorted(list(zip(repeat('C'), count(), self.col_clues))
                                   + list(zip(repeat('R'), count(), self.row_clues)),
                                    key=lambda x: sum(x[2]), reverse=True)

        self.solved_lines = set()  # set of all the solved lines for lookup

        self.prev_states = []  # list of states in case it needs to guess and backtrack

    def solve(self):
        """Generates the furthest left, and furthest right possible permutation of a row
        and takes the intersection of the points that are the same (line-solving).
        If no more points can be deduced, then it takes a random guess and repeats.
        If the grid becomes invalid, it just backtracks to the last guess."""
        line_solve = self.line_solve
        while len(self.solved_lines) < self.no_of_lines:
            self.grid_changed = False

            try:
                line_solve()
            except InvalidGridError:
                # Resets the grid back to the old state.
                old_grid, old_guess, guess_pos, old_solved_lines = self.prev_states.pop()
                self.grid = [l[:] for l in old_grid]
                self.grid[guess_pos[0]][guess_pos[1]] = old_guess ^ 1  # Swaps the guess
                self.solved_lines = old_solved_lines.copy()
                continue

            if not self.grid_changed and len(self.solved_lines) < self.no_of_lines:
                # Guesses if no extra blocks/gaps have been deduced
                self.guess()
        return self.grid

    def line_solve(self):
        """This method should line solve all the clues in self.line_solve
        using the furthest left, and furthest right to compare which blocks are valid/invalid.
        It may miss a small amount though (limitations of alg), but 'should' be fast(ish)"""
        solved_lines = self.solved_lines
        get_line = self.get_line
        linesolve_helper = self.linesolve_helper
        change_grid = self.change_grid

        for vert, pos, clue in self.to_linesolve:

            if (vert, pos, clue) in solved_lines:
                # If the line is already solved
                continue

            line = get_line(vert, pos)  # The current line so far

            solved = linesolve_helper(line, clue)
            
            if solved is True:
                # The line must be solved
                solved_lines.add((vert, pos, clue))
            elif solved:
                # Changes the grid if the line changed
                change_grid(solved, vert, pos)
                self.grid_changed = True

    def guess(self):
        """Guesses a random choice if nothing can be deduced from linesolving"""
        guess = random.choice((0, 1))

        target = self.find_guess_target()

        # Incase the guess is wrong and needs to backtrack
        self.prev_states.append(([l[:] for l in self.grid],
                                 guess, target,
                                 self.solved_lines.copy()))
        self.grid[target[0]][target[1]] = guess

    def find_guess_target(self):
        """Finds the first unkown square sorted by the length of the sum of the clue,
        and therefore should be more likely to lead to a guess with more impact"""
        for vert, pos, clue in self.to_linesolve:
            if (vert, pos, clue) not in self.solved_lines:
                if vert == 'R':
                    for i, b in enumerate(self.grid[pos]):
                        if b == -1:
                            return (pos, i)
                elif vert == 'C':
                    for i, r in enumerate(self.grid):
                        if r[pos] == -1:
                            return i, pos

    def get_line(self, vert, pos):
        """Gets the specified line"""
        if vert == 'R':
            return tuple(self.grid[pos])
        elif vert == 'C':
            return tuple(row[pos] for row in self.grid)

    def change_grid(self, line, vert, pos):
        """Changes the line in the grid"""
        if vert == 'R':
            self.grid[pos] = list(line)
        elif vert == 'C':
            for i, val in enumerate(line):
                self.grid[i][pos] = val

    @staticmethod
    @Memo
    def linesolve_helper(line, clue):
        """This method first calculates the leftmost and
        rightmost possible permutations of the line.
        Then it find the intersection where there is a overlap of the same colour."""
        length = len(line)

        leftmost = Nonogram.get_leftmost(clue, length, line)
        rightmost = Nonogram.get_leftmost(clue[::-1], length, line[::-1])[::-1]

        solved = Nonogram.find_intersection(leftmost, rightmost, line, length)

        return solved if solved != line else not -1 in line

    @staticmethod
    @Memo
    def get_leftmost(clue, length, filled_line):
        """This method should get the leftmost valid arrangement of all the clues."""

        # List of all blocks in order of clues given.
        # block is [start_pos, end_pos, length]
        blocks = tuple([0, c, c] for c in clue)

        for i, block in enumerate(blocks):
            # Moves the blocks up until they are all in valid positions,
            # but not necessarily covering all the blocked spots.
            if i != 0:
                # Teleports the block to the end of the previous block
                diff = blocks[i - 1][1] - block[0] + 1
                block[0] += diff
                block[1] += diff

            while 0 in filled_line[block[0]:block[1]]:
                # If the block is in an invalid position, then it moves it along 1 square
                block[0] += 1
                block[1] += 1

        while True:
            # Moves the blocks until all the blocked spots are covered.

            line = [0] * length
            # Fills in the line if a block is there.
            for block in blocks:
                line[block[0]:block[1]] = [1] * block[2]

            changed = False
            for i, c in enumerate(filled_line):
                # If a block should be covering a filled square but isn't
                if c == 1 and line[i] == 0:
                    changed = True
                    for block in reversed(blocks):
                        # Finds the first block to the left of the square,
                        # and teleports the right end of the block to the square
                        if block[1] <= i:
                            diff = i - block[1] + 1
                            block[0] += diff
                            block[1] += diff
                            break
                    else:
                        # If no block was found, then the grid must be invalid.
                        raise InvalidGridError('Invalid grid')

            if not changed:
                break

            for i, block in enumerate(blocks):
                # Moves the blocks up until they are not covering any zeros,
                # but not necessarily covering all the blocked spots,
                while 0 in filled_line[block[0]:block[1]]:
                    # If the block is in an invalid spot
                    block[0] += 1
                    block[1] += 1

                if i != 0:
                    # If any block is in an invalid position compared to the previous block
                    if block[0] <= blocks[i - 1][1]:
                        # Teleports the block to 1 square past the end of the previous block
                        diff = blocks[i - 1][1] - block[0] + 1
                        block[0] += diff
                        block[1] += diff

        return tuple(line)

    @staticmethod
    def find_intersection(left, right, line, length):
        """Groups the same blocks together then takes the intersection."""
        leftmost = list(
            chain.from_iterable([i] * len(list(g[1]))
                                for i, g in enumerate(groupby((0,) + left))))[1:]
        rightmost = list(
            chain.from_iterable([i] * len(list(g[1]))
                                for i, g in enumerate(groupby((0,) + right))))[1:]

        solved = tuple(line[i] if line[i] != -1 else -1 if leftmost[i] != rightmost[i]
                       else leftmost[i] % 2 for i in range(length))

        return solved


class InvalidGridError(Exception):
    """Custom Exception for an invalid grid."""
    
##########################
from itertools import repeat, groupby, count, chain
from functools import lru_cache
import random


def solve(*args):
    return tuple(map(tuple, Nonogram(*args).solve()))


class Nonogram:

    __slots__ = ['W', 'H', 'no_of_lines', 'col_clues', 'row_clues',
                 'grid', 'to_linesolve', 'grid_changed', 'solved_lines',
                 'prev_states']

    def __init__(self, clues, width, height):
        self.W, self.H = width, height
        self.no_of_lines = width + height
        self.col_clues, self.row_clues = clues

        self.grid = [[-1 for _ in range(width)] for _ in range(height)]

        self.to_linesolve = sorted(list(zip(repeat('C'), count(), self.col_clues))
                                   + list(zip(repeat('R'), count(), self.row_clues)),
                                    key=lambda x: sum(x[2]), reverse=True)

        self.solved_lines = set()  # set of all the solved lines for lookup

        self.prev_states = []  # list of states in case it needs to guess and backtrack

    def solve(self):
        """Generates the furthest left, and furthest right possible permutation of a row
        and takes the intersection of the points that are the same (line-solving).
        If no more points can be deduced, then it takes a random guess and repeats.
        If the grid becomes invalid, it just backtracks to the last guess."""
        while len(self.solved_lines) < self.no_of_lines:
            self.grid_changed = False

            try:
                self.line_solve()
            except (InvalidGridError, AssertionError):
                # Resets the grid back to the old state.
                old_grid, old_guess, guess_pos, old_solved_lines = self.prev_states.pop()
                self.grid = [l[:] for l in old_grid]
                self.grid[guess_pos[0]][guess_pos[1]] = old_guess ^ 1  # Swaps the guess
                self.solved_lines = old_solved_lines.copy()
                continue

            if not self.grid_changed and len(self.solved_lines) < self.no_of_lines:
                # Guesses if no extra blocks/gaps have been deduced
                self.guess()
        return self.grid

    def line_solve(self):
        """This method should line solve all the clues in self.line_solve
        using the furthest left, and furthest right to compare which blocks are valid/invalid.
        It may miss a small amount though (limitations of alg), but 'should' be fast(ish)"""
        for vert, pos, clue in self.to_linesolve:

            if (vert, pos, clue) in self.solved_lines:
                # If the line is already solved
                continue

            line = tuple(self.get_line(vert, pos))  # The current line so far

            length = len(line)

            leftmost = self.get_leftmost(clue, length, line)
            rightmost = self.get_leftmost(clue[::-1], length, line[::-1])[::-1]

            # Groups the same blocks together then takes the intersection.
            leftmost = list(
                chain.from_iterable([i] * len(list(g[1]))
                                    for i, g in enumerate(groupby([0] + leftmost))))[1:]
            rightmost = list(
                chain.from_iterable([i] * len(list(g[1]))
                                    for i, g in enumerate(groupby([0] + rightmost))))[1:]

            solved = [line[i] if line[i] != -1 else -1 if leftmost[i] != rightmost[i]
                      else leftmost[i] % 2 for i in range(length)]

            if tuple(solved) != line:
                # Changes the grid if the line changed
                self.change_grid(solved, vert, pos)
                self.grid_changed = True
            elif -1 not in line:
                # The line must be solved
                self.solved_lines.add((vert, pos, clue))

    def guess(self):
        """Guesses a random choice if nothing can be deduced from linesolving"""
        guess = random.choice((0, 1))

        target = self.find_guess_target()

        # Incase the guess is wrong and needs to backtrack
        self.prev_states.append(([l[:] for l in self.grid],
                                 guess, target,
                                 self.solved_lines.copy()))
        self.grid[target[0]][target[1]] = guess

    def find_guess_target(self):
        """Finds the first unkown square sorted by the length of the sum of the clue,
        and therefore should be more likely to lead to a guess with more impact"""
        for vert, pos, clue in self.to_linesolve:
            if (vert, pos, clue) not in self.solved_lines:
                if vert == 'R':
                    for i, b in enumerate(self.grid[pos]):
                        if b == -1:
                            return (pos, i)
                elif vert == 'C':
                    for i, r in enumerate(self.grid):
                        if r[pos] == -1:
                            return i, pos

    def get_line(self, vert, pos):
        """Gets the specified line"""
        if vert == 'R':
            return self.grid[pos]
        elif vert == 'C':
            return [row[pos] for row in self.grid]

    def change_grid(self, line, vert, pos):
        """Changes the line in the grid"""
        if vert == 'R':
            self.grid[pos] = line
        elif vert == 'C':
            for i, val in enumerate(line):
                self.grid[i][pos] = val

    @staticmethod
    @lru_cache(maxsize=None)  # Has around a 60% hit ratio
    def get_leftmost(clue, length, filled_line):
        """This method should get the leftmost valid arrangement of all the clues."""

        # List of all blocks in order of clues given
        blocks = [Block(0, c) for c in clue]

        for i, block in enumerate(blocks):
            # Moves the blocks up until they are all in valid positions,
            # but not necessarily covering all the blocked spots.
            if i != 0:
                # Teleports the block to the end of the previous block
                block += blocks[i - 1].end_pos - block.start_pos + 1
            while True:
                # If the block is in an invalid position, then it moves it along 1 square
                if 0 in filled_line[block.start_pos:block.end_pos]:
                    block += 1
                else:
                    break

        while True:
            # Moves the blocks until all the blocked spots are covered.
            # I'm pretty sure this works but you may end up hitting a special case or something.

            line = [0] * length
            # Fills in the line if a block is there.
            for block in blocks:
                line[block.start_pos:block.end_pos] = [1] * len(block)

            changed = False
            for i, c in enumerate(filled_line):
                # If a block should be covering a filled square but isn't
                if c == 1 and line[i] == 0:
                    changed = True
                    for block in reversed(blocks):
                        # Finds the first block to the left of the square,
                        # and teleports the right end of the block to the square
                        if block.end_pos <= i:
                            block += i - block.end_pos + 1
                            break
                    else:
                        # If no block was found, then the grid must be invalid.
                        raise InvalidGridError('Invalid grid')

            if not changed:
                break

            for i, block in enumerate(blocks):
                # Moves the blocks up until they are not covering any zeros,
                # but not necessarily covering all the blocked spots,
                while True:
                    # If the block is in an invalid spot
                    if 0 in filled_line[block.start_pos:block.end_pos]:
                        changed = True
                        block += 1
                    else:
                        break
                if i != 0:
                    # If any block is in an invalid position compared to the previous block
                    if block.start_pos <= blocks[i - 1].end_pos:
                        changed = True
                        # Teleports the block to 1 square past the end of the previous block
                        block += blocks[i - 1].end_pos - block.start_pos + 1

        line = [0] * length
        for block in blocks:
            line[block.start_pos:block.end_pos] = [1] * len(block)
        return line


class Block:
    """Block class used for generating the leftmost permutation of a line.
    A Block represents one part of a clue. ie. a black block."""

    __slots__ = ['start_pos', 'end_pos', 'length']

    def __init__(self, start_pos, length):
        self.start_pos = start_pos
        self.end_pos = start_pos + length
        self.length = length

    def __add__(self, other):
        """adds an integer to the start_pos and end_pos of the Block."""
        if isinstance(other, int):
            return Block(self.start_pos + other, self.end_pos + other, self.length)

    def __iadd__(self, other):
        """adds an integer to the start_pos and end_pos.
            Essentially moves the block forwards."""
        if isinstance(other, int):
            self.start_pos += other
            self.end_pos += other
            return self

    def __len__(self):
        """return the length of the block. This should be the number in the clue."""
        return self.length

    def __str__(self):
        """String representation. Shows the start position, end position and length."""
        return 'Block object. start_pos: {}, end_pos: {}, length: {}'.format(self.start_pos, self.end_pos, self.length)


class InvalidGridError(Exception):
    """Custom Exception for an invalid grid."""
    
############################################
from collections import deque

def is_done(field):
    for r in field:
        if 9 in r:
            return False
    return True


def get_cor(field, t):
    x, d = t
    if d:
        cor = [r[x] for r in field]
    else:
        cor = field[x]
    zeros = 0
    ones = 0
    for i, c in enumerate(cor):
        if c == 1:
            ones |= 1 << i
        elif c == 0:
            zeros |= 1 << i
    return cor, zeros, ones


def set_cor(field, t, i, v):
    x, d = t
    if d:
        field[i][x] = v
    else:
        field[x][i] = v


def get_pos(cor_t, clues, pos, cur_p=0, cur_zero=0, cur_one=0):
    cor, cor_zero, cor_one = cor_t
    left = len(cor) - cur_p
    if len(clues) == 0:
        if left < 0:
            left = 0
        if left > 0 and 1 in cor[-left:]:
            return
        for j in range(left):
            cur_zero |= 1 << cur_p + j
        pos.append((cur_zero, cur_one))
        return
    follower_set = sum(clues[1:])
    follower_len = follower_set + len(clues) - 1
    clue = clues[0]
    for i in range(left - follower_len - clue + 1):
        n_p = cur_p
        n_zero = cur_zero
        n_one = cur_one
        for j in range(i):
            n_zero |= 1 << (cur_p + j)
        n_p += i
        for j in range(clue):
            n_one |= 1 << (n_p + j)
        n_p += clue
        if len(clues) > 1:
            n_zero |= 1 << (cur_p + i + clue)
            n_p += 1
        if n_zero & cor_one or n_one & cor_zero:
            continue
        get_pos(cor_t, clues[1:], pos, n_p, n_zero, n_one)
    return


def filter_pos(field, pos, t, x):
    _, cor_zero, cor_one = get_cor(field, t)
    comp_zero = cor_zero & (1 << x)
    comp_one = cor_one & (1 << x)
    n_pos = [(zero, one) for zero, one in pos if zero & comp_zero or one & comp_one]
    return n_pos


def set_fields(field, pos, t):
    x, d = t
    cor, cor_zero, cor_one = get_cor(field, t)
    any_zero, any_one = 0, 0
    for p in pos:
        zero, one = p
        any_zero |= zero
        any_one |= one
    changed = []
    for i in range(len(cor)):
        if cor[i] != 9:
            continue
        zero = any_zero & (1 << i)
        one = any_one & (1 << i)
        if zero and not one:
            set_cor(field, t, i, 0)
            changed.append((i, not d, x))
        elif not zero and one:
            set_cor(field, t, i, 1)
            changed.append((i, not d, x))
        elif not zero and not one:
            raise Exception
    return changed


def solve_loop(field, a, start):
    check = deque(start)
    later = []
    while check:
        i, d, x = check.popleft()
        if (i, d) in a:
            pos = filter_pos(field, a[(i, d)], (i, d), x)
            new = set_fields(field, pos, (i, d))
            for n in new:
                check.append(n)
            a[(i, d)] = pos
        else:
            later.append((i, d, x))
    return later


def get_sort_order(t, field):
    i, d, cs = t
    cor, _, _ = get_cor(field, (i, d))
    known = len([x for x in cor if x != 9])
    return (len(cor) - sum(cs) - known) ** len(cs)


def solve_deq(field, deq, a):
    while deq:
        k = deq.popleft()
        i, d, x = k
        pos = filter_pos(field, a[(i, d)], (i, d), x)
        new = set_fields(field, pos, (i, d))
        for n in new:
            deq.append(n)
        a[(i, d)] = pos


def guess(field, a):
    to_check = sorted([k for k in a if len(a[k]) > 1], key=lambda x: len(a[x]))[0]
    for pa in a[to_check]:
        n_field = [x[:] for x in field]
        n_a = {k: a[k][:] for k in a}
        n_a[to_check] = [pa]
        new = set_fields(n_field, [pa], to_check)
        try:
            solve_loop(n_field, n_a, new)
        except:
            continue
        if is_done(n_field):
            return n_field
        res = guess(n_field, n_a)
        if res:
            return res


def solve(clues, width, height):
    field = [[9] * width for _ in range(height)]
    a = {}
    deq = deque()
    my_clues = []
    for d in [True, False]:
        for i, cs in enumerate(clues[not d]):
            my_clues.append((i, d, cs))
    my_clues.sort(key=lambda x: get_sort_order(x, field))
    while my_clues:
        i, d, cs = my_clues.pop(0)
        pos = []
        get_pos(get_cor(field, (i, d)), cs, pos)
        a[(i, d)] = pos
        new = set_fields(field, pos, (i, d))
        later = solve_loop(field, a, new)
        for n in later:
            deq.append(n)
        my_clues.sort(key=lambda x: get_sort_order(x, field))
    solve_deq(field, deq, a)

    if not is_done(field):
        field = guess(field, a)
    t = tuple([tuple(f) for f in field])
    return t
  
#########################################
import numpy as np
from scipy.special import binom
from itertools import product, combinations

import time

def nintom(n, m, out=[]):
    if m == 2:
        for i in range(n+1):
            yield out+[i]
    else:
        for i in range(n+1):
            yield from nintom(n-i,m-1, out+[i])

def cluetosetnp(clue, dim):
    cluesn = len(clue)
    boxes = cluesn+1
    freespaces = dim-sum(clue)-cluesn+1
    spacesarr = np.array(list(nintom(freespaces,boxes)),int)
    N = len(spacesarr)
    allrows = list(range(N))
    out = np.zeros([N, dim], int)
    offset = 0
    for i in range(cluesn):
        for j in range(clue[i]):
            out[allrows, spacesarr[:,i] + (offset+j)] = 1
        if i < cluesn-1:
            spacesarr[:,i+1] += spacesarr[:,i]
        offset += clue[i]+1
    return out



def cluetosetnp(clue, dim):
    cluesn = len(clue)
    spaces = dim-sum(clue)
    spacesarr = np.array(list(combinations(range(spaces+1),cluesn)),int)
    N = len(spacesarr)
    allrows = list(range(N))
    out = np.zeros([N, dim], int)
    offset = 0
    for i in range(cluesn):
        for j in range(clue[i]):
            out[allrows, spacesarr[:,i] + (offset+j)] = 1
        offset += clue[i]
    return out


def cluetosetl(clue, dim, res = []):
    blocks_next = len(clue)-1  #blocks after this one
    if blocks_next:
        leave = sum(clue[1:]) + blocks_next  # minimum space for subsequent including afterspace
        maxpos = dim -leave - clue[0] + 1          #maximum position of first black of the first block   
        for i in range(0, maxpos):
            res_new = res + [0]*i + [1]*clue[0] +[0]
            yield from cluetosetl(clue[1:], dim - i - clue[0] - 1, res_new)   
    else:
        maxpos = dim - clue[0] + 1
        for i in range(0, maxpos):
            res_new = res + [0]*i + [1]*clue[0] + [0]*(dim - i - clue[0] )
            yield res_new
                
def cluestoset(clues, dim, frac=0.7, maxn = 4000, smalln = 40):
    sizes = [int(binom(dim-sum(clue), len(clue))) for clue in clues]
    size_frac = sorted(sizes)[int(1+frac*len(sizes))]
    maxn = min(max(maxn, size_frac),40000)    
   
    def cluetoset(clue, size, dim):
        if not clue:
            return np.array([[0]*dim])    
        if size > maxn:
            return [[size, None], None]
        if size < smalln:
            return np.array(list(cluetosetl(clue, dim)))    
        return cluetosetnp(clue, dim)
    
    return [cluetoset(clue, size, dim) for clue, size in zip(clues, sizes) ]
    
def comp(need, have):
    if 0 not in have and 1 not in have:
       return True
    for n, h in zip(need, have):
        if h!=-1 and n!=h:
            return False
    return True
            
def cluetoset2(clue, filled, res = []):
    dim = len(filled)
    cluecur = clue[0]
    blocks_next = len(clue)-1  #blocks after this one
    if blocks_next:
        leave = sum(clue[1:]) + blocks_next  # minimum space for subsequent including afterspace
        maxpos = dim -leave - cluecur + 1          #maximum position of first black of the first block         
    else:
        maxpos = dim - cluecur + 1
    if 1 in filled[:maxpos]:
        maxpos = filled.index(1)+1  
        
    minpos = 0
    
    for i in range(minpos, maxpos):
        res_new = res + [0]*i + [1]*cluecur
        if blocks_next:
            if not comp([1]*cluecur+[0], filled[i : i+cluecur+1]):
                continue
            yield from cluetoset2(clue[1:], filled[ (i+cluecur+1) : ], res_new + [0] )
        else:
           if not comp([1]*cluecur, filled[i : i+cluecur]):
               continue
           if 1 in filled[i+cluecur:]:
               continue  
           yield res_new + [0]*(dim - i - cluecur )            

def possibles(perms,i):
    if perms[0][1] == None: return 10
    a = perms[0,i]
    if a:
        if 0 in perms[:,i].tolist():
            return 10
    else:
        if 1 in perms[:,i].tolist():
            return 10
    return a            
        
def solve(clues, width=15, height=15, frac=0.6, maxn = 1000, smalln = 40): 
    print(width, height)
    print(clues)    
    rows = cluestoset(clues[1], width, frac, maxn, smalln)
    cols = cluestoset(clues[0], height, frac, maxn, smalln)
    filled = np.zeros([height, width], dtype = int)-1
    rowpossibles = filled.copy()
    colpossibles = filled.copy()
    
    def crossinfer(ite):
        totalconds_prev = None
        for it in range(ite):
            rconds = max([len(row) for row in rows])
            cconds = max([len(col) for col in cols])
            totalconds = sum([len(row) for row in rows]) + sum([len(col) for col in cols])
           
            for r in range(height):
                for c in range(width):
                    if filled[r,c] != -1:
                        continue
                    
                    if rowpossibles[r,c] > -1:
                        r_possible = rowpossibles[r,c]
                    else:
                        r_possible =  possibles(rows[r],c)
                        rowpossibles[r,c] = r_possible
                    if colpossibles[r,c] > -1:
                        c_possible = colpossibles[r,c]
                    else:
                        c_possible =  possibles(cols[c],r)
                        colpossibles[r,c] = r_possible       
                             
                    if r_possible != c_possible:
                        if r_possible == 10:
                            if rows[r][0][1] != None:
                                rows[r] = rows[r][ rows[r][:,c] == c_possible , : ]
                            filled[r,c] = c_possible
                            rowpossibles[r,:] = filled[r,:]   
                        if c_possible == 10:
                            if cols[c][0][1] != None:
                                cols[c] = cols[c][ cols[c][:,r] == r_possible , : ]
                            filled[r,c] = r_possible
                            colpossibles[:,c] = filled[:,c] 
                    elif r_possible < 2:
                            filled[r,c] = r_possible
                            
            rconds = max([len(row) for row in rows])
            cconds = max([len(col) for col in cols])
            totalconds = sum([len(row) for row in rows]) + sum([len(col) for col in cols])

            if rconds == 1:
                return tuple(tuple(row[0]) for row in rows)
            if cconds == 1:
                return tuple( tuple(cols[c][0][r] for c in range(width)) for r in range(height))
            if totalconds == totalconds_prev:
                break
            totalconds_prev = totalconds
    
        
    def getbiggerconditions(maxset):
        if any([ r[0][1]==None for r in rows]) or any([c[0][1]==None for c in cols]):
            for i, r in enumerate(rows):
                if r[0][1] != None and len(r)==1:
                    filled[i] = r[0]
            for i, c in enumerate(cols):
                if c[0][1] != None and len(c)==1:
                    filled[:,i] = c[0]
            
            for i in range(height):
                if rows[i][0][1] == None and rows[i][0][0] < maxset:
                    rows[i] = np.array(list(cluetoset2(clues[1][i], filled[i].tolist())),int)
                    rowpossibles[i,:] = filled[i,:] 
            for i in range(width):
                if cols[i][0][1] == None and cols[i][0][0] < maxset:
                    cols[i] = np.array(list(cluetoset2(clues[0][i], filled[:,i].tolist())),int)
                    colpossibles[:,i] = filled[:,i] 
            
            result = crossinfer(50)
            if result:
                return result 
  
    def multiinfer(size1, size2):
        rows_size = sorted([(i, len(r)) for i, r in enumerate(rows) if r[0][1] != None and 1<len(r)<size2 ], key = lambda x:x[1] )
        cols_size = sorted([(i, len(c)) for i, c in enumerate(cols) if c[0][1] != None and 1<len(c)<size2 ], key = lambda x:x[1] )
        def selectset(sizes, size1):
            p = 1; myset = []
            for s in sizes:
                p = p*s[1]
                if p > size1: return myset
                myset.append(s[0])
            return myset
        w, h = len(selectset(cols_size, size1)), len(selectset(rows_size, size1))
        if  h < 2 and w < 2:
            return None
        
        if h > w:
            transpose = False
            rowset = sorted(selectset(rows_size, size1))
            colset = sorted([a[0] for a in cols_size])
            s_rows = [a[:,colset]  for i, a in enumerate(rows) if i in rowset]
            s_cols = [a[:,rowset].tolist()  for i, a in enumerate(cols) if i in colset]                   
        else:
            transpose = True
            rowset = sorted(selectset(cols_size, size1))
            colset = sorted([a[0] for a in rows_size])
            s_rows = [a[:,colset]  for i, a in enumerate(cols) if i in rowset]
            s_cols = [a[:,rowset].tolist()  for i,a in enumerate(rows) if i in colset]
            h = w
        
        w = len(s_cols)
        s_filled = np.zeros([h,w], int)
        allowed = []
        count = 0
        for prod in product(*s_rows):
            s_filled = np.array(prod,int)
            for i in range(w):
                if s_filled[:,i].tolist() not in s_cols[i]:
                    break
            else:
                allowed.append(s_filled)
            count += 1
    
        s_rows = [a.tolist() for a in s_rows]
        for r in range(h):
            allowedvalues = [a[r].tolist() for a in allowed]
            l = []
            for i in range(len(s_rows[r])):
                if s_rows[r][i] in allowedvalues:
                    l.append(i)
            if len(l) < len(s_rows[r]):
                if not transpose:
                    rows[rowset[r]] = rows[rowset[r]][l , :]
                    rowpossibles[rowset[r],:] = filled[rowset[r],:]
                else:
                    cols[rowset[r]] = cols[rowset[r]][l , :]
                    colpossibles[:, rowset[r]] = filled[:, rowset[r]]                    

        for c in range(w):
            allowedvalues = [a[:, c].tolist() for a in allowed]
            l = []
            for i in range(len(s_cols[c])):
                if s_cols[c][i] in allowedvalues:
                    l.append(i)
            if len(l) < len(s_cols[c]):
                if not transpose:
                    cols[colset[c]] = cols[colset[c]][l , :]
                    colpossibles[:, colset[c]] = filled[:, colset[c]]
                else:
                    rows[colset[c]] = rows[colset[c]][l , :]
                    rowpossibles[colset[c], : ] = filled[colset[c], :]                     
 
    
    result = crossinfer(50)
    if result:
        return result
    
    multiinfer(3000, 10000)
    
    result = crossinfer(50)
    if result:
        return result
    
    result = getbiggerconditions(10**25)   
    if result:
        return result
    
    multiinfer(3000, 10000)
    
    result = crossinfer(50)
    if result:
        return result       
    
    

    result = getbiggerconditions(10**50)   
    if result:
        return result 
    
    
    multiinfer(3000, 10000)
    
    result = crossinfer(50)
    if result:
        return result    
    
    
    multiinfer(10000, 50000)
    
    result = crossinfer(50)
    if result:
        return result     
    
    print(filled)        
        
    return False
  
##############################################
import re

def prefill(xs, clue):
    end, n, k = [], len(xs), len(clue)
    i = 0
    for c in clue:
        i += c
        end.append(i)
        i += 1
    i = n - 1
    for c in range(k - 1, -1, -1):
        i -= clue[c] - 1
        if i < (j := end[c]):
            xs[i:j] = ['x'] * (j - i)
            if j - i == clue[c] and j < n - 1:
                xs[j] = '.'
        i -= 2
    return xs

def solve_local_re(xs, clue):
    if not clue.match(''.join(xs)):
        return None, False
    changed = False
    for i in range(len(xs)):
        if xs[i] == '?':
            xs[i] = 'x'
            s = ''.join(xs)
            if not clue.match(s):
                xs[i] = '.'
                changed = True
            else:
                xs[i] = '.'
                s = ''.join(xs)
                if not clue.match(s):
                    xs[i] = 'x'
                    changed = True
                else:
                    xs[i] = '?'
    return xs, changed

def solve(clues, w, h):
    col_clues, row_clues = clues
    init = [prefill(['?'] * w, row_clues[i]) for i in range(h)]
    for j in range(w):
        col = prefill([init[i][j] for i in range(h)], col_clues[j])
        for i in range(h):
            init[i][j] = col[i]

    def clue_to_re(clue):
        if not clue: return re.compile('^[^x]*$')
        return re.compile(f'^[^x]*[x?]{{{clue[0]}}}' + ''.join(f'[^x]+[x?]{{{c}}}' for c in clue[1:]) + '[^x]*$')

    col_clues, row_clues = [*map(clue_to_re, col_clues)], [*map(clue_to_re, row_clues)]

    def search(grid):
        changed = True
        while changed:
            changed = False
            for i in range(h):
                r = grid[i]
                r, c = solve_local_re(r, row_clues[i])
                if not r: 
                    return None
                changed |= c
            for j in range(w):
                r = [grid[i][j] for i in range(h)]
                r, c = solve_local_re(r, col_clues[j])
                if not r:
                    return None
                if c:
                    changed = True
                    for i in range(h): 
                        grid[i][j] = r[i]
        if any('?' in row for row in grid):
            i = min(range(h), key=lambda i: grid[i].count('?') or w)
            j = grid[i].index('?')
            copy = [row[:] for row in grid]
            copy[i][j] = 'x'
            sol1 = search(copy)
            if sol1: return sol1
            grid[i][j] = '.'
            return search(grid)
        return grid
    return tuple(tuple(-1 if x == '?' else 0 if x == '.' else 1 for x in row) for row in search(init))
  
############################################
import re
from itertools import product

class NonogramSolver:
    ERROR, VERTICAL, HORIZONTAL = range(-1, 2)
    UNKOWNS, WHITES, BLACKS = range(-1, 2)

    def __init__(self, clues):
        self.vClues, self.hClues = clues
        self.width, self.height = map(len, clues)
        self.unkowns = {*product(range(self.height), range(self.width))}
        self.whites, self.blacks = set(), set()
        self.patterns = [[*map(self.getPatterns, self.vClues)]]
        self.patterns += [[*map(self.getPatterns, self.hClues)]]
        self.queue = {*product((self.VERTICAL,), range(self.width))}
        self.queue |= {*product((self.HORIZONTAL,), range(self.height))}
        self.updates, self.guessing = [], False

    def getPatterns(self, clues):
        patterns = [f"([UB]{{{clue}}})" for clue in clues]
        patterns = map("[UW]+?".join, (patterns, patterns[::-1]))
        return [re.compile("[UW]*?" + pattern + "[UW]*") for pattern in patterns]

    def getBestGuess(self):
        maxUpdates, guessList = -1, [*self.unkowns]
        for c, t in product(guessList, (self.WHITES, self.BLACKS)):
            updates = 0
            self.updates.append([set(), set()])
            self.updateUnkowns({c}, t)
            self.queue |= {*zip((self.HORIZONTAL, self.VERTICAL), c)}
            result = self.logicalSolve()
            self.undoUpdates()
            if result == self.ERROR: return [c, [1 - t]]
            if not self.unkowns: return [c, [t]]
            if updates > maxUpdates:
                maxUpdates = updates; guess = [c, [1 - t, t]]
        return guess

    def updateUnkowns(self, n, t):
        self.unkowns -= n
        [self.whites, self.blacks][t] |= n
        if self.guessing: self.updates[-1][t] |= n

    def undoUpdates(self):
        for n, kowns in zip(self.updates.pop(), (self.whites, self.blacks)):
            self.unkowns |= n; kowns -= n

    def lineSolve(self, line):
        d, cFixed = line
        bound = [self.height, self.width][d]
        clues = [self.vClues, self.hClues][d][cFixed]
        lineCells = {*product(*((range(bound), (cFixed,))[::(-1) ** d]))}
        lineKowns = lineCells & self.whites, lineCells & self.blacks
        lineKowns = [*map(lambda s: {c[d] for c in s}, lineKowns)]
        strLine = ["U"] * bound
        for kowns, s in zip(lineKowns, "WB"):
            for x in kowns: strLine[x] = s
        strLine = "".join(strLine)
        patterns = self.patterns[d][cFixed]
        matches = [p.fullmatch(s) for p, s in zip(patterns, (strLine, strLine[::-1]))]
        if not all(matches): return self.ERROR
        starts = [[*map(m.start, range(1, len(clues) + 1))] for m in matches]
        starts[1] = [bound - c - 1 for c in starts[1]][::-1]
        news, lastEnd = [set(), set()], 0
        for lStart, rStart, clue in zip(starts[0], starts[1], clues):
            news[0] |= {*range(lastEnd, lStart)}
            lastEnd = rStart + 1
            news[1] |= {*range(lastEnd - clue, lStart + clue)}
        news[0] |= {*range(lastEnd, bound)}
        for n, kowns in zip(news, lineKowns): n -= kowns
        return news

    def logicalSolve(self):
        while self.queue:
            d, cFixed = self.queue.pop()
            news = self.lineSolve((d, cFixed))
            if news == self.ERROR: return self.ERROR
            for x in news[0] | news[1]: self.queue.add((1 - d, x))
            news = [*map(lambda s: {(c, cFixed)[::(-1) ** d] for c in s}, news)]
            for n, t in zip(news, [self.WHITES, self.BLACKS]): self.updateUnkowns(n, t)

    def guess(self):
        self.guessing = True
        guesses = [self.getBestGuess()]
        while True:
            c, types = guesses[-1]
            self.updates.append([set(), set()])
            self.updateUnkowns({c}, types[-1])
            self.queue |= {*zip((self.HORIZONTAL, self.VERTICAL), c)}
            if self.logicalSolve() == self.ERROR:
                while True:
                    types.pop()
                    self.undoUpdates()
                    if types: break
                    guesses.pop()
                continue
            if not self.unkowns: break
            guesses += [self.getBestGuess()]
        self.guessing = False

    def solve(self):
        self.logicalSolve()
        if self.unkowns: self.guess()
        result = [[0] * self.width for x in range(self.height)]
        for x, y in self.blacks: result[x][y] = 1
        return tuple(map(tuple, result))

def solve(clues, width, height):
    return NonogramSolver(clues).solve()
  
##############################################
import copy

class RowOrCol:
    def __init__(self, is_horizontal, index):
        self.is_horizontal = is_horizontal
        self.index = index
    def __repr__(self): 
        return "RowOrCol({},{})".format(self.is_horizontal, self.index)

class FilterPossibilitiesTask:
    def __init__(self, row_or_col, changed_value_index):
        self.row_or_col = row_or_col
        self.changed_value_index = changed_value_index
    def __repr__(self): 
        return "FilterPossibilitiesTask({},{})".format(self.row_or_col, self.changed_value_index)

class RunInfo:
    def __init__(self, length, possible_starts):
        self.length = length
        self.possible_starts = possible_starts
    def __repr__(self): 
        return "RunInfo({},{})".format(self.length, self.possible_starts)

def init_row_or_col_info(clues, other_size):
    result = []
    for clue_list in clues:
        row_or_col_info = []
        if clue_list:
            total_size = sum(clue_list) + len(clue_list) - 1
            min = 0
            max = other_size - total_size
            for j in clue_list:
                row_or_col_info.append(RunInfo(j, list(range(min, max + 1))))
                min += j + 1
                max += j + 1
        result.append(row_or_col_info)
    return result

class State:
    def __init__(self, top_clues, left_clues):
        self.result = [[255 for j in range(0, len(top_clues))] for i in range(0, len(left_clues))]
        self.col_info = init_row_or_col_info(top_clues, len(left_clues))
        self.row_info = init_row_or_col_info(left_clues, len(top_clues))
        self.unfilled_fields = len(left_clues) * len(top_clues)
        self.infer_values_tasks = set([RowOrCol(False, i) for i in range(0, len(top_clues))] + [RowOrCol(True, i) for i in range(0, len(left_clues))])
        self.filter_possibilities_tasks = set()

    def find_unfilled_field(self):
        for i in range(len(self.result)):
            for j in range(len(self.result[i])):
                if self.result[i][j] == 255:
                    return (i, j)
        raise Exception("")
    
    def solve(self):
        while len(self.infer_values_tasks) + len(self.filter_possibilities_tasks) > 0:
            infer_values_tasks = self.infer_values_tasks
            self.infer_values_tasks = set()
            for task in infer_values_tasks:
                self.infer_values(task)
            filter_possibilities_tasks = self.filter_possibilities_tasks
            self.filter_possibilities_tasks = set()
            for task in filter_possibilities_tasks:
                self.filter_possibilities(task)
        if self.unfilled_fields > 0:
            (row, col) = self.find_unfilled_field()
            clone = copy.deepcopy(self)
            row_or_col = RowOrCol(False, col)
            result = clone.try_solve_with_fixed_value(row_or_col, row, 0)
            if result:
                return result
            else:
                return self.try_solve_with_fixed_value(row_or_col, row, 1)
            
        
        return self.result
    def try_solve_with_fixed_value(self, row_or_col, other_index, value):
        self.set_value(row_or_col, other_index, value)
        self.filter_possibilities_tasks.add(FilterPossibilitiesTask(row_or_col, other_index))
        try:
            return self.solve()
        except:
            return None
        
    
    def count(self, is_horizontal):
        if is_horizontal:
            return len(self.result[0])
        else:
            return len(self.result)
        
    def info(self, row_or_col: RowOrCol):
        if row_or_col.is_horizontal:
            return self.row_info[row_or_col.index]
        else:
            return self.col_info[row_or_col.index]
    
    def get_result(self, row_or_col, other_index):
        if row_or_col.is_horizontal:
            return self.result[row_or_col.index][other_index]
        else:
            return self.result[other_index][row_or_col.index]
    
    def set_value(self, row_or_col, other_index, value):
        result = self.get_result(row_or_col, other_index)
        if result <= 1 and result != value:
            raise Exception("")
        elif result > 1:
            if row_or_col.is_horizontal:
                self.result[row_or_col.index][other_index] = value
            else:
                self.result[other_index][row_or_col.index] = value
            self.unfilled_fields -= 1
            self.filter_possibilities_tasks.add(FilterPossibilitiesTask(RowOrCol(not row_or_col.is_horizontal, other_index), row_or_col.index))
            return True
        else:
            return False
    
    def infer_values(self, row_or_col):
        size = self.count(row_or_col.is_horizontal)
        sometimes_occupied = [False] * size
        always_occupied = [True] * size
        info = self.info(row_or_col)
        
        if len(info) == 0:
            always_occupied = [False] * size
        else:
            for run_index in range(len(info)):
                run = info[run_index]
                a = run.possible_starts[0]
                b = run.possible_starts[0]
                for possible_start in run.possible_starts:
                    if possible_start < a or b < possible_start:
                        # ranges are disjoint
                        sometimes_occupied[a:b] = [True] * (b - a)
                        a = possible_start
                    b = possible_start + run.length
                sometimes_occupied[a:b] = [True] * (b - a)
                if run_index == 0:
                    always_occupied[0:run.possible_starts[-1]] = [False] * run.possible_starts[-1]
                else:
                    begin_not_always_occupied_range = info[run_index - 1].possible_starts[0] + info[run_index - 1].length
                    always_occupied[begin_not_always_occupied_range:run.possible_starts[-1]] = [False] * (run.possible_starts[-1] - begin_not_always_occupied_range)
                if run_index == len(info) - 1:
                    always_occupied[run.possible_starts[0] + run.length:] = [False] * (len(always_occupied) - (run.possible_starts[0] + run.length))
        for i in range(size):
            if not sometimes_occupied[i]:
                self.set_value(row_or_col, i, 0)
            elif always_occupied[i]:
                self.set_value(row_or_col, i, 1)
    
    def filter_possibilities(self, task):
        value = self.get_result(task.row_or_col, task.changed_value_index)
        info = self.info(task.row_or_col)
        changed = False
        if value == 0:
            for run in info:
                left_index = index_of(run.possible_starts, lambda x: x + run.length > task.changed_value_index)
                if left_index >= 0:
                    right_index = index_of(run.possible_starts, lambda x: x > task.changed_value_index)
                    if right_index >= 0:
                        if right_index > left_index:
                            run.possible_starts = run.possible_starts[:left_index] + run.possible_starts[right_index:]
                            changed = True
                    else:
                        if left_index == 0:
                            raise Exception("")
                        run.possible_starts = run.possible_starts[:left_index]
                        changed = True
        else:
            for run in info:
                index = index_of(run.possible_starts, lambda x: x + run.length == task.changed_value_index)
                if index >= 0:
                    del run.possible_starts[index]
                    changed = True
                index = index_of(run.possible_starts, lambda x: x == task.changed_value_index + 1)
                if index >= 0:
                    del run.possible_starts[index]
                    changed = True
                if len(run.possible_starts) == 0:
                    raise Exception("")
                
            
            changed = filter_unique_runs_for_an_occupied_place(info, task.changed_value_index) or changed
            
        if changed:
            self.infer_values_tasks.add(task.row_or_col)

        while changed:
            changed = False
            
            for i in reversed(range(len(info) - 1)):
                length = info[i].length
                max_previous_start = info[i + 1].possible_starts[-1]
                left_index = index_of(info[i].possible_starts, lambda x: x + length >= max_previous_start)
                if left_index >= 0:
                    if left_index == 0:
                        raise Exception("")
                    info[i].possible_starts = info[i].possible_starts[:left_index]
            
            for i in range(1, len(info)):
                length = info[i - 1].length
                min_previous_end = info[i - 1].possible_starts[0] + length
                left_index = index_of(info[i].possible_starts, lambda x: x > min_previous_end)
                if left_index >= 0:
                    if left_index > 0:
                        info[i].possible_starts = info[i].possible_starts[left_index:]
                else:
                    raise Exception("")
        
            for i in range(self.count(task.row_or_col.is_horizontal)):
                if self.get_result(task.row_or_col, i) == 1:
                    changed = filter_unique_runs_for_an_occupied_place(info, i) or changed
            
    
def filter_unique_runs_for_an_occupied_place(info, index):
    changed = False
    runs = [run for run in info if any(start <= index and start + run.length > index for start in run.possible_starts)]
    if len(runs) == 0:
        raise Exception("")
    elif len(runs) == 1:
        run = runs[0]
        left_index = index_of(run.possible_starts, lambda x: x + run.length > index)
        right_index = index_of(run.possible_starts, lambda x: x > index)
        if right_index >= 0:
            run.possible_starts = run.possible_starts[left_index:right_index]
            changed = True
        elif left_index > 0:
            run.possible_starts = run.possible_starts[left_index:]
            changed = True
    return changed
                    
def index_of(list, f):
    return next((i for (i, v) in enumerate(list) if f(v)), -1)

def solve(clues, width, height):
    state = State(clues[0], clues[1])
    result = state.solve()
    return tuple(tuple(x) for x in result)
  
#################################################
from collections import deque

def is_done(field):
    for r in field:
        if 9 in r:
            return False
    return True


def get_cor(field, t):
    x, d = t
    if d:
        cor = [r[x] for r in field]
    else:
        cor = field[x]
    zeros = 0
    ones = 0
    for i, c in enumerate(cor):
        if c == 1:
            ones |= 1 << i
        elif c == 0:
            zeros |= 1 << i
    return cor, zeros, ones


def set_cor(field, t, i, v):
    x, d = t
    if d:
        field[i][x] = v
    else:
        field[x][i] = v


def get_pos(cor_t, clues, pos, cur_p=0, cur_zero=0, cur_one=0):
    cor, cor_zero, cor_one = cor_t
    left = len(cor) - cur_p
    if len(clues) == 0:
        if left < 0:
            left = 0
        if left > 0 and 1 in cor[-left:]:
            return
        for j in range(left):
            cur_zero |= 1 << cur_p + j
        pos.append((cur_zero, cur_one))
        return
    follower_set = sum(clues[1:])
    follower_len = follower_set + len(clues) - 1
    clue = clues[0]
    for i in range(left - follower_len - clue + 1):
        n_p = cur_p
        n_zero = cur_zero
        n_one = cur_one
        for j in range(i):
            n_zero |= 1 << (cur_p + j)
        n_p += i
        for j in range(clue):
            n_one |= 1 << (n_p + j)
        n_p += clue
        if len(clues) > 1:
            n_zero |= 1 << (cur_p + i + clue)
            n_p += 1
        if n_zero & cor_one or n_one & cor_zero:
            continue
        get_pos(cor_t, clues[1:], pos, n_p, n_zero, n_one)
    return


def filter_pos(field, pos, t, x):
    _, cor_zero, cor_one = get_cor(field, t)
    comp_zero = cor_zero & (1 << x)
    comp_one = cor_one & (1 << x)
    n_pos = [(zero, one) for zero, one in pos if zero & comp_zero or one & comp_one]
    return n_pos


def set_fields(field, pos, t):
    x, d = t
    cor, cor_zero, cor_one = get_cor(field, t)
    any_zero, any_one = 0, 0
    for p in pos:
        zero, one = p
        any_zero |= zero
        any_one |= one
    changed = []
    for i in range(len(cor)):
        if cor[i] != 9:
            continue
        zero = any_zero & (1 << i)
        one = any_one & (1 << i)
        if zero and not one:
            set_cor(field, t, i, 0)
            changed.append((i, not d, x))
        elif not zero and one:
            set_cor(field, t, i, 1)
            changed.append((i, not d, x))
        elif not zero and not one:
            raise Exception
    return changed


def solve_loop(field, a, start):
    check = deque(start)
    later = []
    while check:
        i, d, x = check.popleft()
        if (i, d) in a:
            pos = filter_pos(field, a[(i, d)], (i, d), x)
            new = set_fields(field, pos, (i, d))
            for n in new:
                check.append(n)
            a[(i, d)] = pos
        else:
            later.append((i, d, x))
    return later


def get_sort_order(t, field):
    i, d, cs = t
    cor, _, _ = get_cor(field, (i, d))
    known = len([x for x in cor if x != 9])
    return (len(cor) - sum(cs) - known) ** len(cs)


def solve_deq(field, deq, a):
    while deq:
        k = deq.popleft()
        i, d, x = k
        pos = filter_pos(field, a[(i, d)], (i, d), x)
        new = set_fields(field, pos, (i, d))
        for n in new:
            deq.append(n)
        a[(i, d)] = pos


def guess(field, a):
    to_check = sorted([k for k in a if len(a[k]) > 1], key=lambda x: len(a[x]))[0]
    for pa in a[to_check]:
        n_field = [x[:] for x in field]
        n_a = {k: a[k][:] for k in a}
        n_a[to_check] = [pa]
        new = set_fields(n_field, [pa], to_check)
        try:
            solve_loop(n_field, n_a, new)
        except:
            continue
        if is_done(n_field):
            return n_field
        res = guess(n_field, n_a)
        if res:
            return res


def solve(clues, width, height):
    field = [[9] * width for _ in range(height)]
    a = {}
    deq = deque()
    my_clues = []
    for d in [True, False]:
        for i, cs in enumerate(clues[not d]):
            my_clues.append((i, d, cs))
    my_clues.sort(key=lambda x: get_sort_order(x, field))
    while my_clues:
        i, d, cs = my_clues.pop(0)
        pos = []
        get_pos(get_cor(field, (i, d)), cs, pos)
        a[(i, d)] = pos
        new = set_fields(field, pos, (i, d))
        later = solve_loop(field, a, new)
        for n in later:
            deq.append(n)
        my_clues.sort(key=lambda x: get_sort_order(x, field))
    solve_deq(field, deq, a)

    if not is_done(field):
        field = guess(field, a)
    t = tuple([tuple(f) for f in field])
    return t
  
##################################################
# nonogram solver

#from nonodisplay import Nonodisplay 
#from dataclasses import dataclass
#from constants import WHITE, BLACK, KNOWN, UNKNOWN, KEEPCOLOR, dx, dy, UNCHANGED
from copy import deepcopy

WHITE = 0
BLACK = -1
KNOWN = -2
UNKNOWN = -3
KEEPCOLOR = -4
UNCHANGED = -5
dx = (1,0)
dy = (0,1)

#--------------------------------------------------------------------------------------------------------------------------

# lines = [{},{}] = for eeach direction dict with (lineNr: list of Clue)

# @dataclass
# class Block():
#     ID  : int
#     width    : int
#     complete : bool
#     clue : int
     
# @dataclass
# class Clue():
#     ID : int
#     blocks : list
#     pos0   : int    # todo min/max coordinates
#     pos1   : int
#     lineNr : int
#     direction: int

# @dataclass
# class Field():
#     color : int # BLACK, WHITE, UNKNOWN
#     block : list # [horizID, vertID] if known
#     clue  : list # [horizID, vertID] of clues which cover this field
 
 #---------------------------------------------------------
def fieldcode(f, direction):
    # fields can be:
    # unknown: (UNKNOWN = -3)
    # white (WHITE = 0), 
    # black and unassigned (KNOWN = -2) # todo change?
    # black and assigned (blockID)
    if f['color'] != BLACK: return f['color']
    if f['block'][direction] == None: return KNOWN
    return f['block'][direction]   

#---------------------------------------------------------

def fits(line, block, startpos):
    if not line[startpos-1] in [WHITE, UNKNOWN]: return False    # white or unknown before block
    for i in range(block['width']):
        if not (line[startpos + i] in [UNKNOWN, KNOWN, block['ID']]): return False  # unknown, unassigned black or assigned to block within range
    if not line[startpos + i+1] in [WHITE, UNKNOWN]: return False           # white or unknown after block
    return True

#---------------------------------------------------------
DPL = {}
def leftmost(line, clue, startpos, blocks):
    # clue here is list of blocks!
    
    if len(clue) == 0:
        # no more clues, are there unassigned fields left ?
        if any([f == KNOWN for f in line[startpos:]]): return None
        else: return {}
    
    #if (tuple(line),tuple(clue),startpos) in DPL: return DPL[tuple(line),tuple(clue),startpos]
    
    block = blocks[clue[0]]
    last = len(line) - sum([blocks[c]['width'] for c in clue]) - len(clue) 
    aux = min([i for i,e in enumerate(line[startpos:], startpos) if not e in [WHITE, UNKNOWN]], default = last)
    last = min(aux, last)
    
    # is block already present in line ?
    aux = max([i for i,e in enumerate(line[startpos:], startpos) if e == block['ID']], default = 0)
    first = max(startpos, aux - block['width'] + 1)

    for startpos in range(first,last+1):
        if fits(line, block, startpos):
            rest = leftmost(line, clue[1:], startpos + block['width'] + 1, blocks )
            if rest != None: 
                ret = { **{block['ID']: startpos}, **rest}
                DPL[tuple(line),tuple(clue),startpos] = ret
                return ret
    DPL[tuple(line),tuple(clue),startpos] = None            
    return None

#---------------------------------------------------------
DPR = {}
def rightmost(line, clue, startpos, blocks):
    # clue here is list of blocks!            
    if len(clue) == 0:
        # no more clues, are there unassigned fields left ?
        if any([f == KNOWN for f in line[:startpos+1]]): return None
        else: return {}
    
    #if (tuple(line),tuple(clue),startpos) in DPR: return DPR[tuple(line),tuple(clue),startpos]
    
    block = blocks[clue[-1]]
    last = sum([blocks[c]['width'] for c in clue]) + len(clue) - 1
    aux = max([i for i,e in enumerate(line[1:startpos+1]) if not e in [WHITE, UNKNOWN]], default = 0)
    last = max(aux, last)
    
    # is block already present in line ?
    aux = min([i for i,e in enumerate(line[:startpos]) if e == block['ID']], default = startpos)
    first = min(startpos, aux+block['width']-1)
    
    for startpos in range(first,last-1, -1):
        if fits(line, block, startpos - block['width'] + 1):
            rest = rightmost(line, clue[:-1], startpos - block['width'] - 1, blocks )
            if rest != None: 
                ret = { **{block['ID']: startpos}, **rest}
                DPR[tuple(line),tuple(clue),startpos] = ret
                return ret
    DPR[tuple(line),tuple(clue),startpos] = None         
    return None

def evalClue(clue, grid, blocks):
    
    #---------------------------------------------------------
        
    if clue['direction'] == 0:
        line = [fieldcode(grid[(x, clue['lineNr'])], clue['direction']) for x in range(clue['pos0']-1, clue['pos1']+2)] 
    else:
        line = [fieldcode(grid[(clue['lineNr'], y)], clue['direction']) for y in range(clue['pos0']-1, clue['pos1']+2)]

    ret =  [UNKNOWN]*len(line)
    
    left = {}
    right = {}
    
    left = leftmost(line, clue['blocks'], 1, blocks)
    if left == None: return None
    #left = {} if auxleft == None else auxleft
    
    # find rightmost pattern
    right = rightmost(line, clue['blocks'], len(line)-1, blocks) 
    if right == None: return None
    #right = {} if auxright == None else auxright
                
    # fill patterns        
    for block in clue['blocks']:           
        for i in range(right[block]-blocks[block]['width'] + 1, left[block]+blocks[block]['width']):
            ret[i] = block            

    left = sorted([ l for l in left.values() ] + [len(line)-1])
    right = sorted([0] + [r for r in right.values()])
    for l1,l2 in zip(right, left):
        for i in range(l1+1,l2): ret[i] = WHITE  
    ret = [ r if r != l else UNCHANGED for r,l in zip(ret, line) ]
    return ret

#--------------------------------------------------------------------------------------------------------------------------


def SetPoint(x, y, color, block, direction, grid, clues, blocks, cluequeue):
    
    global clueIdx
    
    old_color = grid[(x,y)]['color']
    
    # test for correctness if solution is known
    #checkSolution(x,y,color)
    #-----------------------------------------------------------
    
    # set new color value    
    if color != KEEPCOLOR: grid[(x,y)]['color'] = color
    
    # update block ID 
    if grid[(x,y)]['block'][direction] == None: grid[(x,y)]['block'][direction] = block    
    
    cluequeue.add(grid[(x,y)]['clue'][0])
    cluequeue.add(grid[(x,y)]['clue'][1])  # ? only one should be necessary
    
    # update block ID of/from direct neighbors
    if color == BLACK:

        for direction in [0,1]:
            # don't do anything if block is already completed
            block = grid[(x,y)]['block'][direction]
            if not (block and blocks[block]['complete']):
                
                # see if there are adjacent black fields             
                block = None
                minx = maxx = x
                miny = maxy = y
                while grid[(minx,miny)]['color'] == BLACK:
                    if grid[(minx,miny)]['block'][direction] : block = grid[(minx,miny)]['block'][direction]                    
                    minx -= dx[direction]
                    miny -= dy[direction]
                while grid[(maxx,maxy)]['color'] == BLACK:
                    if grid[(maxx,maxy)]['block'][direction] : block = grid[(maxx,maxy)]['block'][direction]
                    maxx += dx[direction]
                    maxy += dy[direction]
                    
                # shrink back to black fields
                minx += dx[direction]
                miny += dy[direction]
                maxx -= dx[direction]
                maxy -= dy[direction]
                    
                l = max(maxx-minx, maxy-miny) + 1
                if l > 1:   # fields found, set block ID
                    auxx = minx
                    auxy = miny
                    for _ in range(l):
                        grid[(auxx,auxy)]['block'][direction] = block 
                        auxx += dx[direction]
                        auxy += dy[direction]
                        
                # is block complete ?
                if block and l == blocks[block]['width']:    # block is complete
                    blocks[block]['complete'] = True
                    # set adjacent fields to white
                    SetPoint(minx - dx[direction], miny - dy[direction], WHITE, None, direction, grid, clues, blocks, cluequeue)
                    SetPoint(maxx + dx[direction], maxy + dy[direction], WHITE, None, direction, grid, clues, blocks, cluequeue)
                    # get neighboring blocks in clue and "reserve" next fields
                    c = clues[grid[(maxx, maxy)]['clue'][direction]]
                    idx = c['blocks'].index(block)
                    if idx>0:
                        for aux in range(1, blocks[c['blocks'][idx-1]]['width']+1):
                            SetPoint(minx - (aux+1) * dx[direction], miny - (aux+1) * dy[direction], KEEPCOLOR, c['blocks'][idx-1], direction, grid, clues, blocks, cluequeue)

                        if c['ID'] in cluequeue:
                            cluequeue.remove(c['ID'])
                        # split clue
                        global clueIdx
                        auxclue = {'ID':clueIdx,'blocks': c['blocks'][:idx],'pos0':c['pos0'],'pos1': (minx-2, miny-2)[direction] , 'lineNr':c['lineNr'], 'direction':c['direction']}
                        
                        if direction == 0: 
                            for x in range(c['pos0'],minx): grid[(x,miny)]['clue'][direction] = clueIdx
                        else: 
                            for y in range(c['pos0'],miny): grid[(minx,y)]['clue'][direction] = clueIdx
                        
                        for b in auxclue['blocks']: blocks[b]['clue'] = clueIdx
                        clues[clueIdx] = auxclue
                        
                        cluequeue.add(auxclue['ID'])
                            
                        clueIdx += 1
                        
                    if idx<len(c['blocks'])-1: 
                        for aux in range(1, blocks[c['blocks'][idx+1]]['width']+1):
                            SetPoint(maxx + (aux+1) * dx[direction], maxy + (aux+1) * dy[direction], KEEPCOLOR, c['blocks'][idx+1], direction, grid, clues, blocks, cluequeue)
                            
                        # split clue
                        auxclue = {'ID':clueIdx,'blocks': c['blocks'][idx+1:],'pos0': (maxx+2, maxy+2)[direction],'pos1': c['pos1'] ,'lineNr':c['lineNr'], 'direction':c['direction']}
                        
                        if direction == 0: 
                            for x in range(maxx+1,c['pos1']+1): grid[(x,miny)]['clue'][direction] = clueIdx
                        else: 
                            for y in range(maxy+1,c['pos1']+1): grid[(minx,y)]['clue'][direction] = clueIdx
                        
                        for b in auxclue['blocks']: blocks[b]['clue'] = clueIdx
                        clues[clueIdx] = auxclue
                        
                        cluequeue.add(auxclue['ID'])
                            
                        clueIdx += 1
                                        
    return


#-------------------------------------------------------------------------------------------

def solveGrid(grid, clues, blocks, cluequeue):
    
    while cluequeue:
        
        c = clues[cluequeue.pop()]
        direction = c['direction']

        points = evalClue(c, grid, blocks)
        
        if points == None: return None
        
        x,y = ( (c['pos0']-1, c['lineNr']), (c['lineNr'], c['pos0']-1))[direction]
            
        for i,p in enumerate(points):
            if p == WHITE:
                SetPoint(x + i*dx[direction], y + i*dy[direction], WHITE, None, direction, grid, clues, blocks, cluequeue) 
            elif p != UNCHANGED and p != UNKNOWN:
                aux = grid[(x + i*dx[direction], y + i*dy[direction])]
                if not( aux['color'] == BLACK and aux['block'][direction] == p):
                    SetPoint(x + i*dx[direction], y + i*dy[direction], BLACK, p, direction, grid, clues, blocks, cluequeue)
                    
        # end while cluequeue
        
    # completely solved ?
    solved = True
    for f in grid.values():
        if f['color'] == UNKNOWN:
            solved = False
            break
        
    if solved:
        # convert to output format
        ret = []
        for row in range(1, maxy-1):
            ret.append( tuple((0 if grid[(column, row)]['color'] == WHITE else 1 for column in range(1,maxx-1) )) )
        return(tuple(ret))
                
    # solution incomplete, start guessing
    
    # get unsolved block
    unsolved = [ (b['width'], b['ID']) for b in blocks.values() if b['complete'] == False]
    block = blocks[max(unsolved)[1]]
    #block = blocks[random.choice(unsolved)[1]]
    # for block in blocks.values():
    #     if not block['complete']: break
    clue = clues[block['clue']]
            
    # get possible block positions
    direction = clue['direction']
    if direction == 0:
        line = [fieldcode(grid[(x, clue['lineNr'])], direction) for x in range(clue['pos0']-1, clue['pos1']+2)] 
    else:
        line = [fieldcode(grid[(clue['lineNr'], y)], direction) for y in range(clue['pos0']-1, clue['pos1']+2)]
    right = rightmost(line, clue['blocks'], len(line)-1, blocks)
    if right == None: return None
    right = right[block['ID']] - block['width']+1
    
    left  = leftmost(line, clue['blocks'], 1, blocks)
    if left == None: return None
    left = left[block['ID']] 
    
    for pos in range(left, right+1):
        if fits(line, block, pos):
            # copy data
            newgrid = deepcopy(grid)
            newclues = deepcopy(clues)
            newblocks = deepcopy(blocks)
            cluequeue.clear()
            cluequeue.add(clue['ID'])
            # put block and add clues
            x,y = ( (clue['pos0']-1, clue['lineNr']), (clue['lineNr'], clue['pos0']-1))[direction]
            newblocks[block['ID']]['complete'] = True
            for i in range(block['width']):
                newgrid[(x + (pos+i)*dx[direction], y + (pos+i)*dy[direction])]['color'] = BLACK
                newgrid[(x + (pos+i)*dx[direction], y + (pos+i)*dy[direction])]['block'][direction] = block['ID']
                # if evalClue(clues[newgrid[(x + i*dx[direction], y + i*dy[direction])]['clue'][1-direction]], newgrid, newblocks) == None:
                #     continue
                cluequeue.add(newgrid[(x + i*dx[direction], y + i*dy[direction])]['clue'][1-direction])
            
            ret = solveGrid(newgrid, newclues, newblocks, cluequeue)
            #ret = True
            if ret == None: continue
            else: return ret
            
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

def solve(clues,h,w):
# main solver starts here
    
    #print(clues)
    DPR = {}
    DPL = {}
    global clueIdx
    #global nd
                

    #global Mysolution
    #aux = tuple(0 for _ in range(len(Mysolution[0])+2))
    #Mysolution =  (aux,) + tuple( (0,) + l + (0,) for l in Mysolution ) + (aux,)

    framedclues = ( ((),) + clues[1] + ((),), ((),) + clues[0] + ((),)) # column/row swap because grid is printed that way

    # store individual blocks (ID, length, completed flag) in dict
    # build data structure for clues (ID, width, list of blocks)
    # build data structure for lines/columns: (Nr, list of clues)
    # add frame of zeros
    blocks = {}
    clues = {}
    lines = [{},{}]
    blockIdx = 1
    clueIdx = 1

    # create block and clue objects
    for direction in [0,1]:      # horizontal (+) and vertical (-)
        width = len(framedclues[1-direction])
        for lineNr, clue in enumerate(framedclues[direction]):    # for each clue (= each line)
            
            auxBlockList = []
            for blockNr, w in enumerate(clue):          # go through entries in clue
                auxBlock = {'ID':blockIdx,'width': w, 'complete':False, 'clue':clueIdx}    # build block objects     

                blocks[blockIdx] = auxBlock
                blockIdx += 1
                auxBlockList.append(auxBlock['ID'])
            
            auxClue = { 'ID':clueIdx, 'blocks':auxBlockList,'pos0': 1, 'pos1':width-2,'lineNr': lineNr,'direction': direction }    # build clue object   # todo min/max coordinates?
            clues[clueIdx] = auxClue
            clueIdx += 1            
            lines[direction][lineNr] = [auxClue]            # attach to clue list for line        

    
    # set up grid
    gridX = len(framedclues[1])
    gridY = len(framedclues[0])
    grid = { (x,y): {'color':UNKNOWN,'block':[None, None],'clue':[lines[0][y][0]['ID'], lines[1][x][0]['ID']]} for y in range(gridY) for x in range(gridX) }
            
    #-------------------------------------------------------------------------------------------        
    
    # start solving
    cluequeue = set()
    global maxy
    global maxx
    
    maxx = len(lines[1])
    maxy = len(lines[0])

    # set border of zeros
    for y in range(maxy):
        grid[(0,y)]['color'] = WHITE
        grid[(maxx-1,y)]['color'] = WHITE
    for x in range(maxx):
        grid[(x,0)]['color'] = WHITE
        grid[(x,maxy-1)]['color'] = WHITE
    
    # add all clues to queue
    for c in clues.values(): cluequeue.add(c['ID'])
    
    ret = solveGrid(grid, clues, blocks, cluequeue)
        
    return ret
