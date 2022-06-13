def find_it(seq)
  seq.detect { |n| seq.count(n).odd? }
end
_______________________________
def find_it(seq)
  seq.reduce(:^)
end
_______________________________
def find_it(seq)
  seq.uniq.each do |val|
    return val if seq.count(val).odd?
  end
end
_______________________________
def find_it(seq)
  seq.find{|c| seq.count(c).odd? }
end
_______________________________
def find_it(seq)
  seq.each do |i|
    if seq.count(i) % 2 != 0
      return i
    end
  end
end
_______________________________
def find_it(seq)
  seq.uniq.each{|x| return x if seq.count(x).odd?}
end
