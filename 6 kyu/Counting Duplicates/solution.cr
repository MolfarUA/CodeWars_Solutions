def duplicate_count(text)
    text.downcase.each_char.tally.map { |x, y| x if y > 1 }.compact.size
end
_________________
def duplicate_count(text)
    letter_counts = Hash(Char, Int32).new(default_value: 0)

        text.each_char do |char|
            letter_counts[char.upcase] += 1
        end

        result = 0
        letter_counts.each do |key, value|
            if value > 1
                result += 1
            end
        end

        return result
end
________________________
def duplicate_count(text)
  text.downcase.chars.tally.count { |_, n| n > 1 }
end
_____________________
def duplicate_count(text)
  chars = text.downcase.chars
  chars.uniq.count do |c|
    chars.count(c) > 1  
  end
end
_________________
def duplicate_count(text)
  text.downcase.chars.uniq.count{|c| text.downcase.count(c) > 1}
end
___________________
def duplicate_count(text)
    #your code here
    duplicateHash = {} of String => Int32
  
    text.downcase.chars.each { |char|
    puts "char: #{char}"
    if duplicateHash.has_key?(char.to_s)  #returns value : nil instead of true : false
        duplicateHash[char.to_s] += 1
    else
      duplicateHash[char.to_s] = 1
    end
    }
  rHash = duplicateHash.select {|k, v| v > 1}  
  return rHash.size
end
