52bb6539a4cf1b12d90005b7


def validate_battlefield(field)
    
     if field.map{|f| f = f.sum}.sum != 20
      return false
     end
    
    @new_field = Array.new(Array.new(12)).map{|a| a = Array.new(12,0)}
    
    for i in 0..9
      for j in 0..9
        @new_field[i+1][j+1] = field[i][j]
      end
    end
    
    for i in 1..10
      for j in 1..10
        if @new_field[i][j] == 1 && (@new_field[i-1][j-1] == 1 || @new_field[i+1][j-1] == 1 || @new_field[i-1][j+1] == 1 || @new_field[i+1][j+1] == 1)
          return false
        end
      end
    end
    
    @count = [0,0,0,0]
     for i in 0..10
      @count[1] += check(@new_field.transpose[i].join,"0110") + check(@new_field[i].join,"0110")
      @count[2] += check(@new_field.transpose[i].join,"01110") + check(@new_field[i].join,"01110")
      @count[3] += check(@new_field.transpose[i].join,"011110") + check(@new_field[i].join,"011110")
     end
     
     if @count[3] != 1 || @count[2] != 2 || @count[1] != 3
       return false
     else
       return true
     end
end

def check(a, b)
  if a.include?(b)
    return 1 + check(a.sub(b,b.gsub("1","0")),b)
  else
    return 0
  end
end
____________________________________________________________
def validate_battlefield(field)
  grid = field.dup
  ships = Array.new(5){Array.new}
  4.downto(1) do |i|
    2.times do
      grid.map! do |row|
        row.join.gsub(/#{"1"*i}/) {|match| ships[i] << 1; "x"*i}.chars
      end
      grid = grid.transpose
    end
  end
  
  #check for diagonals
  return false if grid.each_cons(2).any? do |first_row, second_row| 
    [first_row, second_row.drop(1) + ["0"],  ["0"] + second_row.take(second_row.size-1)].transpose.any? do |first,middle,last| 
      first == "x" && (first == middle || first == last)
    end
  end
    
  ships.reject(&:empty?).map(&:size) == [4,3,2,1]
end
____________________________________________________________
def count_neighbors(field, row, col)
  result = -1
  (row-1..row+1).select {|r| (0..9) === r}.each do |r|
    (col-1..col+1).select {|c| (0..9) === c}.each do |c|
      result += field[r][c]
    end
  end
  result
end

def validate_battlefield(field)
  cells = field.flatten.reject(&:zero?).size
  return false unless cells == 20
  neighbors = 0
  (0..9).each do |row|
    (0..9).each do |col|
      unless field[row][col].zero?
        neighbors += count_neighbors(field, row, col)
      end
    end
  end
  neighbors == 20
end
____________________________________________________________
def validate_battlefield(field)
  BattleshipValidator.new(field).validate
end

class BattleshipValidator
  def initialize(field)
    @field = field
    @is_horizontal = false
    @is_vertical = false
    @ships = []
  end
  
  def validate
    @field.each_with_index do |row, row_index|
      row.each_with_index do |value, column_index|
        @is_horizontal = false
        @is_vertical = false
        
        if value == 1    
          next if @ships.flatten(1).include?([row_index, column_index])
          
          ship = []
          
          check_if_horizontal(row, row_index, column_index, ship)
          check_if_vertical(row_index, column_index, ship) if !@is_horizontal

          return false unless validate_neighbours(row_index, column_index)
        end
      end
    end
    
    return validate_ships
  end
  
  def check_if_horizontal(row, row_index, column_index, ship)
    row.drop(column_index).each_with_index do |value, index|  
      @is_horizontal = true if index > 0 && value == 1

      set_ship(ship, row_index, column_index + index, value)
      break if value != 1
    end
  end
  
    
  def check_if_vertical(row_index, column_index, ship)
    @field.transpose[column_index].drop(row_index).each_with_index do |value, index| 
      @is_vertical = true if index > 0 && value == 1

      set_ship(ship, row_index + index, column_index, value)
      break if value != 1
    end
  end
  
  def set_ship(ship, row, column, value)
    if value == 1
      point = [row, column]
      ship << point unless @ships.flatten(1).include?(point) || ship.include?(point)
    end

    @ships << ship if (value == 0 || column == 9) && !ship.empty? && !@ships.include?(ship)
    
    ship
  end
  
  def validate_neighbours(row, column)
    if @is_horizontal
      return false if row != 9 && column != 0 && @field[row + 1][column - 1] == 1

      @field[row].drop(column).each_with_index do |value, index|
        return false if row != 9 && @field[row + 1][column + index] == 1
        
        break if value == 0
      end
    elsif @is_vertical
      @field.transpose[column].drop(row).each_with_index do |value, index|
        return false if @field[row + index][column + 1] == 1

        if value == 0
          return false if column > 0 && @field[row + index][column - 1] == 1
          
          break
        end
      end
    else
      return false if row != 9 && column != 9 && @field[row + 1][column + 1] == 1
      return false if row != 9 && column != 0 && @field[row + 1][column - 1] == 1
    end
    
    true
  end
  
  def validate_ships
    @ships.map(&:size).sort == [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
  end
end
____________________________________________________________
def validate_battlefield(field)
  valid = true
  # primeiro procure erros 
  for i in 0..9
    for j in 0..9
      if i != j and field[i][j] == 1
        #navios na diagonal
        valid = false if i < 9 and j < 9 and field[i+1][j+1] == 1
        valid = false if i < 9 and j > 0 and field[i+1][j-1] == 1 
        valid = false if i > 0 and j < 9 and field[i-1][j+1] == 1 
        valid = false if i > 0 and j > 0 and field[i-1][j-1] == 1 
        
        #navio com tamanho maior que 4
        valid = false if i < 6 and field[i+1][j] == 1 and field[i+2][j] == 1 and field[i+3][j] == 1 and field[i+4][j] == 1
        valid = false if j < 6 and field[i][j+1] == 1 and field[i][j+2] == 1 and field[i][j+3] == 1 and field[i][j+4] == 1
      end
    end
  end
  
  bat = 1
  cru = 2
  des = 3
  sub = 4

  if valid
    for i in 0..9
      for j in 0..9
        if field[i][j] == 1
          if i < 6 and field[i+1][j] == 1 and field[i+2][j] == 1 and field[i+3][j] == 1 and field[i+4][j] == 0
            bat -= 1 
            field[i][j] = 0
            field[i+1][j] = 0
            field[i+2][j] = 0
            field[i+3][j] = 0
          end
          if j < 6 and field[i][j+1] == 1 and field[i][j+2] == 1 and field[i][j+3] == 1 and field[i][j+4] == 0
            bat -= 1 
            field[i][j] = 0
            field[i][j+1] = 0
            field[i][j+2] = 0
            field[i][j+3] = 0
          end
          if i > 3 and field[i-1][j] == 1 and field[i-2][j] == 1 and field[i-3][j] == 1 and field[i-4][j] == 0 
            bat -= 1 
            field[i][j] = 0
            field[i-1][j] = 0
            field[i-2][j] = 0
            field[i-3][j] = 0
          end
          if j > 3 and field[i][j-1] == 1 and field[i][j-2] == 1 and field[i][j-3] == 1 and field[i][j-4] == 0
            bat -= 1 
            field[i][j] = 0
            field[i][j-1] = 0
            field[i][j-2] = 0
            field[i][j-3] = 0
          end
        end
      end
    end
    valid = false if bat != 0
  end

  if valid
    for i in 0..9
      for j in 0..9
        if field[i][j] == 1
          if i < 7 and field[i+1][j] == 1 and field[i+2][j] == 1 and field[i+3][j] == 0
            cru -= 1 
            field[i][j] = 0
            field[i+1][j] = 0
            field[i+2][j] = 0
          end
          if  j < 7 and field[i][j+1] == 1 and field[i][j+2] == 1 and field[i][j+3] == 0
            cru -= 1 
            field[i][j] = 0
            field[i][j+1] = 0
            field[i][j+2] = 0
          end
          if i > 2 and field[i-1][j] == 1 and field[i-2][j] == 1 and field[i-3][j] == 0
            cru -= 1 
            field[i][j] = 0
            field[i-1][j] = 0
            field[i-2][j] = 0
          end
          if j > 2 and field[i][j-1] == 1 and field[i][j-2] == 1 and field[i][j-3] == 0
            cru -= 1 
            field[i][j] = 0
            field[i][j-1] = 0
            field[i][j-2] = 0
          end
        end
      end
    end
    valid = false if cru != 0
  end

  if valid
    for i in 0..9
      for j in 0..9
        if field[i][j] == 1
          if i < 8 and field[i+1][j] == 1 and field[i+2][j] == 0
            des -= 1 
            field[i][j] = 0
            field[i+1][j] = 0
          end
          if j < 8 and field[i][j+1] == 1 and field[i][j+2] == 0
            des -= 1 
            field[i][j] = 0
            field[i][j+1] = 0
          end
          if i > 1 and field[i-1][j] == 1 and field[i-2][j] == 0
            des -= 1 
            field[i][j] = 0
            field[i-1][j] = 0
          end
          if j > 1 and field[i][j-1] == 1 and field[i][j-2] == 0
            des -= 1 
            field[i][j] = 0
            field[i][j-1] = 0
          end
        end
      end
    end
    valid = false if des != 0
  end

  if valid
    for i in 0..9
      for j in 0..9
        if field[i][j] == 1
          if i < 9 and field[i+1][j] == 0
            sub -= 1 
            field[i][j] = 0
          elsif j < 9 and field[i][j+1] == 0
            sub -= 1 
            field[i][j] = 0
          elsif i > 0 and field[i-1][j] == 0
            sub -= 1 
            field[i][j] = 0
          elsif j > 0 and field[i][j-1] == 0
            sub -= 1 
            field[i][j] = 0
          end
        end
      end
    end
    valid = false if sub != 0
  end

  return valid
        
end
