57f75cc397d62fc93d000059


def calc(s)
  s.chars.map(&:ord).join.count('7')*6
end
__________________________________
def calc(s)
  s.codepoints.join.count('7') * 6
end
__________________________________
def calc(s)
  s.chars.map(&:ord).join.count(?7)*6
end
