def smash(words)
  words.join ' '
end
_____________________________________
def smash(words)
  words * ' '
end

_____________________________________
def smash(words)
 return "" if words.empty?
  words.inject("") do |m,w|
      m << w << " "
  end.chop!
end

_____________________________________
def smash(words)
  words.join (' ')
end

words = Array.new
words << 'Mike'
words << 'Katya'

puts smash(words)
