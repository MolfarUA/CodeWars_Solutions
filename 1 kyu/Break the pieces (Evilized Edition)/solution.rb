591f3a2a6368b6658800020e

MOVES4  = [[0,1], [0,-1], [1,0], [-1,0]]
MOVES8  = [[1,1], [-1,1], [1,-1], [-1,-1]]
BORDERS = '-+|'.chars.to_set

def break_evil_pieces(shape)
    return [] if shape.empty?
    
    lstShape, out = zoomIn(shape.split("\n")), []
    
    flood(1,1,lstShape)
    (1...lstShape.size-1).each{ |x| 
        (1...lstShape[0].size-1).each{ |y|
            next unless lstShape[x][y] == " "
            out << extractShape(x,y,lstShape)
        }
    }
    return out
end


def zoomIn(lst)
    out, size = [], lst.map(&:size).max * 2 + 3
    
    out << '*'*size
    lst.each{ |s|
        out << "*"+' '*(size-2)+"*"
        out << "*"
        s << " "*((size-2)/2-s.size)
        s.each_char{ |c| out[-1] << " " ; out[-1] << c }
        out[-1] << " *"
    }
    out << "*"+' '*(size-2)+"*"
    out << '*'*size
    
    for x in (1...out.size-1) do
        if x%2==0
            (3...size-2).step(2).each{ |y| out[x][y] = '-' if '-+'.include?(out[x][y-1]) && '-+'.include?(out[x][y+1]) }
        else
            (2...size-2).step(2).each{ |y| out[x][y] = '|' if '|+'.include?(out[x-1][y]) && '|+'.include?(out[x+1][y]) }
        end
    end
    return out
end


def extractShape(x,y,lstShape)
    borders = flood(x,y,lstShape)
    return formatShape(borders, lstShape)
end


def flood(x,y,lstShape)
    bag, borders = [[x,y]], []
    until bag.empty? do
        newBag = []
        for x,y in bag do
            added = 0
            lstShape[x][y] = '*'
            for dx,dy in MOVES4 do
                a, b = x+dx, y+dy
                if lstShape[a][b] != '*'
                    if BORDERS.include?(lstShape[a][b])
                        borders << [a,b]
                        added += 1
                    end
                    if lstShape[a][b] == " "
                        lstShape[a][b] = '*'
                        newBag << [a,b]
                    end
                end
            end
            if added >= 2
                for dx,dy in MOVES8 do
                    a, b = x+dx, y+dy
                    borders << [a,b] if lstShape[a][b] == '+'
                end
            end
        end
        bag = newBag
    end
    return borders.to_set
end


def formatShape(borders, lstShape)
    miX,maX,miY,maY = borders.first.zip(*borders).map!(&:minmax).flatten!
    lX,lY = maX-miX+1, maY-miY+1
    shape = (1..lX).map{|_| ' '*lY}
    
    borders.each{ |x,y| 
        c = lstShape[x][y]
        if c=='+'
            neighs = MOVES4.map{ |dx,dy| [x+dx, y+dy] }
                           .reject!{|a,b| ' *'.include?(lstShape[a][b]) || !borders.include?([a,b]) }
            if neighs.size==2
                c = neighs[0][0] == neighs[1][0] ? '-'
                  : neighs[0][1] == neighs[1][1] ? '|' : c
            end      
        end
        shape[x-miX][y-miY] = c
    }
    return (0...shape.size).step(2).map{ |x| (0...shape[x].size).step(2).map{|y| shape[x][y]}.join.rstrip }.join("\n")
end
____________________________________________________________________
COLORS = '!abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890[]{}=_)(*&^%$#@`,.<>/?'.split('')

class Array
  def neighbours(h, w)
    x, y = self
    result = []
    result << [x - 1, y] if x > 0
    result << [x + 1, y] if x < h - 1
    result << [x, y - 1] if y > 0
    result << [x, y + 1] if y < w - 1
    result
  end

  def expand(h, w)
    x, y = self
    result = []
    if x > 0
      result << [x - 1, y - 1] if y > 0
      result << [x - 1, y]
      result << [x - 1, y + 1] if y + 1 < w
    end
    result << [x, y - 1] if y > 0
    result << [x, y + 1] if y + 1 < w
    if x + 1 < h
      result << [x + 1, y - 1] if y > 0
      result << [x + 1, y]
      result << [x + 1, y + 1] if y + 1 < w
    end
    result
  end
end

class Breaker
  attr_reader :pieces

  def initialize(shape)
    @map = shape.lines.map { |line| line.chomp }
    @h = @map.size
    @w = @map.map { |line| line.size }.max
    @pieces = []

    paint
  end

  def paint
    borders =
      0.upto(@w - 1).flat_map { |y| [[0, y], [@h - 1, y]] } +
      0.upto(@h - 1).flat_map { |x| [[x, 0], [x, @w - 1]] }

    borders.each do |x, y|
      fill x, y, COLORS[0] if self[x, y] == ' '
    end

    color = 1

    indices.each do |x, y|
      if self[x, y] == ' '
        fill x, y, COLORS[color]
        color += 1
      end
    end

    1.upto(color - 1) do |i|
      extract COLORS[i]
    end
  end

  def fill(x, y, color)
    remaining = [[x, y]]

    while remaining.length > 0
      a, b = remaining.shift
      if self[a, b] == ' '
        self[a, b] = color
        remaining += [a, b].neighbours(@h, @w)
      end
    end
  end

  def indices_of_color(color)
    result = []
    0.upto(@h - 1) do |x|
      line = @map[x]
      next unless line.include? color

      y = line.index color
      while y
        result << [x, y]
        y = line.index(color, y + 1)
      end
    end
    result
  end

  def indices
    (0...@h).to_a.product((0...@w).to_a)
  end

  def extract(color)
    marked = indices_of_color(color).flat_map { |p| p.expand(@h, @w) }.uniq
    l, r = marked.map { |_, y| y }.minmax
    t, b = marked.map(&:first).minmax
    r = @w - r
    b = @h - b
    w = @w - l - r + 1
    h = @h - t - b + 1

    result = nil
    result = h.times.map { ' ' * w }

    pluses = []

    marked.each do |x, y|
      value = self[x, y]
      result[x - t][y - l] = value if value == '|' or value == '-' or value == '+'

      pluses << [x - t, y - l] if value == '+'
    end

    pluses.each do |x, y|
      next unless result[x][y] == '+'

      if (x == 0 || result[x - 1][y] == ' ') and (x + 1 == h || result[x + 1][y] == ' ')
        result[x][y] = '-'
      elsif (y == 0 || result[x][y - 1] == ' ') and (y + 1 == w || result[x][y + 1] == ' ')
        result[x][y] = '|'
      end
    end

    piece = result.join("\n").gsub(/^ +\n/, '')

    prefix = piece.scan(/^ */).min_by { |a| a.length }
    piece = piece.gsub(/ +$/, '').gsub(/^#{prefix}/, '')

    @pieces << piece.chomp
  end

  def [](x, y)
    return nil if x < 0 || x >= @h || y < 0
    @map[x][y]
  end

  def []=(x, y, v)
    return nil if x < 0 || x >= @h || y < 0
    @map[x][y] = v
  end

  def show
    puts @map.join("\n")
  end
end

def explode(shape)
  map = shape.lines.map { |line| line.chomp.split('') }
  h = map.size
  w = map.map { |line| line.size }.max

  result = (h * 2).times.map { (w * 2).times.map { ' ' } }

  0.upto(h - 1).each do |x|
    0.upto(w - 1).each do |y|
      char = map[x][y]
      result[x * 2][y * 2] = char
      result[x * 2 + 1][y * 2] = '|' if char == '+' and x.succ < h and map[x + 1][y] =~ /[|+]/
      result[x * 2 + 1][y * 2] = '|' if char == '|' and x.succ < h
      result[x * 2][y * 2 + 1] = '-' if char == '+' and y.succ < w and map[x][y + 1] =~ /[-+]/
      result[x * 2][y * 2 + 1] = '-' if char == '-' and y.succ < w
    end
  end

  result.map { |line| line.join('') }.join("\n")
end

def implode(shape)
  shape.lines
    .select.with_index { |_, i| i.even? }
    .map { |line| line.split('').select.with_index { |_, i| i.even? }.join.chomp }
    .join("\n")
end

def break_evil_pieces(text)
  return [] if text =~ /\A\s*\z/
  Breaker.new(explode(text)).pieces.map { |piece| implode(piece) }
end

____________________________________________________________________
def flood_fill(shape, i, piece, line_length)
  if i >= 0 and i < piece.size
    piece[i] = shape[i] unless shape[i] == 'X'
    if shape[i] == ' '
      shape[i] = 'X'
      flood_fill(shape, i + 1, piece, line_length)
      flood_fill(shape, i - 1, piece, line_length)
      flood_fill(shape, i - line_length, piece, line_length)
      flood_fill(shape, i + line_length, piece, line_length)
    elsif /[\-\+]/ =~ shape[i]
      piece[i - 1] = '+' if i > 0 and shape[i - 1] == '+'
      piece[i + 1] = '+' if i < shape.size - 1 and shape[i + 1] == '+'
    end
  end
end

def inflate_vertical(shape, i, inflated_cols)
  prev_end = shape.rindex("\n", i) || -1
  i = i - prev_end + 1
  line_end = -1
  inflated_cols.push(i + line_end)
  inflated_cols.each_index { |j| inflated_cols[j] += 1 if inflated_cols[j] > i + line_end }
  while i + line_end < shape.size
    if (/[\+\-]/ =~ shape[i + line_end]) and i != 0 and /[\+\-]/ =~ shape[i + line_end - 1]
      shape.insert(i + line_end, '-')
    else
      shape.insert(i + line_end, ' ')
    end
    line_end = shape.index("\n", line_end + 1) || shape.size
  end
end

def inflate_horizontal(shape, i, inflated_lines, line_length)
  prev_end = shape.rindex("\n", i) || -1
  prev_prev_end = nil
  if prev_end > 0
      prev_prev_end = shape.rindex("\n", prev_end - 1) || -1
  end
  line_end = shape.index("\n", i) || shape.size
  i = prev_end + 1
  s = ''
  while i < line_end
    if /[\+\|]/ =~ shape[i] and prev_prev_end and /[\+\|]/ =~ shape[prev_prev_end + i - prev_end]
      s += '|'
    else
      s += ' '
    end
    i += 1
  end
  shape.insert(prev_end + 1, s + "\n")
  inflated_lines.push((prev_end + 1) / line_length + 1)
  inflated_lines.each_index { |j| inflated_lines[j] += 1 if inflated_lines[j] > inflated_lines[-1] }
end

def fix_corners(piece, line_length)
  i = -1
  while (i = piece.index('+', i + 1))
    if ((i > 0 and /[\-\+]/ =~ piece[i - 1]) or (i + 1 < piece.size and /[\-\+]/ =~ piece[i + 1]))
      if ((i >= line_length and /[\|\+]/ =~ piece[i - line_length]) or (i + line_length < piece.size and /[\|\+]/ =~ piece[i + line_length]))
        piece[i] = '+'
      else
        piece[i] = '-'
      end
    else
      piece[i] = '|'
    end
  end
end

def break_evil_pieces(shape)
  original_length = line_length = shape.each_line.map { |l| l.size }.max
  return [] if line_length.nil?
  s = shape.each_line.map { |l| l.chomp + ' ' * (line_length - l.size) }.join("\n").chop
  pieces = []
  inflated_cols = []
  i = -1
  while i = s.index(/[\|\+][\|\+]/, i + 1)
    inflate_vertical(s, i, inflated_cols)
    line_length += 1
  end
  if line_length > 1
    i = -1
    while i = s.index(Regexp.new("\\+ .{#{line_length - 2}} \\+", Regexp::MULTILINE), i + 1)
      inflate_vertical(s, i, inflated_cols)
      line_length += 1
    end
  end
  if line_length > 1
    i = -1
    while i = s.index(Regexp.new(" \\+.{#{line_length - 2}}\\+ ", Regexp::MULTILINE), i + 1)
      inflate_vertical(s, i, inflated_cols)
      line_length += 1
    end
  end
  inflated_lines = []
  if line_length > 0
    i = -1
    r = Regexp.new("\\-.{#{line_length - 1}}\\-", Regexp::MULTILINE)
    while i = s.index(r, i + 1)
      inflate_horizontal(s, i + line_length, inflated_lines, line_length)
    end
  end
  inflated_cols.sort!
  inflated_lines.sort!
  while i = s.index(' ')
    piece = s.gsub(/[\S ]/, 'X')
    flood_fill(s, i, piece, line_length)
    fix_corners(piece, line_length)
    piece = "\n" + piece
    inflated_cols.reverse_each do |j|
      k = -1
      while k = piece.index("\n", k + 1)
        piece[k + j + 1] = ''
      end
    end
    piece = piece[1..-1]
    inflated_lines.reverse_each { |j| piece[((j - 1) * original_length)...(j * original_length)] = '' }
    piece = "\n" + piece + "\n"
    while piece.gsub!(/\nX*\n/, "\n")
    end
    j = piece.scan(/\n(X*)\S/).flatten.map { |t| t.size }.min
    piece.gsub!(Regexp.new("\nX{#{j}}"), "\n") unless j.nil?
    piece.gsub!(/X+\n/, "\n")
    piece = piece[1..-2]
    if !(/(\n )|( \n)|(\n\n)/ =~ piece) and ((piece.index(' ') || s.size) > (piece.index("\n") || -1)) and ((piece.rindex(' ') || -1) < (piece.rindex("\n") || s.size))
      pieces.push(piece.gsub('X', ' '))
    end
  end
  return pieces.sort
end
____________________________________________________________
require 'set'

BOUNDARIES = Set.new(%w(- + |))
H_BOUNDARIES = Set.new(%w(| +))
V_BOUNDARIES = Set.new(%w(- +))

class Value
  def initialize(v)
    @value = v
  end

  def to_s
    @value.to_s
  end

  def clear!
    @value = ' '
  end
end

class Cell
  attr_reader :char, :i, :j, :value
  def initialize(i, j, char)
    @i = i
    @j = j
    @char = char
    @boundary = BOUNDARIES.include?(@char)
    @empty = !@boundary
  end

  def boundary?
    @boundary
  end

  def value=(v)
    @value = v
    @empty = false
  end

  def empty?
    @empty
  end

  def to_s
    #boundary? ? '·' : (@value || @char).to_s
    boundary? ? @char : (@value || @char).to_s
  end

  alias inspect to_s
end

class Grid

  attr_reader :n,:m, :shapes

  def initialize(text)
    lines = text.sub(/^\n+/,'').sub(/\n+$/, '').split("\n").map{|line| line.rstrip}
    @m = lines.size
    @n = lines.map(&:size).max
    @table = lines.map.with_index{|line,i|
      line.rstrip.ljust(@n).chars.map.with_index{|char,j|
        Cell.new(i,j,char)
      }
    }
    @shapes = []
    # pack
  end

  def double!
    @m = 2*m - 1
    @n = 2*n - 1
    old_table = @table
    @table = Array.new(@m) do |i|
      Array.new(@n) do |j|
        case [i.even?, j.even?]
        when [true, true]
          Cell.new(i, j, old_table[i/2][j/2].char)
        when [false, true]
          u, d = old_table[(i-1)/2][j/2], old_table[(i+1)/2][j/2]
          if [u, d].all?{|x| H_BOUNDARIES.include? x.char}
            Cell.new(i, j, '|')
          else
            Cell.new(i, j, ' ')
          end
        when [true, false]
          l, r = old_table[i/2][(j-1)/2], old_table[i/2][(j+1)/2]
          if [l, r].all?{|x| V_BOUNDARIES.include? x.char}
            Cell.new(i, j, '-')
          else
            Cell.new(i, j, ' ')
          end
        else
          Cell.new(i, j, ' ')
        end
      end
    end
  end

  def fill!
    i = 0
    while cell=first_empty_cell
      shape = Shape.new(i+=1)
      @shapes << shape
      expand(shape, cell)
    end
  end

  def expand(shape, cell)
    if !cell
      shape.clear!
      @shapes.delete(shape)
      return
    end
    return unless cell.empty?
    shape.add(cell)
    i = cell.i
    j = cell.j
    expand(shape, get_cell(i+1,j))
    expand(shape, get_cell(i-1,j))
    expand(shape, get_cell(i,j+1))
    expand(shape, get_cell(i,j-1))
  end

  def first_empty_cell
    cells.find{|c| c.empty?}
  end

  def to_s
    rows.map do |row|
      row.join(' ')
    end.join("\n")
  end
  alias inspect to_s

  def get_cell(i, j)
    i >= 0 && j >= 0 && @table[i][j] rescue nil
  end

  def cells
    @cells ||= (
    rows.flat_map do |row|
      row.map do |cell|
        cell
      end
    end
    )
  end

  def rows
    Enumerator.new do |y|
      @table.each do |row|
        y << row
      end
    end
  end
end

class Shape
  attr_reader :cells, :value
  def initialize(value)
    @value = Value.new(value)
    @cells = []
  end

  def add(cell)
    cell.value = value
    @cells << cell
  end

  def clear!
    @value.clear!
  end

  def to_s
    min_i, max_i = cells.map{|c| c.i}.minmax
    min_j, max_j = cells.map{|c| c.j}.minmax

    # Create empty table with placeholders
    table = Array.new(max_i - min_i + 3){
      Array.new(max_j - min_j + 3){
        ' '
      }
    }

    cross_table = Array.new(max_i - min_i + 3){
      Array.new(max_j - min_j + 3){
        [false, false]
      }
    }

    # Add cells
    cells.each do |c|
      table[c.i-min_i+1][c.j-min_j+1] = 'X'
    end

    # Add boundaries
    table.each_with_index do |row, i|
      row.each_with_index do |cell, j|
        if cell == ' '
          if i > 0 && table[i-1][j] == 'X'
            table[i][j] = "-"
            cross_table[i][j+1][1] = true
            cross_table[i][j-1][1] = true
          elsif i < max_i - min_i + 2 && table[i+1][j] == 'X'
            table[i][j] = "-"
            cross_table[i][j+1][1] = true
            cross_table[i][j-1][1] = true
          elsif j > 0 && table[i][j-1] == 'X'
            table[i][j] = "|"
            cross_table[i-1][j][0] = true
            cross_table[i+1][j][0] = true
          elsif j < max_j - min_j + 2 && table[i][j+1] == 'X'
            table[i][j] = "|"
            cross_table[i-1][j][0] = true
            cross_table[i+1][j][0] = true
          end
        end
      end
    end

    # Add crosses
    table.each_with_index do |row, i|
      row.each_with_index do |cell, j|
        if cross_table[i][j].all?
          table[i][j] = "+"
        end
      end
    end

    # Only keep boundaries
    table.map{|row| row.join.rstrip}.join("\n").gsub('X', ' ')
  end

  def half_to_s
    to_s.split("\n").select.with_index{|r, i| i.even?}.map{|line|
      line.chars.select.with_index{|c, j| j.even?}.join
    }.join("\n")
  end
end


def break_pieces(shape)
  grid = Grid.new(shape)
  grid.fill!
  grid.shapes.map{|shape| shape.to_s}
end

def break_evil_pieces(shape)
  return [] if shape.empty?
  grid = Grid.new(shape)
  grid.double!
  grid.fill!
  grid.shapes.map{|shape| shape.half_to_s }
end
