595970246c9b8fa0a8000086


def capitalize_word(word)
  word.capitalize
end
______________________
def capitalize_word(word)
  word.gsub(/^(\w)/) { $1.upcase }
end
______________________
def capitalize_word(word)
  i = 0
  new = word.split('')
  h = []
  new.each do |x|
    while i == 0
      h.push(x[i].upcase)
      i+=1
    end
  end
  h.push(new[1..-1])
  return h.join
end
