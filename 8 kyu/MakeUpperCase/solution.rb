def make_upper_case(string)
  string.upcase
end
_____________________________________________
define_method :make_upper_case, &:upcase
_____________________________________________
def make_upper_case(str)
   upper = str.upcase
   upper
end
_____________________________________________
def make_upper_case(str) str.upcase end
_____________________________________________
def make_upper_case(str)
  str.bytes.map{|c| (97..122).include?(c) ? (c - 32).chr : c.chr}.join
end
_____________________________________________
def make_upper_case(str)
  # Code here
#   upcased = []
#   str.split.each do |letter|
#     if letter =~ (/^\s*$/)
#       upcased << letter
#     else
#       upcased << letter.upcase
#     end
#   end 
#   upcased.join("\s")
    str.upcase
end
