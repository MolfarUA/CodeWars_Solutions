59eb1e4a0863c7ff7e000008


def solve(s,ops)
  s = s.chars.map do |el| 
    el == 't' ? 1 : 0
  end
  
  Hash.new { |k, v|
    l, r, res = v
    next k[v] = res == s[l] ? 1 : 0 if l == r
    next k[v] = s[l].send(ops[l],s[r]) == res ? 1 : 0 if r - l == 1
    k[v] = (l...r).to_a.product([0,1],[0,1])
    .map {|mid, l_res, r_res| l_res.send(ops[mid], r_res) == res ? k[[l, mid, l_res]] * k[[mid+1, r, r_res]] : 0}
    .sum
  }[[0, s.size-1, 1]]
end
_________________________________________
def solve(s,ops)
  TrueFalseCounter.new(s, ops).count[0]  
end

class TrueFalseCounter
  @@count_hash = {"t" => [1,0],
    "f" => [0,1],
    "tt&" => [1,0],
    "tt|" => [1,0],
    "tt^" => [0,1],
    "tf&" => [0,1],
    "tf|" => [1,0],
    "tf^" => [1,0],
    "ft&" => [0,1],
    "ft|" => [1,0],
    "ft^" => [1,0],
    "ff&" => [0,1],
    "ff|" => [0,1],
    "ff^" => [0,1]
  }
  
  def initialize(s, ops)
    @s = s
    @ops = ops
  end
    
  def calculate_count(s, ops)
    count = [0, 0]
  
    # Iterate through operators calculating number of possible true results
    # if selected operator is the last to be evaluated
    ops.chars.each_with_index { |op, i|    
      # Get count of possible results either side of operator
      left_count = TrueFalseCounter.new(s[0, i+1], ops[0, i]).count
      right_count = TrueFalseCounter.new(s[i+1, s.length-i], ops[i+1, ops.length - i - 1]).count
      
      total = left_count.reduce(:+) * right_count.reduce(:+)
      
      # Calculate additional true counts
      add_true_count = left_count[0] * right_count[0] if (op == "&")   
      add_true_count = total - (left_count[1] * right_count[1]) if (op == "|")
      add_true_count = left_count[0] * right_count[1] + left_count[1] * right_count[0] if (op == "^")
      
      count[0] += add_true_count
      count[1] += total - add_true_count
    }
    
    count
  end

  def count
    @@count_hash[@s+@ops] ||= self.calculate_count(@s, @ops)
  end
  
end
_________________________________________
def solve(values, ops)
  p [values, ops]
  count(values.split('').map {|s| s == 't'}, ops.split('').map(&:to_sym)).first
end

def count(values, ops, from = 0, to = ops.length, cache = {})
  return values[from] ? [1, 0] : [0, 1] if from >= to || from > ops.length
  return cache[[from, to]] if cache.include?([from, to])
  cache[[from, to]] = (from...to).map do |i|
    op = ops[i]
    left_t, left_f = count(values, ops, from, i, cache)
    right_t, right_f = count(values, ops, i + 1, to, cache)
    case op
    when :&
      [left_t * right_t, left_f * right_f + left_t * right_f + left_f * right_t]
    when :|
      [left_t * (right_t + right_f) + left_f * right_t, left_f * right_f]
    when :^
      [left_t * right_f + left_f * right_t, left_t * right_t + left_f * right_f]
    end
  end.transpose.map {|arr| arr.reduce &:+}
end
