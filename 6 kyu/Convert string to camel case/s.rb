def to_camel_case(str)
  str.gsub(/[_-](.)/) {"#{$1.upcase}"}
end
________________________
def to_camel_case(str)
  str.gsub('_','-').split('-').each_with_index.map{ |x,i| i == 0 ? x : x.capitalize }.join
end
________________________
def to_camel_case(str)
  head, *tail = str.split(/[-_]/)
  head.to_s + tail.map(&:capitalize).join
end
________________________
def to_camel_case(str)
  
  phrase = str.include?('_') ? str.split('_') : str.split('-')
  
  phrase.map.with_index do |word, index|
    index == 0 ? word : word.capitalize
  end.join('')

end
________________________
def to_camel_case(str)
  str.gsub(/([\-_][a-zA-Z])/) do |m|
   m[1].upcase
  end
end
