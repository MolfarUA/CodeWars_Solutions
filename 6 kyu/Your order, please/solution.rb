def order(words)
  words.split.sort_by{ |w| w[/\d/] }.join(' ')
end

_____________________________________________
def order(words)
  words.split.sort_by { |w| w.chars.min } .join(" ")
end

_____________________________________________
def order(str)
  h = Hash.new
  arr = Array.new
  str = str.split(' ')
  (0...str.size).each{|x|
    (0...str[x].size).each{|y|
      if str[x][y].to_i > 0 then
        h[str[x][y].to_i] = str[x]
      end
    }
  }
  h.each{|k, i|
    arr[k] = i
  }
  ret = arr.join(' ')
  ret[0] = ''
  ret
end
  
_____________________________________________
def order(words)
  words = words.split
  indexes = words.map { |i| i.gsub(/[a-zA-Z]/, "").to_i - 1 }
  rearranged_words = []
  indexes.size.times { |i| rearranged_words[indexes[i]] = words[i] }
  rearranged_words.join(" ")
end
  
_____________________________________________
def order(words)
  if words.empty?
    return ""
  end
  @final_table = []
  9.times {@final_table << ""}
  words_table = words.split(" ")
  words_table.each_with_index do |word, index|
    words_table.each do |ord_word|
      if ord_word.include?("#{index+1}")
        @final_table[index] = ord_word
      end
   end
  end
  @final_table = @final_table.reject {|f| f.empty?}
  @final_table.join(" ")
end
