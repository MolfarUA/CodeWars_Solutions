def cut(cake)
  map = cake.split("\n")
  cake_h = map.size
  cake_w = map.first.size
  n = cake.count('o')
  return [] unless (cake_h * cake_w % n).zero?
  piece_square = cake_h*cake_w/n
  widths = (1..piece_square).select{|w| (piece_square % w).zero?}.reverse
  result = []
  pieces = Array.new(cake_h){Array.new(cake_w){0}}
  
  cut = ->(k){
    return true if k == n  
    start_row = pieces.index{|row| row.include?(0)}
    start_col = pieces[start_row].index(0)
    widths.each{|w|
      h = piece_square/w
      rows = start_row...start_row+h
      cols = start_col...start_col+w
      if cols.end <= cake_w && rows.end <= cake_h &&
        pieces[rows].all?{|row| row[cols].all?{|x| x.zero?}} &&
        map[rows].sum{|row| row[cols].count('o')} == 1
        
        rows.each{|r| cols.each{|c| pieces[r][c] = k + 1}}
        result << [rows,cols]
        return true if cut.(k+1)
        result.pop
        rows.each{|r| cols.each{|c| pieces[r][c] = 0}}
      end  
    }
    false
  }
  cut.(0) 
  result.map{|(rows,cols)| rows.map{|r| map[r][cols]}.join("\n")}
end
_____________________________________________________
def cut cake
    k = cake.count('o')
    cake = cake.split("\n")
    n, m = cake.size, cake[0].size
    area = n * m
    area, r = area.divmod(k)
    return [] unless r.zero?

    dims = (1..[Math.sqrt(area).floor, n].min).each_with_object([]) do |i, a|
        next if area % i > 0
        j = area / i
        next if j > m
        a << i
        a << j unless i == j
    end
    dims.sort!

    accum = []
    recf = -> cake do
        res = y = nil
        if (x = cake.find_index{|r| y = /\S/ =~ r})
            dims.each_with_index do |k, i|
                l = dims[~i]
                if x+k <= n and y+l <= m
                    slice = cake[x...x+k].map{|r| r[y...y+l]}.join("\n")
                    if not slice.include?(' ') and slice.count('o') == 1
                        accum << slice
                        re = /(?<=.{#{y}})\S{#{l}}/
                        sliced = cake.map.with_index{|r,i| x <= i && i < x+k ? r.sub(re, ' ' * l) : r}
                        break if (res = recf.(sliced))
                        accum.pop
                    end
                end
            end
            res
        else
            true
        end
    end
    
    recf.(cake) ? accum : []
end
_____________________________________________________
def possible_rectangles(data, size)
  rectangles = []
  data[0].size.downto(1) do |width|
    data.size.downto(1) do |height|
      rectangles << [width, height] if width * height == size
    end
  end
  rectangles
end

def empty_position?(arr, y, x)
  arr.all? { |a| a[y][x].nil? }
end

def get_empty_position(arr)
  width = arr[0][0].size
  height = arr[0].size
  (0...height).each do |y|
    (0...width).each do |x|
      return [y, x] if arr.all? { |b| b[y][x].nil? }
    end
  end
  nil
end

def get_layer(arr, position, size, data)
  width, height = size
  y, x = position
  return nil if y + height > data.size || x + width > data[y].size

  layer = Array.new(data.size) { Array.new(data[0].size) }
  raisins = 0
  data.each_with_index do |row, yy|
    row.each_with_index do |column, xx|
      next unless
        yy.between?(y, y + height - 1) && xx.between?(x, x + width - 1)
      return nil unless empty_position?(arr, yy, xx)

      raisins += 1 if column == 'o'
      layer[yy][xx] = column
    end
  end
  return nil if raisins != 1

  layer
end

def search(raisins, arr, rectangles, data)
  return arr if raisins.zero?

  position = get_empty_position(arr)
  rectangles.each do |size|
    layer = get_layer(arr, position, size, data)
    next if layer.nil?

    arr << layer
    res = search(raisins - 1, arr, rectangles, data)
    return res unless res.nil?

    arr.pop
  end
  nil
end

def extract(board)
  board[1..-1].map do |layer|
    layer.map(&:join).reject(&:empty?).join("\n")
  end
end

def cut(cake)
  raisins = cake.count('o')
  data = cake.each_line.map { |line| line.strip.split('') }
  cells = data.size * data[0].size
  return [] unless (cells % raisins).zero?

  result = search(
    raisins,
    [Array.new(data.size) { Array.new(data[0].size) }],
    possible_rectangles(data, cells / raisins),
    data
  )
  result ? extract(result) : []
end
