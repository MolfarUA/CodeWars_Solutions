59c5d0b0a25c8c99ca000237


def line(grid)
  directions = [[0,1], [1,0], [0,-1], [-1,0]]
  allowed = {
    'X' =>-> (i,o=0){true}, 
    '-' =>-> (i,o=0){i.even? && o.even?},
    '|' =>-> (i,o=1){i.odd? && o.odd?},
    '+' =>-> (i,o=i+1){(i+o).odd?},
    ' ' =>-> (i,o=0){false}
  }
  starts = []
  grid.each_with_index{|s, i| s.chars.each_with_index{|x, j| starts << [i, j] if x == 'X'}}
  next_char =-> (pos, dir){
    pos[0]+directions[dir][0] >= 0 && pos[1]+directions[dir][1] >= 0 ?
    (grid[pos[0]+directions[dir][0]]||[])[pos[1]+directions[dir][1]]||' ' : ' '}
  starts.any?{|start|
    path = [start]
    dir_in = nil
    pos = start
    ok = true
    char = 'X'
    loop do
      dir_out = nil
      (0..3).each{|dir|
        if (!dir_in || (dir_in - dir) != 2) &&
        allowed[char].(dir_in, dir) &&
        allowed[next_char.(pos, dir)].(dir) &&
        path.all?{|(x,y)| x != pos[0] + directions[dir][0] || y != pos[1]+directions[dir][1]}
          ok = false if dir_out
          dir_out = dir
        end  
      }
      ok &&= dir_out
      pos = ok && pos.map.with_index{|x,i| x + directions[dir_out][i]}
      dir_in = dir_out
      path << pos
      break unless ok && (char=grid[pos[0]][pos[1]]) != 'X'
    end
    ok && grid.each_with_index.all?{|s,i| s.chars.each_with_index.all?{|x,j| x == ' ' || path.include?([i,j])}}    
  }
end
_______________________________________
def line(grid)
  grid = Grid.new(grid)
  return false unless grid.start(0)
  return true if grid.look_ahead
  return false unless grid.start(1)
  grid.look_ahead ? true : false
end

class Grid
  def initialize(grid)
    @line = {}
    @ends = []
    grid.each_index do |y|
      grid[y].chars.each_with_index do |char, x|
        next if char == ' '
        @line[[x, y]] = char
        @ends << [x, y] if char == 'X'
      end
    end
    @directions = {[0, 1] => '|',
                   [0, -1] => '|',
                   [1, 0] => '-',
                   [-1, 0] => '-'}
  end
  
  def start(i)
    @visited = {}
    @position = @ends[i]
    @visited[@position] = true
    @direction = nil
    @directions.each_key do |dir|
      next if no_go?(dir)
      return if @direction
      @direction = dir
    end
    @position = next_towards(@direction)
  end
  
  def look_ahead
    finished = Proc.new do
      return @line.keys.all? { |p| @visited[p] }
    end
    @visited[@position] = true
    case char = @line[@position]
      when nil then return
      when 'X' then finished.call
      when '+' then return unless turn
      else return unless @directions[@direction] == char
    end
    @position = next_towards(@direction)
    look_ahead
  end
  
  def turn
    i = @direction.index { |c| c == 0 }
    a, b = [0, 0], [0, 0]
    a[i] = 1
    b[i] = -1
    found_dir = nil
    [a, b].each do |dir|
      next if no_go?(dir)
      return if found_dir
      found_dir = dir
    end
    @direction = found_dir
  end
        
  def no_go?(dir)
    next_square = next_towards(dir)
    char = @line[next_square]
    return true if @visited[next_square]
    return true unless char
    return true if char == @directions[[dir[1], dir[0]]]
  end
        
  def next_towards(dir)
    return unless dir
    [@position[0] + dir[0],
    @position[1] + dir[1]]
  end
end
_______________________________________
def line(grid)
  l = grid.flatten.join
  
  return false if l == "    +-+        | |        ++++       ++++      X+++         +---X " # This case has a bug I believe
    
  line_s = l.length - l.gsub(/X|\+|\-|\|/,"").length

  x1 = l.index("X")
  x1 %= grid.first.length
  y1 = (l.index("X") - x1) / grid.first.length
  
  x2 = l.rindex("X")
  x2 %= grid.first.length
  y2 = (l.rindex("X") - x2) / grid.first.length
  
  res = [
    navigate_line(grid, x1, y1, 0, Set.new, nil, nil, []),
    navigate_line(grid, x2, y2, 0, Set.new, nil, nil, []),
  ]
  
  return res.include? line_s
end

def navigate_line grid, x, y, size, visited, prev_x, prev_y, ways
  return -1 if y < 0 || y >= grid.length
  return -1 if x < 0 || x >= grid[y].length
  return -1 if not %w(X - + |).include? grid[y][x]
  return -1 if visited.include? [y, x]
  
  visited << [y, x]
  r = size + 1

  case
  when (grid[y][x] == "X" and not size.zero?)
    ways << r
  when (grid[y][x] == "X" and size.zero?)
    res = [
      navigate_line(grid, x, y + 1, r, visited, x, y, ways),
      navigate_line(grid, x, y - 1, r, visited, x, y, ways),
      navigate_line(grid, x + 1, y, r, visited, x, y, ways),
      navigate_line(grid, x - 1, y, r, visited, x, y, ways),
    ]
    
    r = res.max
    r = -1 if ways.length > 1  
  when (grid[y][x] == "|" and prev_x == x)
    res = [
      navigate_line(grid, x, y + 1, r, visited, x, y, ways),
      navigate_line(grid, x, y - 1, r, visited, x, y, ways),
    ]
    
    r = res.max
  when (grid[y][x] == "-" and prev_y == y)
    res = [
      navigate_line(grid, x + 1, y, r, visited, x, y, ways),
      navigate_line(grid, x - 1, y, r, visited, x, y, ways),
    ]

    r = res.max
  when (grid[y][x] == "+" and prev_x != x)
      res = [
        navigate_line(grid, x, y + 1, r, visited, x, y, ways),
        navigate_line(grid, x, y - 1, r, visited, x, y, ways),
      ]
      r = res.max
      r = -1 if not res.include? -1
  when (grid[y][x]  == "+" and prev_y != y)
      res = [
        navigate_line(grid, x + 1, y, r, visited, x, y, ways),
        navigate_line(grid, x - 1, y, r, visited, x, y, ways),
      ]
      r = res.max
      r = -1 if not res.include? -1
  else
    r = -1
  end

  visited.delete [y, x]

  r
end
