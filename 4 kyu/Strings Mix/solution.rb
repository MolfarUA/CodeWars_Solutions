def mix(s1, s2)
  selection = ('a'..'z').to_a.select { |letter| s1.count(letter) > 1 || s2.count(letter) > 1 }
  selection.map! do |selection| 
    if s1.count(selection) > s2.count(selection)
      "1:#{selection * s1.count(selection)}"
    elsif s1.count(selection) < s2.count(selection)
      "2:#{selection * s2.count(selection)}"
    else
      "=:#{selection * s1.count(selection)}"
    end
  end
  selection.sort_by { |x| [-x.size, x[0], x[-1]] }.join("/")
end

_____________________________________________________
def mix(s1, s2)
  (s1 + s2).scan(/[a-z]/).uniq.map { |char|
    [char, [s1.count(char), s2.count(char)]]
  }.select { |_, counts|
    counts.max > 1
  }.map { |char, (s1_count, s2_count)|
    case s1_count <=> s2_count
    when  1 then "1:#{char * s1_count}"
    when  0 then "=:#{char * s1_count}"
    when -1 then "2:#{char * s2_count}"
    end
  }.sort_by { |string|
    [-string.length, string]
  }.join("/")
end
      
_____________________________________________________
def mix a, b
  ("a".."z").to_a.select{ |letter| a.count(letter) > 1 || b.count(letter) > 1 }.map{ |letter|
    if a.count(letter) > b.count(letter)
      "1:#{letter * a.count(letter)}" 
    elsif b.count(letter) > a.count(letter)
      "2:#{letter * b.count(letter)}"
    else
      "=:#{letter * a.count(letter)}"
    end
  }.sort_by{|h| [-h.size, h[0], h[-1]] }.join("/")
end
