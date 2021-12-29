def alphabet_position(text)
  text.gsub(/[^a-z]/i, '').chars.map{ |c| c.downcase.ord - 96 }.join(' ')
end

________________________________________________
def alphabet_position(text)
  # Delete everything but letters from the string
  only_letters = text.delete("^a-zA-Z")
  
  # Make every letter in the new string lowercase
  lower_case = only_letters.downcase
  
  # Convert each letter to byte position
  # Note: byte positions are sequential - subtract 96 from
  # each value and you get their position in the alphabet
  byte_value = lower_case.bytes
  
  # Produce new array using .map with alphabet position correct
  mapped_text = byte_value.map { |ltr| ltr - 96 }
  
  # Return final answer
  final_answer = mapped_text.join(' ')
end

________________________________________________
def alphabet_position(text)
  text.upcase.chars.select { |c| ("A".."Z").include?(c) } .map { |c| c.ord-64 } .join(" ")
end

________________________________________________
def alphabet_position(text)
  result = ''
  text.split('').each do |c|
    case c.downcase
      when 'a'
        result += '1 '
      when 'b'
        result += '2 '
      when 'c'
        result += '3 '
      when 'd'
        result += '4 '
      when 'e'
        result += '5 '
      when 'f'
        result += '6 '
      when 'g'
        result += '7 '
      when 'h'
        result += '8 '
      when 'i'
        result += '9 '
      when 'j'
        result += '10 '
      when 'k'
        result += '11 '
      when 'l'
        result += '12 '
      when 'm'
        result += '13 '
      when 'n'
        result += '14 '
      when 'o'
        result += '15 '
      when 'p'
        result += '16 '
      when 'q'
        result += '17 '
      when 'r'
        result += '18 '
      when 's'
        result += '19 '
      when 't'
        result += '20 '
      when 'u'
        result += '21 '
      when 'v'
        result += '22 '
      when 'w'
        result += '23 '
      when 'x'
        result += '24 '
      when 'y'
        result += '25 '
      when 'z'
        result += '26 '
      else
        result = result
    end
  end
  result[0..-2]
end

________________________________________________
def alphabet_position(text)
  alphabet = ("a".."z").to_a
  text = text.downcase.chars
  positions = []
  text.each do |char|
    if alphabet.include? char
      positions << alphabet.find_index(char).to_i + 1
    end
  end
  
  positions.join(" ")
end
