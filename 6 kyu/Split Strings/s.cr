515de9ae9dcfc28eb6000001


def solution(str)
  str.chars.in_groups_of(2, '_').map(&.join)
end
________________________________
def solution(str)
  (str + '_').scan(/../).map(&.[](0))
end
________________________________
def solution(str : String) : Array(String)
  str.each_char.in_groups_of(2, '_', true).map(&.join).to_a
end
________________________________
def solution(str)
  str.split(/(^\d{1(?=(\w{2})*$)|\w{2})/, remove_empty: true).map &.ljust(2, '_')
end
________________________________
def solution(str)
  if str.size % 2 > 0
    str = "#{str}_"
  end
  
  res = [] of String
  (str.size // 2).times do |i|
    res << String.build do |builder|
      builder << str[i * 2]
      builder << str[i * 2 + 1]
    end
  end

  res
end
