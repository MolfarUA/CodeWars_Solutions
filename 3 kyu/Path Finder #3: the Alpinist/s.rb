576986639772456f6f00030c


def get_lowest(remaining)
  lowest_coord = nil
  lowest_val = Float::INFINITY
  
  remaining.each do |k, v|
    if v < lowest_val
      lowest_val = v
      lowest_coord = k
    end
  end
  
  lowest_coord
end

def start(maze, h, remaining)
  len = maze.size
  
  while remaining.size > 0
    coord = get_lowest(remaining)
    x,y = coord
    total = h[[x,y]]

    if x < len-1
      climb = (maze[x+1][y] - maze[x][y]).abs
      if h[[x+1, y]] > total+climb
        h[[x+1, y]] = total + climb
        remaining[[x+1, y]] = total + climb
      end
    end

    if x > 0
      climb = (maze[x-1][y] - maze[x][y]).abs
      if h[[x-1, y]] > total+climb
        h[[x-1, y]] = total + climb
        remaining[[x-1, y]] = total + climb
      end
    end

    if y > 0
      climb = (maze[x][y-1] - maze[x][y]).abs
      if h[[x, y-1]] > total+climb
        h[[x, y-1]] = total + climb
        remaining[[x, y-1]] = total + climb
      end
    end

    if y < len - 1
      climb = (maze[x][y+1] - maze[x][y]).abs
      if h[[x, y+1]] > total+climb
        h[[x, y+1]] = total + climb
        remaining[[x, y+1]] = total + climb
      end
    end
    
    remaining.delete(coord)
  end
end

def path_finder(maze)
   maze = maze.split("\n")
  
   maze = maze.map do |s|
     s.chars.map { |c| c.to_i }
   end
   start1 = Time.now()
  
   h = {}
   remaining = {}
  
   (0...maze.size).each do |i|
     (0...maze.size).each do |j|
       remaining[[i, j]] = Float::INFINITY
       h[[i, j]] = Float::INFINITY
     end
   end
   remaining[[0, 0]] = 0
   h[[0, 0]] = 0
  
   start(maze, h, remaining) 
  
   h[[maze.size-1, maze.size-1]]
end
_____________________________
def path_finder(maze)
  maze_string_array = maze.split("\n").map{ |n| n.split('') }
  @maze_array = maze_string_array.map{ |i| i.map { |j| j.to_i }}
  @dist = Array.new(@maze_array.length) { Array.new(@maze_array[0].length, 999999) }
  @dist[0][0] = 0
  @open = [[0, 0]]
  while @dist[-1][-1] >= 999999
    choose_candidate(get_candidates)
    close_exhausted
  end
  return @dist[-1][-1]
end

def get_candidates
  candidates = {dummy: 999999}
  @open.each do |i|
    candidates.merge!({[i[0] - 1, i[1]] => @dist[i[0]][i[1]] + (@maze_array[i[0] - 1][i[1]] - @maze_array[i[0]][i[1]]).abs}) if i[0] > 0 && @dist[i[0] - 1][i[1]] >= 999999 && @dist[i[0]][i[1]] + (@maze_array[i[0] - 1][i[1]] - @maze_array[i[0]][i[1]]).abs <= candidates.values.min
    candidates.merge!({[i[0] + 1, i[1]] => @dist[i[0]][i[1]] + (@maze_array[i[0] + 1][i[1]] - @maze_array[i[0]][i[1]]).abs}) if i[0] < @maze_array.length - 1 && @dist[i[0] + 1][i[1]] >= 999999 && @dist[i[0]][i[1]] + (@maze_array[i[0] + 1][i[1]] - @maze_array[i[0]][i[1]]).abs <= candidates.values.min
    candidates.merge!({[i[0], i[1] - 1] => @dist[i[0]][i[1]] + (@maze_array[i[0]][i[1] - 1] - @maze_array[i[0]][i[1]]).abs}) if i[1] > 0 && @dist[i[0]][i[1] - 1] >= 999999 && @dist[i[0]][i[1]] + (@maze_array[i[0]][i[1] - 1] - @maze_array[i[0]][i[1]]).abs <= candidates.values.min
    candidates.merge!({[i[0], i[1] + 1] => @dist[i[0]][i[1]] + (@maze_array[i[0]][i[1] + 1] - @maze_array[i[0]][i[1]]).abs}) if i[1] < @maze_array[0].length - 1 && @dist[i[0]][i[1] + 1] >= 999999 && @dist[i[0]][i[1]] + (@maze_array[i[0]][i[1] + 1] - @maze_array[i[0]][i[1]]).abs <= candidates.values.min
  end
  return candidates
end

def choose_candidate(candidates)
  candidates.select{ |k, v| v == candidates.values.min }.each do |k, v|
    @dist[k[0]][k[1]] = v
    @open << k
  end
end

def close_exhausted
  @open.reject!{ |i| can_be_closed?(i[0], i[1]) }
end

def can_be_closed?(x, y)
  return false if @dist[x][y] >= 999999

  return false if x > 0 && @dist[x - 1][y] >= 999999

  return false if x < @dist.length - 1 && @dist[x + 1][y] >= 999999

  return false if y > 0 && @dist[x][y - 1] >= 999999

  return false if y < @dist[0].length - 1 && @dist[x][y + 1] >= 999999
  
  return true
end
_____________________________
def path_finder(maze)
  map = maze.split("\n").map(&:chars).map{|s| s.map(&:to_i)}
  rounds = map.map{|s| s.map{Float::INFINITY}}
  rounds[0][0] = 0
  queue = [[0, 0]]
  while !queue.empty?
    x,y = queue.shift
    level = map[x][y]
    r = rounds[x][y]
    [[0,1], [1,0], [0,-1], [-1,0]].each{|dx, dy|
      if ((0...map.size) === x+dx) && ((0...map.first.size) === y+dy) && 
      rounds[x+dx][y+dy] > (newR = r + (level - map[x+dx][y+dy]).abs)
        rounds[x+dx][y+dy] = newR
        queue << [x + dx, y + dy]
      end  
    }
  end
  rounds.last.last
end

