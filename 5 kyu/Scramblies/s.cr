55c04b4cc56a697bb0000048


def scramble(s1,s2)
 s2.chars.uniq.all?{|x| s2.count(x)<=s1.count(x)}
end
______________________________
def scramble(s1, s2)
  s1_hash = s1.split(//).group_by { |c| c }
  s2_hash = s2.split(//).group_by { |c| c }
  
  
  s2_hash.all? { |k, v| s1_hash[k] >= v rescue false }
end
______________________________
def scramble(s1, s2)
  ht = {} of Char => Int32
  s1.each_char{|c| ht[c]=(ht[c]? || 0)+1}
  s2.each_char do |c|
    ht[c] = (ht[c]? || 0)-1
    return false if ht[c] < 0
  end
  true
end
