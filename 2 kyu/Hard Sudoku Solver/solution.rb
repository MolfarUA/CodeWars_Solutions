5588bd9f28dbb06f43000085


class SudokuDLX
  def initialize(puzzle)
    setup_board
    @solutions = []
    fill_puzzle(puzzle)
  end

  def solve(n=0)
    return true if (column = min_column).nil?
    column.cover
    column.traverse :down do |row|
      @solutions[n] = row
      row.traverse :right do |node|
        node.column.cover
      end
      return true if solve(n + 1)
      row.traverse :right do |node|
        node.column.uncover
      end
    end

    column.uncover
  end

  def solution
    raise RuntimeError if @solutions.size != 81
    result = []
    @solutions.each do |node|
      r = [node.column.label]
      node.traverse :right do |n|
        r << n.column.label
      end
      result << r
    end
    ans = [[],[],[],[],[],[],[],[],[]]
    result.each do |pos|
      pos.sort!
      row = (pos[0] - 1) / 9
      col = (pos[0] - 1) % 9
      ans[row][col] = pos[1] - 81 - row * 9
    end
    ans
  end

  private

  def min_column
    return nil if @root.right == @root
    column = @root.right
    min = column.size
    @root.traverse :right do |tmp|
      column, min = tmp, tmp.size if tmp.size <= min
    end
    column
  end

  def add_row(rows)
    nodes = rows.map do |row|
      new_node = nil
      @root.traverse :right do |node|
        new_node = node.add_node if node.column.label == row
      end
      new_node
    end
    # binding.pry if rows.max == 323
    nodes.each_with_index do |node, index|
      node.left = nodes[index - 1]
      node.right = nodes[(index + 1)% rows.size]
    end
  end

  def fill_puzzle(puzzle)
    9.times do |row|
      9.times do |col|
        1.upto(9) do |digit|
          box = (row / 3) * 3 + col / 3
          rows = [row * 9 + col + 1]
          rows << 81 + row * 9 + digit
          rows << 2 * 81 + col * 9 + digit
          rows << 3 * 81 + box * 9 + digit
          add_row(rows) if puzzle[row][col] == digit || puzzle[row][col].zero?
        end
      end
    end
  end

  def setup_board
    @root = Column.new(0)
    old_col = @root
    new_col = nil
    1.upto(324) do |i|
      new_col = Column.new(i)
      old_col.right = new_col
      new_col.left = old_col
      old_col = new_col
    end
    new_col.right = @root
    @root.left = new_col
  end

  class Node
    attr_accessor :column, :up, :down, :left, :right
    def initialize(column)
      @left = @right = @up = @down = self
      @column = column
    end

    def traverse(direction)
      node = self
      while (node = node.send(direction)) != self
        yield node
      end
    end

    def cover
      up.down, down.up = down, up
      column.size -= 1
    end

    def uncover
      up.down, down.up = self, self
      column.size += 1
    end
  end

  class Column < Node
    attr_accessor :label, :size
    def initialize(label)
      @label = label
      @size = 0
      super(self)
    end

    def add_node
      bottom = self.up
      bottom.down = Node.new(self)
      bottom.down.up = bottom
      bottom.down.down = self
      self.up = bottom.down
      @size += 1
      bottom.down
    end

    def cover
      left.right, right.left = right, left
      traverse :down do |row|
        row.traverse :right do |node|
          node.cover
        end
      end
    end

    def uncover
      left.right, right.left = self, self
      traverse :down do |row|
        row.traverse :right do |node|
          node.uncover
        end
      end
    end
  end
end

def sudoku_solver(puzzle)
  list = puzzle.flatten
  _puzzle = puzzle.flatten
  _puzzle.delete(0)
  raise RuntimeError if _puzzle.size < 17
  raise RuntimeError if (list.uniq - (0..9).uniq).any? || list.size != 81 || puzzle.map(&:size).uniq != [9]

  solver = SudokuDLX.new(puzzle)
  solver.solve
  solver.solution
end

_______________________________________________
class Cell < Struct.new(:num, :neighbors)
  ALL = (1..9).to_set.freeze

  def initialize(*args)
    super
    self.neighbors = []
  end

  def add_row(row)
    values = row.map(&:num).reject { |v| v == 0 } 
    raise ArgumentError if values != values.uniq
    self.neighbors.concat(row)
  end

  def solved?
    num > 0
  end

  def possible_values
    ALL - neighbors.map(&:num)
  end

  def inspect
    num.to_s
  end
end

class Board
  class Unsolvable < StandardError; end
  
  def initialize(puzzle)
    @puzzle = parse(puzzle)

    @puzzle.each(&method(:create_row))
    @puzzle.transpose.each(&method(:create_row))

    @puzzle.each_slice(3).map(&:transpose).flatten.each_slice(9) do |cells|
      create_row(cells)
    end
  end
  
  def solve(unsolved = @cells.reject(&:solved?))
#     puts @puzzle.inspect  
    @solution = nil
    find_solution(unsolved)
#     puts @solutions.size.inspect
    @solution
  end

  def find_solution(unsolved)
    all_solved = []
    while unsolved.any?
      solved = 0
      unsolved = unsolved.reject do |cell|
        values = cell.possible_values
        if values.size == 1
          solved += 1
          cell.num = values.first
          all_solved << cell
          true
        elsif values.size == 0
          raise Unsolvable
        end
      end
      
      return brute_force(unsolved) if solved == 0 # Can't solve any rows, time to brute force
    end
    
    raise Unsolvable if @solution
    @solution = self.to_a
  rescue Unsolvable
    all_solved.each { |cell| cell.num = 0 }
    raise
  end
  
  def brute_force(unsolved)
    idx = (@idx = (@idx || 0) + 1)
    cell, *unsolved = unsolved
    cell.possible_values.each do |v|
      cell.num = v
      find_solution(unsolved)
    rescue Unsolvable
      cell.num = 0
    end
    
    raise Unsolvable unless @solution
  end

  def parse(puzzle)
    @cells = []
    raise Unsolvable if puzzle.size != 9
    puzzle.map do |row|
      raise Unsolvable if row.size != 9
      row.map do |cell|
        Cell.new(cell).tap { |cell| @cells << cell }
      end
    end
  end

  def create_row(cells)
    cells.each { |cell| cell.add_row(cells) }
  end

  def to_a
    @puzzle.map { |row| row.map(&:num) }
  end
end

def sudoku_solver(puzzle)
  Board.new(puzzle).solve.to_a
end
_______________________________________________
def sudoku_solver(puzzle)
  raise "Not 9 rows" if (puzzle.size != 9)
  raise "Not 9 columns" if (puzzle.collect { |puzzle_row| puzzle_row.size }.uniq != [9])
  raise "Only 1 to 9 allowed" if (!(puzzle.flatten.uniq - (0..9).to_a).empty?)

  def cell_key(row, column, value)
    row.to_s + "," +  column.to_s + "," + value.to_s
  end

  square_sudoku_putty = {}

  (0..8).each { |row|
    (0..8).each { |column|
      (1..9).each { |cell_value|
        putty = Array.new(324, 0)
        putty[row * 9 + column] = 1
        putty[81 + row * 9 + cell_value - 1] = 1
        putty[162 + column * 9 + cell_value - 1] = 1
        putty[243 + ((row/3 * 3) + column/3)*9 + cell_value - 1] = 1
        square_sudoku_putty[cell_key(row, column, cell_value)] = putty
      }
    }
  } 
  chosen_cells = []
  (0..8).each { |row|
    (0..8).each { |column|
      cell_value = puzzle[row][column]
      if (cell_value != 0)
        chosen_cells.push(cell_key(row, column, cell_value))
      end
    }
  }
  
  solved_puzzle_cells = solver(square_sudoku_putty, chosen_cells) 
  raise "Puzzle could not be solved" if (solved_puzzle_cells == nil)
  solved_puzzle = Array.new(9){Array.new(9)}
  solved_puzzle_cells.each { |cell_key|
    cell = cell_key.split(",")
    solved_puzzle[cell[0].to_i][cell[1].to_i] = cell[2].to_i
  } 
  solved_puzzle
end

def solver(cell_putty, chosen_cells)
  putty_coverage = Array.new(cell_putty.values.first.size, 0)
  if (!chosen_cells.empty?)
    chosen_cell_putty = chosen_cells.collect { |cell| cell_putty[cell] }
    chosen_cell_putty.delete(nil)
    putty_coverage = chosen_cell_putty.transpose.map { |value| value.reduce(:+)}
  end 
  return chosen_cells if (putty_coverage.index(0) == nil)
  
  satisfied_putty = putty_coverage.each_index.select{|i| putty_coverage[i] == 1}
  filtered_cell_putty = cell_putty.select { |key, value|
    !satisfied_putty.collect{|i| value[i] == 1}.include?(true) }
  filtered_cell_putty.each { |key, value|
    putty = value.clone()
    satisfied_putty.reverse.each { |i| putty.delete_at(i) }
    filtered_cell_putty[key] = putty    
  }
  putty_cell_possibilities = filtered_cell_putty.values.transpose.map { |value| value.reduce(:+)}
  min_putty_cell_possibilities = putty_cell_possibilities.min
  return nil if (min_putty_cell_possibilities == 0)
  
  putty_index = putty_cell_possibilities.index(min_putty_cell_possibilities)
  cell_choices = filtered_cell_putty.find_all { |key, value| 
    value[putty_index] == 1}.collect { |value| value[0] }
  cell = cell_choices.sample
  chosen_cells_with_guess = chosen_cells.clone()
  chosen_cells_with_guess.push(cell)
  res = solver(filtered_cell_putty, chosen_cells_with_guess)
  
  tried_cells = Array.new
  while (res == nil)
    tried_cells.push(cell)
    chosen_cells_with_guess.pop()
    filtered_cell_putty.delete(cell)
    cell = (cell_choices - tried_cells).sample
    return nil if (cell == nil)
    chosen_cells_with_guess.push(cell)
    res = solver(filtered_cell_putty, chosen_cells_with_guess)
  end
  chosen_cells_with_guess2 = chosen_cells.clone()
  res2 = nil
  while (res2 == nil)
    tried_cells.push(cell)
    cell = (cell_choices - tried_cells).sample
    return res if cell == nil
    chosen_cells_with_guess2.push(cell)
    res2 = solver(filtered_cell_putty, chosen_cells_with_guess2)
    raise "Multiple ress" if res2 != nil
    chosen_cells_with_guess2.pop()
  end
end
_______________________________________________
class Object
  def deep_copy
    Marshal.load(Marshal.dump(self))
  end
end

class Sudoku

  class SudokuError < StandardError
  end

  class AlreadySet < SudokuError
  end

  class InvalidState < SudokuError
  end

  class InvalidGrid < SudokuError
  end

  ARY_9 = *(0...9).freeze
  MAT_9 = ARY_9.product(ARY_9).freeze
  ARY_3 = [0, 1, 2].freeze
  MAT_3 = ARY_3.product(ARY_3).freeze
  POSSIBLES = *(1..9).freeze


  # EmptyLinkedCell and FilledLinkedCell are really similar, 
  # hence the code could be refactorized.
  # Moreover, instead of compute the cells each time they are
  # needed, they could be store as a Sudoku instance variables.
  # Then, they would be updated when the sudoku is updated.

  class EmptyLinkedCell
    include Enumerable
    attr_reader :i, :j
    
    def initialize(sudoku, i, j)
      @i = i
      @sudoku = sudoku
      @j = j
    end
    
    def each(&block)
      return to_enum(self, :each) unless block_given?
      ARY_9.each do |k| 
        block.call(i, k) if k != @j && @sudoku[@i, k].zero?
        block.call(k, j) if k != @i && @sudoku[k, @j].zero?
      end
      
      l = @i / 3
      c = @j / 3
      
      MAT_3.each do |li, cj|
        x = l * 3 + li
        y = c * 3 + cj
        block.call(x, y) if x != @i && y != @j && @sudoku[x, y].zero?
      end
    end
  end
  
  class FilledLinkedCell
    include Enumerable
    attr_reader :i, :j
    
    def initialize(sudoku, i, j)
      @i = i
      @sudoku = sudoku
      @j = j
    end
    
    def each(&block)
      return to_enum(self, :each) unless block_given?
      ARY_9.each do |k| 
        block.call(i, k) if k != @j && @sudoku[@i, k] != 0
        block.call(k, j) if k != @i && @sudoku[k, @j] != 0
      end
      
      l = @i / 3
      c = @j / 3
      
      MAT_3.each do |li, cj|
        x = l * 3 + li
        y = c * 3 + cj
        block.call(x, y) if x != @i && y != @j && @sudoku[x, y] != 0
      end
    end
  end

  def initialize(grid)
    raise InvalidGrid if grid.size != 9 || grid.find { |l| l.size != 9 }
    raise InvalidGrid if grid.flatten.find { |v| v < 0 || v > 9} 
  
    @grid = Array.new(9) { Array.new(9, 0) }
    @possibles = Hash.new
    
    MAT_9.each { |i, j| @possibles[[i, j]] = POSSIBLES.dup }
    
    begin 
      MAT_9.each do |i, j|
        self[i, j] = grid[i][j] if grid[i][j] != 0 && @grid[i][j].zero?
      end
    rescue AlreadySet
      raise InvalidGrid
    end
    
    # Check coherence
    if MAT_9.find { |i, j| grid[i][j] != 0 && grid[i][j] != @grid[i][j]}
      raise InvalidGrid 
    end
  end
  
  def to_s
    @grid.map(&:to_s).join(",\n")
  end
  
  def complete?
    @possibles.empty?
  end
  
  def possibles
    @possibles.deep_copy
  end
  
  def linked_empty_cells(i, j)
    EmptyLinkedCell.new(self, i, j)
  end
  
  def filled_empty_cells(i, j)
    FilledLinkedCell.new(self, i, j)
  end
    
  def [](i, j=nil)
    j ? @grid[i][j] : @grid[i].dup 
  end
  
  def []=(i, j, v)
    raise AlreadySet unless @grid[i][j].zero?
    raise InvalidValue if v < 1 || v > 9
    raise InvalidState if filled_empty_cells(i, j).find { |x, y| @grid[x][y] == v }
    
    @possibles.delete([i, j])
    @grid[i][j] = v
   
    linked_empty_cells(i, j).each do |x, y|
      @possibles[[x, y]].delete(v)
      raise InvalidState if @possibles[[x, y]].empty?
      if @possibles[[x, y]].size == 1
        self[x, y] = @possibles[[x, y]].first 
      end
    end
  end
  
  def grid
    @grid.deep_copy
  end
end

# By the way, I could just raise an exception or return if
# I found a second solutions instead of going for all the 
# solutions. But I keep it that way.
# Here, we try fo fill firstly the cell with a minimum of
# possibility, but we can search for better heuristic.
module Solver
  module_function
  
  def solve(sudoku)
    return [sudoku] if sudoku.complete?
    (i, j), possibles = sudoku.possibles.min_by do |(i, j), k|
      k.size
    end
    
    solutions = []
    
    possibles.each do |v|
      copy = sudoku.deep_copy
      begin
        copy[i, j] = v
        solutions += solve(copy)
      rescue Sudoku::SudokuError
      end
    end
    solutions
  end
end


def sudoku_solver(puzzle)
  sudoku = Sudoku.new(puzzle)
  solutions = Solver.solve(sudoku)
  raise StandardError if solutions.size != 1
  solutions[0].grid
end
_______________________________________________
require 'set'

class Sudoku
  attr_reader :possibles, :to_find
  
  def to_s
    @puzzle.map(&:to_s).join("\n")
  end
  
  def valid?
   (0...9).each do |i|
     line = @puzzle[i].reject { |x| x == 0}
     column = @puzzle.map { |l| l[i] }.reject  { |x| x == 0}
     if column.size != column.uniq.size
       print "Error column #{i}"  
       #return false
     end
     if line.size != line.uniq.size
       #print "Error line #{i}"  
       return false
     end
    end
    
    (0...3).each do |i|
      (0...3).each do |j|
        block = []
        l = i / 3
        c = j / 3
        (0...3).each do |li|
          (0...3).each do |cj|
            block << @puzzle[l*3 + li][c*3 + cj] unless @puzzle[l*3 + li][c*3 + cj].zero?
          end
        end
        if block.size != block.uniq.size
          #print "Error block #{i} #{j}"  
          return false
        end
      end
    end   
    true
  end
  
  def initialize(grid)
    @puzzle = grid
    raise StandardError if grid.size != 9
    raise StandardError if grid.find { |l| l.size != 9 }
    raise StandardError unless valid?
    @possibles = Hash.new()
    @to_find = 0
    (0...9).each do |i|
      (0...9).each do |j|
        if @puzzle[i][j].zero?
          compute_possible(i, j) 
          @to_find += 1
        end
      end
    end
  end
  
  def compute_possible(i, j)
    @possibles[[i, j]] = Set.new(1..9)
    (0...9).each do |k|
      n = @puzzle[i][k]
      m = @puzzle[k][j]
      @possibles[[i, j]].delete(n) unless n.zero?
      @possibles[[i, j]].delete(m) unless m.zero?
    end
    l = i / 3
    c = j / 3
    (0...3).each do |li|
      (0...3).each do |cj|
        n = @puzzle[l*3 + li][c*3 + cj]
        @possibles[[i, j]].delete(n) unless n.zero?
      end
    end
  end
  
  def [](i, j)
    @puzzle[i][j]
  end
  
  def []=(i, j, v)
    #raise CannotRewrite, "case (#{i}, #{j} already contains #{@sudoku[i][j]}"
    @puzzle[i][j] = v
    @to_find -= 1
    @possibles.delete([i, j])
    
    (0...9).each do |k|
      if @puzzle[i][k].zero?
        @possibles[[i, k]].delete(v)
        throw(:error, false) if @possibles[[i, k]].empty?
        #if @possibles[[i, k]].size == 1
        #  v1 = @possibles[[i, k]].first
        #  return false unless (self[i, k] = v1)
        #end
      end
      if @puzzle[k][j].zero?
        @possibles[[k, j]].delete(v)
        throw(:error, false) if @possibles[[k, j]].empty?
        #if @possibles[[k, j]].size == 1
        #  v1 = @possibles[[k, j]].first
        #  return false unless (self[k, j] = v1)
        #end
      end
    end
    l = i / 3
    c = j / 3
    (0...3).each do |li|
      (0...3).each do |cj|
        if @puzzle[l*3 + li][c*3 + cj].zero?
          @possibles[[l*3 + li, c*3 + cj]].delete(@puzzle[i][j])
          throw(:error, false) if @possibles[[l*3 + li, c*3 + cj]].empty?
          #if @possibles[[l*3 + li, c*3 + cj]].size == 1
          #  v1 = @possibles[[l*3 + li, c*3 + cj]].first
          #  return false unless (self[l*3 + li, c*3 + cj] = v1)
          #end
        end
      end
    end
    true
  end
  
  def complete?
    @to_find == 0
  end
  
  def grid
    Marshal.load(Marshal.dump(@puzzle))
  end
end


class Solver
  attr_reader :sudoku, :solution, :uniq_solution
  
  def initialize(sudoku)
    @sudoku = sudoku
    @solution = nil
    @other_solution = nil
    @uniq_solution = true
  end
  
  def solved?
    !!@solution
  end
  
  
  def solve(sudoku)
    sudoku = Marshal.load(Marshal.dump(sudoku))
    loop do
      (i, j), ary = sudoku.possibles.find { |_, ary| ary.size == 1 }
      break unless i
      result = catch(:error) { sudoku[i, j] = ary.first }
      return false unless result
    end
    if sudoku.possibles.empty?
      @uniq_solution = false if solved? 
      @solution = sudoku
      return @uniq_solution
    end
    (i, j), possibles = sudoku.possibles.min_by { |h, k| k.size }
   
    possibles.each do |n|
      copy = Marshal.load(Marshal.dump(sudoku))
      if (copy[i, j] = n)
        solve(copy)
        return false if solved? && !@uniq_solution
      end
      copy = sudoku
    end
    solved? && @uniq_solution 
  end
end


def sudoku_solver(puzzle)
  #puts "The puzzle"
  #puzzle.each do |l| 
  #  print l
  #  print ","
  #  puts
  #end
  #puts 'End'
  #puts
  sudoku = Sudoku.new(puzzle)
  solver = Solver.new(sudoku)
  solver.solve(sudoku)
  #print "Multiple" unless solver.uniq_solution
  raise StandardError unless solver.solution && solver.uniq_solution
  solver.solution.grid
end
