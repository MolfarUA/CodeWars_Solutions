def find_it(seq)
  seq
  .each
  .skip_while {|i| seq.count(i).even?}
  .first
end
_______________________________
def find_it(seq)
  seq.reduce(0) {|a, b| a ^ b}
end
_______________________________
def find_it(seq)
  seq.uniq.each { |x| return x if seq.count(x).odd? }
end
_______________________________
def find_it (seq)
  hash = {} of Int32 => Int32

  seq.each() do |key|
    hash[key] = hash.fetch(key, 0) + 1
  end

  hash.each() do |key, value|
    if value % 2 != 0
      return key
    end
  end

  return nil
end
_______________________________
def find_it(seq)
  seq.reduce{ |x, y| x ^ y }
end
