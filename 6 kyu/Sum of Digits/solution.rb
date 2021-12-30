def digital_root(n)
  n < 10 ? n : digital_root(n.digits.sum)
end

________________________________
def digital_root(n)
  n < 10 ? n : digital_root(n / 10 + n % 10)
end

________________________________
def digital_root(n)
    num = n.to_s.split("")
    digit = []
    num.each do |number|
        digit << number.to_i
    end
    sum = 0
    digit.each{ |x| sum+=x }
    return sum if sum < 10
    digital_root(sum)
end

________________________________
# def digital_root(n)
#   # ...
# #   digits = n.to_s.split("").map(&:to_i)
# # #   digits.inject{ |sum, digit| 
# # #     0 + sum + digit
# # #   }
  
# #   puts ">>>>>>"
# #   puts digits.inspect
# #   puts ">>>>>>"
# #   digits.reduce(0, :+)
  
# #   sum = 0
# #   digits.each do |digit|
# #     sum += digit
# #     puts sum.inspect
# #   end
# #   sum
#   puts "\n n is: #{n}"
#   puts "\n n % 100 is: #{n % 100}"
#   n % 10
  
#   sum = 0
#   sum = n
#   while sum > 9 do
#     sum = sum.to_s.split.map(&:to_i).reduce(&:+)  
#   end
  
# #   sum = n.to_s.split.map(&:to_i).reduce(&:+)
# end

# def digital_root(n)
#   s = nil
#   temp = n
#   if sum_digits(n) < 10
#     s = sum_digits(n)
#   else
#     s = sum_digits
    
#   s = sum_digits(n) if sum_digits(n)  
# end






def digital_root(n)
  while(n >= 10) do 
    n = sum_digits(n)
  end
  n
end

private

def sum_digits(number)
  number.to_s.split('').map(&:to_i).reduce(0, :+)
end
