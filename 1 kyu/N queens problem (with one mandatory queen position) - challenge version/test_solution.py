import codewars_test as test
import random


def check_solution_valid(solution, required, size):
    def parse_solution(solution, size):
        expected_length = size * (size + 1)
        
        if type(solution) != str:
            raise ValueError('Solution is not a string')
        if len(solution) != expected_length:
            raise ValueError(f'Length of returned board is {len(solution)}, but should be {expected_length}\n')
        
        qs = []
        lines = solution[:-1].split('\n')
        
        if len(lines) != size:
            raise ValueError('Invalid number of rows')
        
        for i in range(len(lines)):
            line = lines[i]
            
            if len(line) != size:
                raise ValueError(f'Line {i} has invalid length of {len(line)}')
            
            qc = line.count('Q')
            ec = line.count('.')
            
            if qc + ec != size:
                raise ValueError(f'Invalid caharacter found in row {i}')
            if qc == 0:
                raise ValueError(f'No queen found at row {i}')
            if qc != 1:
                raise ValueError(f'More than one queen found in row {i}')
            
            qs.append(line.index('Q'))
        return qs
    qs = []
    try:
        qs = parse_solution(solution, size)
        req_row = required[0]
        req_col = required[1]
        if qs[req_row] != req_col:
            raise ValueError('Queen not found in required position')
        
        for row in range(len(qs)):
            col = qs[row]
            if col < 0 or col >= size:
                raise ValueError(f'({row},{col}) is now a valid position for a board of size {size}')
        
        cols = [True for _ in range(size)]
        lds = [True for _ in range(size * 2 - 1)]
        rds = [True for _ in range(size * 2 - 1)]
        ldid = lambda row, col: size + col - row - 1
        rdid = lambda row, col: col + row 
        
        for row in range(size):
            col = qs[row]
            atk = not (cols[col] and lds[ldid(row, col)] and rds[rdid(row, col)])
            
            if atk:
                raise ValueError(f'Queen ({row}, {col}) can be attacked')
            
            cols[col] = False
            lds[ldid(row, col)] = False
            rds[rdid(row, col)] = False
            
    except ValueError as e:
        test.fail(str(e))
    test.pass_()
        

@test.describe("N Queens Test")
def test_group():
    
    def test_solution(size, fixed):
        @test.it(f'Testing size={size}, fixed={fixed}')
        def test_it():
            solution = solve_n_queens(size, fixed)
            check_solution_valid(solution, fixed, size)
            
    def test_random_in_range(min, max):
        size = random.randint(min, max)
        fixed = (random.randint(0, size-1), random.randint(0, size-1))
        test_solution(size, fixed)
        
    @test.describe("Basic Tests")
    def test_basic():
        test_cases = [
            {'size': 1, 'fixed': (0, 0), 'solution': 'Q\n'},
            {'size': 4, 'fixed': (0, 2), 'solution': '..Q.\nQ...\n...Q\n.Q..\n'},
            {'size': 6, 'fixed': (1, 2), 'solution': '....Q.\n..Q...\nQ.....\n.....Q\n...Q..\n.Q....\n'},
        ]
        for test_case in test_cases:
            size = test_case['size']
            fixed = test_case['fixed']
            solution = test_case['solution']
            
            @test.it(f'Testing size={size}, fixed=({fixed})')
            def test_it():
                test.assert_equals(solve_n_queens(size, fixed), solution)
                
    @test.describe('No Solution')
    def test_no_solution():
        test_cases = [
            [2, (0, 0)],
            [3, (0, 2)],
            [6, (2, 3)]
        ]
        
        for test_case in test_cases:
            size = test_case[0]
            fixed = test_case[1]
            
            @test.it(f'Testing size={size}, fixed={fixed}')
            def test_it():
                test.assert_equals(solve_n_queens(size, fixed), None)
    
    @test.describe('Test Tiny Boards')
    def test_tiny_boards():
        no_solution_cases = [
            [2, (0, 0)],[2, (0, 1)],[2, (1, 0)],[2, (1, 1)],

            [3, (0, 0)],[3, (0, 1)],[3, (0, 2)],[3, (1, 0)],
            [3, (1, 1)],[3, (1, 2)],[3, (2, 0)],[3, (2, 1)],
            [3, (2, 2)],
            
            [4, (0, 0)],[4, (0, 3)],[4, (1, 1)],[4, (1, 2)],
            [4, (2, 1)],[4, (2, 2)],[4, (3, 0)],[4, (3, 3)],
            
            [6, (0, 0)],[6, (0, 5)],[6, (1, 1)],[6, (1, 4)],
            [6, (2, 2)],[6, (2, 3)],[6, (3, 2)],[6, (3, 3)],
            [6, (4, 1)],[6, (4, 4)],[6, (5, 0)],[6, (5, 5)],
        ]
        
        NO_SOLUTIONS_4 = {(0, 0), (0, 3), (1, 1), (1, 2), (2, 1), (3, 0), (3, 3)}
        NO_SOLUTIONS_6 = {(0, 0), (0, 5), (1, 1), (1, 4), (2, 2), (2, 3), (3, 2), (3, 3), (4, 1), (4, 4), (5, 0), (5, 5)}
        
        specs = list('-+' * 5)
        random.shuffle(specs)
        for spec in specs:
            if spec == '-':
                random_case = no_solution_cases[random.randint(0, len(no_solution_cases) - 1)]
                size = random_case[0]
                fixed = random_case[1]
                @test.it(f'Testing size={size}, fixed={fixed}')
                def test_it():
                    test.assert_equals(solve_n_queens(size, fixed), None)
            else:
                size = 0
                fixed = (0, 0)
                case_ready = False
                while not case_ready:
                    size = random.randint(0, 6) + 4
                    fixed = (random.randint(0, size - 1), random.randint(0, size - 1))
                    if size == 4 and fixed in NO_SOLUTIONS_4:
                        continue
                    if size == 6 and fixed in NO_SOLUTIONS_6:
                        continue
                    case_ready = True
                test_solution(size, fixed)
                
    @test.describe('Test N from 10 to 50')
    def test_small():
        test_random_in_range(10, 15)
        test_random_in_range(15, 20)
        test_random_in_range(20, 25)
        test_random_in_range(25, 35)
        test_random_in_range(45, 50)
        
    @test.describe('Test N from 100 to 500')
    def test_medium():
        test_random_in_range(100, 150)
        test_random_in_range(200, 250)
        test_random_in_range(300, 350)
        test_random_in_range(400, 450)
        test_random_in_range(450, 500)
        
    @test.describe('Test N from 500 to 1000')
    def test_large():
        test_random_in_range(500, 600)
        test_random_in_range(650, 700)
        test_random_in_range(750, 800)
        test_random_in_range(850, 900)
        test_random_in_range(950, 1000)
