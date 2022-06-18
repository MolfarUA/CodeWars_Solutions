5917a2205ffc30ec3a0000a8


def deep_dup(obj)
  return obj.kind_of?(Array) ? obj.map{|e| deep_dup(e)} : obj
end

class Skyscrapers
    @@run_procs = [                      # Procs for creating list of relevant indices for each clue
        ->(i,j,n){ i + j*n }, 
        ->(i,j,n){ n*(i+1) - j - 1 }, 
        ->(i,j,n){ n*(n-j) - i - 1 }, 
        ->(i,j,n){ n*(n-i-1) + j }
    ]
    
    def initialize(n)                  
        @n, @tabs = n, {}                # Size of grid and creation of tabulized data hash
        @runs = build_runs()             # Runs are all relevant boxes for each clue, in the appropriate order
        @perms = build_perms()           # Create list of all possible permutations for each clue 0-N
    end
    
    def solve(clues)
        @clues = clues
        @grid = Array.new(@n*@n){ (1..@n).to_a } # create array of each individual square
      
        deduce()
        return format() if solved?()             
      
        og = deep_dup(@grid)                     # create deep dup of grid so guesses can be reverted easily
        og.each_with_index do |pos, i|
            next if pos.size == 1                # Skip single element lists
            pos.each do |n|
                @grid[i] = [n]                   # Set block to a single value of those possible
                deduce()
                return format() if solved?()
            end
            @grid = deep_dup(og)                 # Reset grid to the originally deduced grid
        end
      
        return "No solution exists"
    end
  
private
  
    def build_runs
      return [].tap do |runs|
          @@run_procs.each do |pro|
              runs.push( *(0...@n).map do |i| 
                  (0...@n).map{|j| pro.call(i, j, @n) } 
              end)
          end
      end
    end
  
    def build_perms
        return [].tap do |arr|
            arr[0] = (1..@n).to_a.permutation.to_a
            arr[0].each do |perm|
                prev = 0
                idx = perm.count{|p| prev < p && (prev = p)}
                (arr[idx] ||= []) << perm
            end
        end
    end

    def solved?
        @grid.all?{|e| e.size == 1}
    end
  
    def format
        @grid && @grid.flatten.each_slice(@n).to_a
    end
    
    def deduce(change = true)
        while change
            change = false
            (0...@clues.size).each do |i|
                pos = possibles( @clues[i], @runs[i].map{|j| @grid[j]} ) 
                return unless pos
                change = update_vals(@runs[i], pos) || change
            end
        end
        return @grid
    end
  
    def possibles(clue, vals)
        key = "#{clue}: " + vals.map(&:join).join(" ")
        return @tabs[key] if @tabs.has_key?(key)
      
        tmp = @perms[clue].select do |p|
          (0...@n).all?{|i| vals[i].include?(p[i])}
        end
      
        @tabs[key] = tmp.empty? ? nil : tmp[0].zip(*tmp[1..-1]).map{ |e| e.uniq }
        return @tabs[key] 
    end
  
    def update_vals(vals, pos)
        change = false
        (0...@n).each do |j|
            tmp = @grid[vals[j]] & pos[j]
            if @grid[vals[j]] != tmp
                @grid[vals[j]] = tmp
                change = true
            end
        end
        return change
    end
    
end


SCRAPER_7x7 = Skyscrapers.new(7)

def solve_puzzle(clues)
  SCRAPER_7x7.solve(clues)
end
______________________________________________
# Create all possible permutations for each clue 0-6, and store globally
# ----------------------------------------------------------------------
N = 7
TABS = {}
ALL_PERMS = (1..N).to_a.permutation.to_a
PERMS = (0..N).map do |n|
  ALL_PERMS.select do |perm|
    prev = 0
    n.zero? || n == perm.count{|p| prev < p && (prev = p)}
  end
end


def deep_dup(obj)
  return obj.kind_of?(Array) ? obj.map{|e| deep_dup(e)} : obj
end

# Find all matching permutations for a given clue and the currently possible values (Hash)
# ----------------------------------------------------------------------------------------
def get_possibles(clue, vals)
  key = "#{clue}: " + vals.map(&:join).join(" ")
  return TABS[key] if TABS.has_key?(key)
  
  tmp = PERMS[clue].select{ |p| (0...N).all?{|i| vals[i].include?(p[i])} }
  return TABS[key] = tmp.empty? ? nil : tmp[0].zip(*tmp[1..-1]).map{ |e| e.uniq.sort }
end


# Fetch row/col with relevant direction (right and bottom clues are 'backwards')
# ------------------------------------------------------------------------------
def get_run(rows, cols, i)
  case i/N
    when 0; return cols[  i%N  ]
    when 1; return rows[  i%N  ].reverse
    when 2; return cols[N-i%N-1].reverse
    when 3; return rows[N-i%N-1]
  end
end


# Update section values with intersection of given values (pos)
# -------------------------------------------------------------
def update_vals(vals, pos)
  change = false
  (0...N).each do |j| 
    tmp = vals[j] & pos[j]
    if vals[j] != tmp
      vals[j].replace(tmp)
      change = true
    end
  end
  return change
end


# Primary solve method. This algorithm is deductive, and will return
# the most deductively simplified grid.
# -------------------------------------------------------------------
def deductive_solve(rows, clues)
  cols = rows.transpose
  loop do
    change = false
    
    (0...clues.size).each do |i|
      vals = get_run(rows, cols, i)
      pos = get_possibles( clues[i], vals )
      
      return unless pos
      change = update_vals(vals, pos) || change
    end
    break if !change
  end
  return rows
end

# Entry method. 
#
def solve_puzzle(clues)
  rows = Array.new(N){ Array.new(N){ (1..N).to_a } }
  deductive_solve(rows, clues)
  return rows.map(&:flatten) if rows.all?{|row| row.all?{|e| e.size == 1}}
  
  guess_list = rows.flatten(1).select{|r| r.size > 1}.sort_by{|e| -e.size}
  guess_list.each do |pos|
    copy = pos.clone
    (0...pos.size).each do |i|
      pos.replace([pos[i]])
      tmp = deductive_solve(deep_dup(rows), clues)
      return tmp.map(&:flatten) if tmp && tmp.all?{|row| row.all?{|e| e.size == 1}}
      pos.replace(copy)
    end
  end
  
  return "No solution exists"
end
________________________________
# Permutation fitting is the most approachable option for small board sizes.

$size = 7
$rng = (0 ... $size)

$rows_per_visible = (1 .. $size).to_a.permutation.inject(Array.new($size + 1){ [] }) do |accum, perm|
    visible_count = perm.inject([0, 0]) do |(maxh, cnt), curh|
        maxh, cnt = curh, cnt + 1 if maxh < curh
        [maxh, cnt]
    end .last
    accum[0].push(perm) # any permutation fits empty clue
    accum[visible_count].push(perm)
    accum
end

def fit row_fits, col_fits
    loop do
        break if row_fits.any?(&:empty?) # contradiction
        return row_fits.map(&:first) if row_fits.all?{|fit| fit.size == 1}
        previous = row_fits.map(&:dup)
        $rng.each do |i|
            $rng.each do |j|
                common = col_fits[i].map{|fit| fit[j]} & row_fits[j].map{|fit| fit[i]}
                col_fits[i].select!{|fit| common.include?(fit[j])}
                row_fits[j].select!{|fit| common.include?(fit[i])}
            end
        end
        break if previous == row_fits # needs futher guess
    end
end

def search row_fits, col_fits
    min_fit, i = row_fits.zip($rng).reject{|fit, _| fit.size == 1}.min_by{|fit, _| fit.size}
    min_fit.inject(nil) do |result, perm|
        row_fits_copy = row_fits.map(&:dup)
        col_fits_copy = col_fits.map(&:dup)
        row_fits_copy[i] = [perm]
        result || fit(row_fits_copy, col_fits_copy)
    end
end

def solve_puzzle clues
    col_fits = $rng.map do |idx|
        opposite_clue = clues[3 * $size - idx - 1]
        $rows_per_visible[clues[idx]] & $rows_per_visible[opposite_clue].map(&:reverse)
    end

    row_fits = ($size ... 2 * $size).map do |idx|
        opposite_clue = clues[5 * $size - idx - 1]
        $rows_per_visible[clues[idx]].map(&:reverse) & $rows_per_visible[opposite_clue]
    end

    fit(row_fits, col_fits) || search(row_fits, col_fits)
end
___________________________________
class Numeric
  def other_side
    ((self / 7) % 2 == 0 ? 20 : 34) - self
  end
end

class Array
  def prefix?(other)
    other.zip(self).all? { |a, b| a == b }
  end

  def simplify(&block)
    size = self.size
    select!(&block)
    size != self.size
  end

  def seen
    reduce([0, 0]) { |(a, m), h| [a + (h > m ? 1 : 0), [h, m].max] }.first
  end
end

N = 7
ALL = [1, 2, 3, 4, 5, 6, 7]
CLUES = []
CLUES[0] = ALL.permutation.to_a
1.upto(N).each { |n| CLUES[n] = ALL.permutation.select { |row| row.seen == n } }

def solve_puzzle(clues)
  columns = 0.upto(N - 1).map { |n| CLUES[clues[n]] & CLUES[clues[n.other_side]].map(&:reverse) }
  rows = 27.downto(21).map { |n| CLUES[clues[n]] & CLUES[clues[n.other_side]].map(&:reverse) }

  while simplify rows, columns
  end

  top = rows.first.select { |row| row.map.with_index.all? { |n, i| columns[i].any? { |c| c[0] == n } } }
  progress = top.map { |row| row.map { |x| [x] } }
  1.upto(N - 1) { |n| progress = append progress, rows[n], columns }
  progress.first.transpose
end

def simplify(rows, columns)
  first = cross rows, columns
  second = cross columns, rows

  first || second
end

def cross(rows, columns)
  simplified = false

  uniqs = (
    uniques(rows) +
    uniques(columns).map { |i, j, n| [j, i, n] }
  ).uniq

  uniqs.each do |i, j, n|
    simplified |= knock(rows, i, j, n)
    simplified |= knock(columns, j, i, n)
  end

  simplified |= smoosh rows, columns
  simplify |= smoosh columns, rows

  simplified
end

def uniques(lines)
  result = []

  lines.each_with_index do |line, i|
    line.transpose.map(&:uniq).each.with_index do |possible, j|
      if possible.size == 1
        result << [i, j, possible.first]
      end
    end
  end

  result
end

def knock(lines, i, j, n)
  simplified = false

  lines.each.with_index do |line, k|
    if k == i
      simplified |= line.simplify { |ns| ns.map.with_index.all? { |v, l| l == j ? v == n : v != n } }
    else
      simplified |= line.simplify { |ns| ns[j] != n }
    end
  end

  simplified
end

def smoosh(rows, columns)
  simplified = false
  allowed = rows.map { |row| row.transpose.map(&:uniq) }
  0.upto(N - 1) do |n|
    simplified |= columns[n].simplify { |col| col.map.with_index.all? { |v, i| allowed[i][n].include?(v) } }
  end
  simplified
end

def append(grids, rows, allowed)
  result = []
  grids.each do |grid|
    rows.each do |row|
      next if row.zip(grid).any? { |n, col| col.include?(n) }
      it = grid.zip(row).map { |col, n| col + [n] }
      result << it if allowed.zip(it).all? { |cols, ic| cols.any? { |col| col.prefix?(ic) } }
    end
  end

  result
end
