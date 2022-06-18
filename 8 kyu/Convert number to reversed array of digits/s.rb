def digitize(n)
  n.to_s.chars.reverse.map(&:to_i)
end
________________________
def digitize(n)
  n.to_s.split('').reverse!.map(&:to_i)
end
________________________
def digitize(n)
  num = n.to_s
  i = (num.size - 1)
  j = 0
  reverse = []
  while i >= 0
    puts num[5]
    reverse[j] = num[i].to_i
    i -= 1
    j +=1
    end
  return reverse
end
________________________
def digitize(n)
  n.to_s.split('').map{|i| i.to_i}.reverse!
end
________________________
def digitize(n)
  n.to_s.split("").reverse.map{|k| k.to_i}
end
________________________
def digitize(n)
  reverse_digits = []
  n.to_s.each_char do |i|
    reverse_digits << i.to_i
  end
  reverse_digits.reverse!
end
