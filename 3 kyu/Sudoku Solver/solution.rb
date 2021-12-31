class SudokuSolver
  def initialize(sudoku)
    @sudoku = sudoku.map.with_index do |line, row|
      line.map.with_index do |cell, col|
        {
          row: row,
          col: col,
          number: cell,
          candidates: []
        }
      end
    end

    @sudoku.each do |row|
      row.each do |cell|
        if cell[:number] == 0
          cell[:candidates] = (1..9).to_a.reject do |number|
            numbers_in_same_row_col_or_group(cell).include?(number)
          end
        end
      end
    end
  end

  def solve
    marked_at_least_one = true

    while marked_at_least_one
      marked_at_least_one = false

      @sudoku.each do |line|
        line.each do |cell|
          if cell[:candidates].length == 1
            cell[:number] = cell[:candidates].first

            cells_in_same_row_col_or_group(cell).each do |another_cell|
              another_cell[:candidates].delete(cell[:number])
            end

            marked_at_least_one = true
          end
        end
      end
    end

    serialize(@sudoku)
  end

  private

  def numbers_in_same_row_col_or_group(cell)
    cells_in_same_row_col_or_group(cell).map { |c| c[:number] }.reject { |n| n == 0 }.sort.uniq
  end

  def cells_in_same_row_col_or_group(cell)
    cells =
      cells_in_same_row(cell) +
      cells_in_same_col(cell) +
      cells_in_same_group(cell)

    cells.uniq { |c| [c[:row], c[:col]] }
  end

  def cells_in_same_row(cell)
    9.times.map do |col|
      @sudoku[cell[:row]][col]
    end
  end

  def cells_in_same_col(cell)
    9.times.map do |row|
      @sudoku[row][cell[:col]]
    end
  end

  def cells_in_same_group(cell)
    3.times.flat_map do |drow|
      3.times.map do |dcol|
        @sudoku[cell[:row] / 3 * 3 + drow][cell[:col] / 3 * 3 + dcol]
      end
    end
  end

  def serialize(sudoku)
    @sudoku.map do |row|
      row.map do |cell|
        cell[:number]
      end
    end
  end
end

def sudoku(sudoku)
  sudoku_solver = SudokuSolver.new(sudoku)
  sudoku_solver.solve
end

___________________________________________________

class SudokuSolver
  attr_reader :puzzle

  def initialize(puzzle)
    @puzzle = puzzle

    @possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9].freeze

    @relevant_3x3_subblock_positions = [
      [1, 1],
      [1, 4],
      [1, 7],
      [4, 1],
      [4, 4],
      [4, 7],
      [7, 1],
      [7, 4],
      [7, 7],
    ].freeze
  end

  def solve
    backtracking_search(puzzle)
  end

  private

  def backtracking_search(assignments)
    unassigned_field = first_unassigned_field(assignments)
    return assignments if unassigned_field == nil

    @possible_values.each do |value|
      local_assignments = assignments.map(&:dup)
      local_assignments[unassigned_field[0]][unassigned_field[1]] = value

      next unless consistent(local_assignments)

      result = backtracking_search(local_assignments)
      return result if result
    end

    nil
  end

  def first_unassigned_field(assignments)
    (0...9).each do |row|
      (0...9).each do |col|
        return [row, col] if assignments[row][col] == 0
      end
    end

    nil
  end

  def consistent(assignments)
    return false unless constraint_row_uniqueness(assignments)
    return false unless constraint_col_uniqueness(assignments)
    return false unless constraint_3x3_uniqueness(assignments)

    true
  end

  def constraint_row_uniqueness(assignments)
    (0...9).each do |row|
      row_values = []

      (0...9).each do |col|
        next if assignments[row][col] == 0

        return false if row_values.include?(assignments[row][col])

        row_values << assignments[row][col]
      end
    end

    true
  end

  def constraint_col_uniqueness(assignments)
    cols = {}

    (0...9).each do |row|
      (0...9).each do |col|
        next if assignments[row][col] == 0

        cols[col] = [] unless cols.key?(col)

        return false if cols[col].include?(assignments[row][col])

        cols[col] << assignments[row][col]
      end
    end

    true
  end

  def constraint_3x3_uniqueness(assignments)
    values = []

    @relevant_3x3_subblock_positions.each do |pos|
      row = pos[0]
      col = pos[1]

      value = assignments[row][col]
      next if value.nil? || value == 0

      values.clear
      values << value

      (-1..1).each do |r|
        new_row = row + r

        (-1..1).each do |c|
          next if r == 0 && c == 0

          new_col = col + c

          next if new_row < 0 || new_row > 8 || new_col < 0 || new_col > 8

          surr_value = assignments[new_row][new_col]
          next if surr_value.nil? || surr_value == 0

          return false if values.include?(surr_value)

          values << surr_value
        end
      end
    end

    true
  end
end

def sudoku(puzzle)
  SudokuSolver.new(puzzle).solve
end

___________________________________________________


def is_possible(board,row,col,rows_arr,cols_arr,squares) 

    if rows_arr[col][board[row][col]-1]==1 

        return false

    end

    if cols_arr[row][board[row][col]-1]==1 

        return false

    end

    if squares[row/3*3+col/3][board[row][col]-1]==1 

        return false

    end

    return true

end

def rec(board,row,col,rows_arr,cols_arr,squares) 

    cor=false

    if col==9 

        row+=1

        col=0

    end

    if row==9 

        return true

    end

    if board[row][col]==0 

        for i in (1..9) 

            board[row][col]=i

            if is_possible(board,row,col,rows_arr,cols_arr,squares) 

                rows_arr[col][i-1]=1

                cols_arr[row][i-1]=1

                squares[row/3*3+col/3][board[row][col]-1]=1

                cor=rec(board,row,col+1,rows_arr,cols_arr,squares)

                rows_arr[col][i-1]=0

                cols_arr[row][i-1]=0

                squares[row/3*3+col/3][board[row][col]-1]=0

            end

            if cor==true 

                break

            end

        end

        if cor==false 

            board[row][col]=0

        end

    else

        while board[row][col]!=0 

            col+=1

            row+=col/9

            col%=9

            if row==9 

                break

            end

        end

        cor=rec(board,row,col,rows_arr,cols_arr,squares)

    end

    return cor

end

def sudoku(board) 

    rows=[]

    cols=[]

    squares=[]

    for i in (0..8) 

        arr=[0]*9

        arr2=[0]*9

        arr3=[0]*9

        for r in (0..8) 

            if board[i][r]!=0 

                arr[board[i][r]-1]=1

            end

            if board[r][i]!=0 

                arr2[board[r][i]-1]=1

            end

        end

        cols.push(arr.clone())

        rows.push(arr2.clone())

    end

    i=0

    r=0

    j=2

    k=2

    while j<=8 

        k=2

        while k<=8 

            i=j-2

            arr3=[0]*9

            while i<=j 

                r=k-2

                while r<=k 

                    if board[i][r]!=0 

                        arr3[board[i][r]-1]=1

                    end

                    r+=1

                end

                i+=1

            end

            squares.push(arr3.clone())

            k+=3

        end

        j+=3

    end

    rec(board,0,0,rows,cols,squares)

    return board

end

___________________________________________________
def sudoku(puzzle)

  output(puzzle)

  aviables = get_all_aviables(puzzle)

  fill_board(puzzle, aviables)

  puzzle
  
end

def fill_board(puzzle, aviables)
 
  return puzzle if aviables.join.length == 0

  (1..9).each do |level|
    puzzle.each_index do |i|
      puzzle[i].each_index do |j|
        if puzzle[i][j] == 0 and aviables[i][j] and aviables[i][j].length == level

          puzzle[i][j] = aviables[i][j][0]
          aviables = get_all_aviables(puzzle)

          fill_board(puzzle, aviables)

        end
      end
    end
  end
end

def get_aviable_numbers(puzzle, i, j)

  row = puzzle[i].reject {|e| e == 0}
  col = get_col(puzzle, j).reject{|e| e == 0}
  square = get_square(puzzle, i, j).reject{|e| e == 0}

  array = (row + col + square).uniq.sort
  aviables = []
  (1..9).each do |i|
    aviables << i if not array.index(i)
  end

  return nil if aviables.length == 0
  aviables

end

def get_all_aviables(puzzle)

  a = Array.new(9) {Array.new(9)}

  puzzle.each_index do |i|
    puzzle[i].each_index do |j|

      if puzzle[i][j] > 0        
        a[i][j] = nil
      else
        a[i][j] = get_aviable_numbers(puzzle, i, j)
      end

    end

  end

  a

end

def get_square(puzzle, i, j)
  start_i = i - i % 3
  start_j = j - j % 3

  array = []

  for r in start_i..(start_i + 2) do
    for c in start_j..(start_j + 2) do
      array << puzzle[r][c]
    end
  end
  array
end

def get_col(puzzle, j)
  array = []
  0.upto(8) {|i|  array << puzzle[i][j]}
  array
end

___________________________________________________


def square(puzzle, row, col)
  hor = row / 3
  vert = col / 3
  result = []
  ((hor * 3)..(hor * 3 + 2)).each do |row|
    ((vert * 3)..(vert * 3 + 2)).each do |col|
      result << puzzle[row][col]
    end
  end
  result
end

def sudoku(puzzle)
  while puzzle.flatten.include?(0)
    (0..8).to_a.each do |row|
      (0..8).to_a.each do |column|
        next if puzzle[row][column] > 0 
        available = (1..9).to_a
        available = available - puzzle[row]
        available = available - puzzle.map{|r| r[column]}
        available = available - square(puzzle, row, column)
        puzzle[row][column] = available.first if available.length == 1
      end
    end
  end
  puzzle
end
