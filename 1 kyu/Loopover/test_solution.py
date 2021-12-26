from random import randint

def copy(a):
    return [r[:] for r in a]

def board_to_string(board):
    return '\n'.join(''.join(row) for row in board)

def print_info(start, end):
    print(f'Testing for:\n{board_to_string(start)}\n\nto turn into:\n{board_to_string(end)}\n')

def check(start, end, moves):
    if not isinstance(moves, list):
        print('A list of moves is expected')
        return False
    def shift(a, k):
        return a[k:] + a[0:k]
    def left_right(r, k):
        start[r] = shift(start[r], k)
    def up_down(c, k):
        col = shift([r[c] for r in start], k)
        for i, r in enumerate(start):
            r[c] = col[i]
    for move in moves:
        try:
            i = int(move[1:])
            if i < 0: raise 'Invalid move'
            if move[0] == 'L': left_right(i, 1)
            elif move[0] == 'R': left_right(i, -1)
            elif move[0] == 'U': up_down(i, 1)
            elif move[0] == 'D': up_down(i, -1)
            else: raise 'Invalid move'
        except:
            print(f'Invalid move: {move}')
            return False
    if start != end:
        print(f'You failed! Your moves got to:\n{board_to_string(start)}')
        return False
    return True

def run_test(start, end, unsolvable):
    print_info(copy(start), copy(end))
    moves = loopover(copy(start), copy(end))
    if unsolvable:
        test.assert_equals(moves, None, 'Unsolvable configuration')
    else:
        test.assert_equals(check(start, end, moves), True)

@test.describe('Basic tests')
def basic_tests():
    def string_to_board(str):
        return [list(row) for row in str.split('\n')]

    @test.it('Test 2x2 (1)')
    def test_2x2_1():
        run_test(string_to_board('12\n34'),
                 string_to_board('12\n34'),
                 False)

    @test.it('Test 2x2 (2)')
    def test_2x2_1():
        run_test(string_to_board('42\n31'),
                 string_to_board('12\n34'),
                 False)

    @test.it('Test 4x5 (1)')
    def test_4x5_1():
        run_test(string_to_board('ACDBE\nFGHIJ\nKLMNO\nPQRST'),
                 string_to_board('ABCDE\nFGHIJ\nKLMNO\nPQRST'),
                 False)

    @test.it('Test 5x5 (1)')
    def test_5x5_1():
        run_test(string_to_board('ACDBE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'),
                 string_to_board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'),
                 False)
    
    @test.it('Test 5x5 (2)')
    def test_5x5_2():
        run_test(string_to_board('ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY'),
                 string_to_board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'),
                 False)
    
    @test.it('Test 5x5 (3)')
    def test_5x5_3():
        run_test(string_to_board('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI'),
                 string_to_board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'),
                 False)
                 
    @test.it('Test 5x5 (unsolvable)')
    def test_5x5_4():
        run_test(string_to_board('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI'),
                 string_to_board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'),
                 True)

    @test.it('Test 6x6')
    def test_6x6():
        run_test(string_to_board('WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789'),
                 string_to_board('ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789'),
                 False)


@test.describe('Random tests')
def random_tests():
    def copy(a):
        return [r[:] for r in a]
    def check(start, end, moves):
        if not isinstance(moves, list):
            print('A list of moves is expected')
            return False
        def shift(a, k):
            return a[k:] + a[0:k]
        def left_right(r, k):
            start[r] = shift(start[r], k)
        def up_down(c, k):
            col = shift([r[c] for r in start], k)
            for i, r in enumerate(start):
                r[c] = col[i]
        for move in moves:
            try:
                i = int(move[1:])
                if i < 0: raise 'Invalid move'
                if move[0] == 'L': left_right(i, 1)
                elif move[0] == 'R': left_right(i, -1)
                elif move[0] == 'U': up_down(i, 1)
                elif move[0] == 'D': up_down(i, -1)
                else: raise 'Invalid move'
            except:
                print(f'Invalid move: {move}')
                return False
        if start != end:
            print(f'You failed! Your moves got to:\n{board_to_string(start)}')
            return False
        return True
    def run_test(start, end, unsolvable):
        print_info(copy(start), copy(end))
        moves = loopover(copy(start), copy(end))
        if unsolvable:
            test.assert_equals(moves, None, 'Unsolvable configuration')
        else:
            test.assert_equals(check(start, end, moves), True)
            
    def generate(m, n, unsolvable=False):
        symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789αβγδεζηθλμνξπρσφχψω'
        if m * n > len(symbols):
            raise Exception('The grid is too large')
        chars = symbols[:m * n]
        scrambled = list(chars)
        sign = 1
        for i in range(len(scrambled) - 1, 0, -1):
            j = randint(0, i)
            if i != j:
                t = scrambled[i]
                scrambled[i] = scrambled[j]
                scrambled[j] = t
                sign = -sign
        if m * n % 2 and unsolvable == (sign > 0):
            t = scrambled[0]
            scrambled[0] = scrambled[1]
            scrambled[1] = t
        start = [scrambled[i:i + n] for i in range(0, m * n, n)]
        end = [list(chars[i:i + n]) for i in range(0, m * n, n)]
        return (start, end)
        
    k = 100
    unsolvables = k // 10
    for _ in range(k):
        sq = randint(0, 3) == 0
        m = randint(2, 9)
        n = m if sq else randint(2, 9)
        unsolvable = False
        if m * n % 2 and randint(0, 2) == 0 and unsolvables > 0:
            unsolvables -= 1
            unsolvable = True
        start, end = generate(m, n, unsolvable)
        @test.it(f'Testing {m} x {n}' + (' (unsolvable)' if unsolvable else ''))
        def test0():
            run_test(start, end, unsolvable)
            
