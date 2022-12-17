598d91785d4ce3ec4f000018


def wordValue(arr)
 arr.map!.with_index(1){
   |element, idx| element.delete(" ").chars.map{
    |char| (p char.ord - 96)}.reduce(&:+) * idx} 
 arr
end
_____________________________
def wordValue(l)
  l.map.with_index(1){|s,i|i*s.chars.sum{|c|c.ord%32}}
end
_____________________________
def wordValue(arr)
  arr.map.with_index(1) { |word, i| i * word.bytes.sum { |n| n % 32 } }
end
