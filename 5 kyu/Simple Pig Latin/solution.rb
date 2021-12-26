def pig_it text
  text.gsub(/(\w)(\w+)*/, '\2\1ay')
end

################
def pig_it text
  text.split.map{|word| word =~ /\w/ ? "#{word[1..-1]}#{word[0]}ay" : word}.join(" ")
end

###############
def pig_it text
  text.gsub(/(\w)(\w*)/){|w| $2 + $1 + 'ay' }
end

################
def pig_it text
  text.split.map do |word|
    if !('a'..'z').to_a.include?(word[0].downcase)
      word
    else
      word[1..-1] + word[0] + "ay"
    end
  end.join(' ')
end

###################
def pig_it text
  text.split(" ").map do |word|
    if word.match?(/\w/)
      first_letter = word.slice!(0)
      "#{word}#{first_letter}ay"
    else
      word
    end
  end.join(" ")
end

###################
def pig_it text
  text.split(' ').map do |x|
    if (x =~ (/[^A-Za-z0-9_]/)).nil?
      x << x[0]
      c = x.chars
      c.shift
      c.join + 'ay'
    else
     x
    end
  end.join(' ')
end

######################
ENDING = 'ay'

def pig_it text
  text.split.map {|word| word.count("\\,.?!") == 0 ? word[1..-1] + word[0] + ENDING : word}.join(' ')
end

###################
def pig_it text
  text.split.map { |x| x.match(/[^a-zA-Z\d\s:]/).nil? ? x[1..-1] + x[0] + 'ay' : x }.join(' ')
end

###################
def pig_it text
  pig = text.split.map { |word| word.chars.rotate.join }.join('ay ')
  pig[-1].match(/[a-zA-Z]/) ? pig.concat('ay') : pig
end

####################
def pig_it text
  letters = (('a'..'z').to_a + ('A'..'Z').to_a).flatten

  text = text.split(' ').map do |word|
    if word.chars.all? { |letter| letters.include?(letter) }
      word = word[1..-1] + word[0] + 'ay'
    end
    word
  end.join(' ')

  text
end

=begin
input: string 
output: a string 
goal: put the first letter of each word at the end of the word, and add ay to each word

notes: leave punctuation as it is 

option1: 
  split the input string into an array, iterate through with map 
    for each iteration, 
      if word.size > 1 
        set the current word = word[2nd-last_letter] + first letter + ay 
      
=end
