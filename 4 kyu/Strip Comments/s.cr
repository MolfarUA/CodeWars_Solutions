51c8e37cee245da6b40000bd


def solution(input : String, markers : Array(String))
  input.each_line.join("\n") do |l|
    m = markers.map { |x| l.index(x) }.compact.min?
    m.nil? ? l : l[0...m].strip
  end
end
__________________________________
def solution(input : String, markers : Array(String))
  return input if markers.empty?
  input.lines.map do |line|
    line.gsub(/\s*#{Regex.union(markers)}.*/, "")
  end.join("\n")
end
__________________________________
def solution(input : String, markers : Array(String))
  a=input.split("\n")
  markers.each{|m| a=a.map{|x| f(m,x)}}
  a.join("\n")
end
def f(m,x)
  o=""
  i=x.index(m)
  !i ? x : i==0 || x==m.to_s ? "" : x[0..i-1].gsub(/ +$/,"")
end
__________________________________
def solution(input : String, markers : Array(String))
  return input if markers.size == 0
  start = /^(#{markers.map { |m| "\\#{m}" }.join("|")}).*/
  pattern = /\s+(#{markers.map { |m| "\\#{m}" }.join("|")}).*/
  input.split("\n")
    .map { |str| str.gsub(start, "").empty? ? "" : str.gsub(pattern, "") }
    .join("\n")
end
