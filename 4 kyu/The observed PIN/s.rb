5263c6999e0f40dee200059d


def get_pins(observed)
  mapping = {
    "1" => %w(1 2 4), 
    "2" => %w(1 2 3 5),
    "3" => %w(2 3 6), 
    "4" => %w(1 4 5 7), 
    "5" => %w(2 4 5 6 8), 
    "6" => %w(3 5 6 9), 
    "7" => %w(4 7 8), 
    "8" => %w(5 7 8 9 0), 
    "9" => %w(6 8 9), 
    "0" => %w(8 0)
  }
  observed.split(//).map {|key| mapping[key] }.reduce {|m, x| m.product(x).map(&:join) }
end
______________________________
def get_pins(observed)
  observed.chars.map(&{
    '1' => [[1],[2],[4]],     '2' => [[1],[2],[3],[5]],     '3' => [[2],[3],[6]],
    '4' => [[1],[4],[5],[7]], '5' => [[2],[4],[5],[6],[8]], '6' => [[3],[5],[6],[9]],
    '7' => [[4],[7],[8]],     '8' => [[5],[7],[8],[9],[0]], '9' => [[6],[8],[9]],
    '0' => [[0],[8]],
  }).reduce(&:product).map(&:join)
end
______________________________
PAD = [
        [ '1', '2', '3'],
        [ '4', '5', '6'],
        [ '7', '8', '9'],
        [ nil, '0', nil]
      ]

def get_adjacent(number)
  row, col = row_of_number(number), col_of_number(number)

  above = PAD[row-1][col] unless row.zero?
  left = PAD[row][col-1] unless col.zero?
  right = PAD[row][col+1]
  below = PAD[row+1][col] unless row >= 3

  [above, left, PAD[row][col], right, below].compact
end

def row_of_number(number)
  return 3 if number.to_i.zero?
  (number.to_i - 1) / 3
end

def col_of_number(number)
  return 1 if number.to_i.zero?
  (number.to_i - 1) % 3
end

def get_pins(observed)
  possible_pins = []
  observed.each_char do |number|
    possible_pins << get_adjacent(number.to_i)
  end
  possible_pins.first.product(*possible_pins[1..-1]).collect{|pin| pin.join('') }
end
