526a569ca578d7e6e300034e


def convert(input, source, target)
  value = input.chars.reduce(0) do |s, c|
    source.size * s + source.index(c)
  end
  res = ''
  while value >= 0
    res = target[value % target.size] + res
    value = value < target.size ? -1 : value/target.size
  end
  res
end
__________________________________________
def convert(input, source, target)
  return input if source == target

  source_base = source.size
  target_base = target.size
  characters = input.reverse.each_char.with_index

  decimal = characters.reduce(0) do |sum, (character, index)|
    sum + (source_base ** index) * source.index(character)
  end

  result = ""
  loop do
    decimal, index = decimal.divmod(target_base)
    result << target[index]

    break if decimal.zero?
  end

  result.reverse
end
__________________________________________
def convert(input, source, target)
    return target[0] if input == source[0]
    
    s = ''
    input = to_int(input, source)
    b = target.length
    
    until input == 0
        s = target[input % b] + s
        input /= b
    end
    
    s
end

def to_int(input, source)
    b = source.length 
    input.reverse.each_char.with_index.reduce(0){|sum, (c, i)| sum + source.index(c) * b ** i}
end

