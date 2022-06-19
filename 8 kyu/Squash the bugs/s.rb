56f173a35b91399a05000cb7


def find_longest(string)
  string.split.map(&:length).max
end
__________________________
def find_longest(str)
  spl = str.split(" ")
  longest = 0
  i=0
  while (i < spl.length) do
    if (spl[i].length > longest) then longest = spl[i].length end
    i=i+1
  end
  longest
end
__________________________
def find_longest(string)
  string.split(' ').map{|s| s.size}.max
end
__________________________
def find_longest(string)
  spl = string.split(" ")
  longest = 0
  i=0
  spl.each do |str|
    if str.length > longest
     longest = str.length
    end
  end
  longest
end
