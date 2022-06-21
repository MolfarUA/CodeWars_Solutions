5870fa11aa0428da750000da


def execute(code)
  r, c = 0, 0
  dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
  dir_idx = 0
  path = [[r,c]]
  code.scan(/[FLR]\d*/).each do |cmd|
    steps = cmd.size > 1 ? cmd[1..-1].to_i : 1
    case cmd[0]
    when 'L' then dir_idx = (dir_idx-steps) % 4
    when 'R' then dir_idx = (dir_idx+steps) % 4
    else
      dir_r, dir_c = dirs[dir_idx]
      steps.times do
        r += dir_r
        c += dir_c
        path << [r, c]
      end
    end
  end
  min_r, max_r = path.map(&:first).minmax
  min_c, max_c = path.map(&:last).minmax
  path.map!{|r_idx,c_idx| [r_idx-min_r, c_idx-min_c]}
  rows = max_r - min_r + 1
  columns = max_c - min_c + 1
  (0...rows).map{|r_idx| (0...columns).map{|c_idx| path.include?([r_idx, c_idx]) ? '*' : ' '}.join}.join("\r\n")
end
__________________________
def execute(code)
  stars = Set.new
  direction = 0
  directions = [[1,0], [0,1], [-1,0], [0,-1]]
  stars << (x,y = 0,0)
  code.scan(/[FLR]\d*/){|command|
    [command[1..-1].to_i, 1].max.times{
      { 'L' => ->(){direction = direction.pred % 4},
        'R' => ->(){direction = direction.succ % 4},
        'F' => ->(){stars << (x, y = x + directions[direction].first, y + directions[direction].last)}
      }[command[0]].()
    }  
  }
  min_x, max_x, min_y, max_y = [:first, :last].flat_map{|f| stars.map(&f).minmax}
  (min_y..max_y).map{|y| (min_x..max_x).map{|x| stars === [x,y] ? '*' : ' '}.join}.join("\r\n")
end
__________________________
def execute(code)
  
  grid = [["*"]]
  d, i, j = "R", 0, 0
  
  turn_right = { 'R' => 'D', 'D' => 'L', 'L' => 'U', 'U' => 'R' }
  turn_left = { 'R' => 'U', 'U' => 'L', 'L' => 'D', 'D' => 'R' }
  
  code.scan(/([RLF])(\d*)/).each do |move, count|
      
      count = count.empty?? 1 : count.to_i
      
      if move == "R" then count.times { d = turn_right[d] }
      elsif move == "L" then count.times { d = turn_left[d] }
      else 
        count.times {
          if d == "R"
            j += 1
            if j == grid[i].size then (0...grid.size).each { |ii| grid[ii] += [" "] } end
          elsif d == "L"
            j -= 1
            if j.negative? then ((0...grid.size).each { |ii| grid[ii] = [" "] + grid[ii] }; j = 0) end
          elsif d == "U"
            i -= 1
            if i.negative? then (grid.unshift([" "] * grid.first.size); i = 0) end
          else
            i += 1
            if i == grid.size then grid << [" "] * grid.first.size end
          end
          grid[i][j] = "*"               
        } 
      end
    end
    grid.map(&:join).join("\r\n")
end
