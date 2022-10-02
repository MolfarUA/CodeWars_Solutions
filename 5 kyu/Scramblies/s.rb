55c04b4cc56a697bb0000048


def scramble(s1,s2)
  s2.chars.uniq.all?{|x| s2.count(x)<=s1.count(x)}
end
______________________________
def scramble(s1,s2)
  s2.chars.all? { |c| s1.sub!(c, '') }
end
______________________________
def scramble(s1, s2)
  s2.chars.uniq.none? { |c| s1.count(c) < s2.count(c) }
end
