58c5577d61aefcf3ff000081


def encode_rail_fence_cipher(str, num_rails)
  transform(num_rails,str.length).zip(str.chars).sort().map{|l|l[1]}.join('')
end

def decode_rail_fence_cipher(str, num_rails)
   transform(num_rails, str.length).sort().zip(str.chars).sort_by{|l|l[0][1]}.map{|l|l[1]}.join('')
end

def transform(num_rails, size)
    pat = (0..num_rails - 1).to_a + (1..num_rails - 2).to_a.reverse()
    pat.cycle.first(size).zip(0..size)
end
_____________________________
def encode_rail_fence_cipher(str, n)
  (0...n).map do |r|
    gap = 2 * n - 2 
    down, up = [r, (gap - r)].map { |x| x.step(str.size - 1, gap).to_a }
    (down. zip(up)).flatten.uniq
  end.flatten.compact.map { |idx| str[idx] }.join
end

def decode_rail_fence_cipher(str, n)
  (str.chars.zip encode_rail_fence_cipher((0...str.size).map(&:chr), n).chars.map(&:ord))
  .sort_by(&:last)
  .map(&:first)
  .join 
end
_____________________________
def encode_rail_fence_cipher(str, num_rails)
  transform(num_rails, str.size).zip(str.chars).sort.map(&:last).join
end

def decode_rail_fence_cipher(str, num_rails)
  transform(num_rails, str.size).sort.map(&:last).zip(str.chars).sort.map(&:last).join
end

def transform(num_rails, size)
  (0.upto(num_rails - 1).to_a + (num_rails - 2).downto(1).to_a).cycle.take(size).zip(0..size)
end
