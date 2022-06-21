5254ca2719453dcc0b00027d


def permutations(string)
  string.chars.permutation.map(&:join).uniq
end
______________________________
def permutations(string)
  string.chars.permutation.uniq.map(&:join)
end
______________________________
def permutations(string)
  arr = string.split('')

  perm_helper(arr)
end

def perm_helper(arr)
  return arr if arr.length <= 1
  
  arr.each_with_index.map do |element, index|
    befores = before(arr, index)
    afters = after(arr, index)
    combined = befores + afters
    permuted = perm_helper(combined)

    permuted.each_with_index.map do |x, y|
      ([element] + [x]).join
    end
  end.flatten.uniq
end

def after(arr, index)
  return [] if (index + 1 == arr.length)
  arr.slice(index + 1, arr.length - 1)
end

def before(arr, index)
  return [] if (index == 0)
  arr.slice(0, index)
end
______________________________
def permutations(string)  
  string.chars.permutation.to_a.map{|e| e.join}.uniq 
end
