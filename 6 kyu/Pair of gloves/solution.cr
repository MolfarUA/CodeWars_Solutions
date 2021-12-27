def number_of_pairs(gloves)
  gloves.group_by(&.itself).map{|k,a|a.size/2}.sum
end

_____________________
def number_of_pairs(gloves)
  gloves.reduce(Hash(String, Int32).new(0)) { |h, x| h[x] += 1; h }.values.sum { |n| n / 2 }
end

_______________
def number_of_pairs(gloves)
  gloves.uniq.sum{|x| gloves.count(x) / 2}
end

________________
def number_of_pairs(gloves)
  gloves.group_by(&.itself).map { |_, a| a.size / 2 }.sum
end

______________
def number_of_pairs(gloves : Iterable(T)) forall T
  gloves.each_with_object(Hash(T, Int32).new(0)){ |g, ks| ks[g] += 1 }.values.sum{ |k| k / 2 }
end

______________
def number_of_pairs(gloves)
    cnt = 0
    gloves = gloves.sort
    i = 0
    while i < gloves.size - 1
        if gloves[i] == gloves[i+1]
            cnt += 1
            i += 2
        else
            i += 1
        end
    end
    return cnt
end

