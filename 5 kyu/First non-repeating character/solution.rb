def  first_non_repeating_letter(s) 
  s.chars.find {|i| s.downcase.count(i)==1 || s.upcase.count(i)==1} || ""
end
_______________________________________________
def  first_non_repeating_letter(s) 
  s.each_char do |char|
    return char if s.downcase.count(char.downcase) < 2
  end
  ""
end
_______________________________________________
def  first_non_repeating_letter(s)
  s.chars.each_with_object(Hash.new(0)) { |l, frq| frq[l.downcase] += 1 }.each { |l, c|  return s[s=~/#{l}/i] if c == 1 }
  ""
end
_______________________________________________
def  first_non_repeating_letter(s)
  letter = s.downcase.chars.find { |c| s.downcase.count(c) == 1 }
  s[/#{letter}/i]
end
_______________________________________________
def first_non_repeating_letter(s)
    str = s.downcase
    str.each_char.with_index do |v, i|
        if str.index(v) == str.rindex(v)
            return s[i]
        end
    end
    ""
end
