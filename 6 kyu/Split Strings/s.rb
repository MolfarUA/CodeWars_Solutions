515de9ae9dcfc28eb6000001


def solution str
  (str + '_').scan /../
end
________________________________
def solution(str)
    str << "_" if str.length % 2 != 0
    str.chars.each_slice(2).map(&:join)
end
________________________________
def solution(str)
  str.concat('_').scan /../
end
________________________________
def solution(str)
  (str+"_").scan(/[\w]{2}/)
end
________________________________
def solution(str)
  str.chars.each_slice(2).map { |d| d.length == 2 ? d.join : d.join+'_' }
end
