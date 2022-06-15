def fake_bin(s)
  s.gsub(/[0-4]/,'0').gsub(/[5-9]/, '1')
end
__________________________________
def fake_bin(s)
  newBin = ""
  arr = s.split("")
  arr.each { |x| newBin += x.to_i < 5 ? "0" : "1"} 
  newBin
end
__________________________________
def fake_bin(s)
  s.split(%r{\s*}).map do |x|
    x = x.to_i
   if x  < 5
     x = 0
   else
     x = 1
   end 
  end.join
end
__________________________________
def fake_bin(s)
  s.split("").map {|k| k.to_i<5 ? '0' : '1' }.join
end
