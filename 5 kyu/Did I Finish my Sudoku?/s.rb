53db96041f1a7d32dc0004d2


def done_or_not(board) #board[i][j]
    check_rows(board) && check_regions(board) && check_cols(board)? "Finished!":"Try again!"    
end 

def check_regions(board)
    slices = board.each_slice(3).to_a
    regions = slices.map {|s| s.transpose.reduce(:+).each_slice(9).to_a}.reduce(:+)
    regions.map{|e| check_sum(e)}.reduce(:&)
end

def check_rows(board)
    board.map {|e| check_sum(e)}.reduce(:&)
end

def check_cols(board)
    board.transpose.map {|e| check_sum(e)}.reduce(:&)
end

def check_sum(block)
    block.reduce(:+) == 45
end
________________________________
def done_or_not(board)
  valid9 = ->(row) { row.uniq.inject(:+) == 45 }
  square9 = ->(x, y) { (y..y+2).map { |j| board[j][x,3] }.inject(:+) }
  board.all? { |row| valid9[row] } && board.transpose.all? { |row| valid9[row] } &&
    [0, 3, 6].product([0, 3, 6]).all? { |x, y| valid9[square9[x, y]] } ? "Finished!" : "Try again!"
end
________________________________
class Array
  def sum
    self.inject { |a, i| a + i }
  end
end

def done_or_not(board)
  board.each_with_index do |line, x|
    return 'Try again!' if line.sum != 45
    
    if [0,3,6].include?(x)
        [0,3,6].each do |y|
        square = board[x][y, 3] + board[x + 1][y, 3] + board[x + 2][y, 3]
        return 'Try again!' if square.sum != 45
      end
    end
  end
  
  board.transpose.each do |line|
    return 'Try again!' if line.sum != 45
  end
  
  'Finished!'
end
