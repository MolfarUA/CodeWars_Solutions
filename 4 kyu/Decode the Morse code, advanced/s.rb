54b72c16cd7f5154e9000457


def decodeBits(bits)
  bits = bits.sub(/^0+/, '').sub(/0+$/, '')
  bitlen = bits.scan(/0+|1+/).map(&:size).min
  bits.split('0' * 7 * bitlen).map { |wd|
    wd.split('0' * 3 * bitlen).map { |ch|
      ch.split('0' * bitlen).map { |b|
        b.size > bitlen ? '-' : '.'
      }.join
    }.join(' ') 
  }.join('   ')
end

def decodeMorse(morseCode)
  morseCode.strip.split('   ').map { |w| w.split(' ').map { |c| MORSE_CODE[c] }.join }.join ' '
end
_____________________________
def decodeBits(bits)
  bits.gsub!(/^0+|0+$/, '')
  t = bits.scan(/1+|0+/).map { |x| x.length }.min
  bits.gsub(/0{#{t*7},}/, '   ')
      .gsub(/1{#{t*3},}/, '-')
      .gsub(/1{#{t},#{t*2}}/, '.')
      .gsub(/0{#{t*3},}/, ' ')
      .gsub(/0{#{t}}/, '')
end

def decodeMorse(morseCode)
  morseCode.split('   ').map { |word| word.split.map { |x| MORSE_CODE[x] }.join }.join(' ')
end
_____________________________
def decodeMorse(morseCode)
  morseCode.strip.split("   ").map do |word|
    word.split(" ").map do |character|
      MORSE_CODE.fetch(character)
    end.join
  end.join(" ")
end

SYMBOLS = {
  "1" => ".",
  "111" => "-",
  "0" => "",
  "000" => " ",
  "0000000" => "   ",
}

def decodeBits(morse)
  morse = morse.gsub(/^0+/, "")
  morse = morse.gsub(/0+$/, "")
  symbols = morse.scan(/0+|1+/)
  dit_time = symbols.map(&:length).min
  symbols.map do |symbol|
    symbol_time = symbol.length / dit_time
    symbol = symbol[0] * symbol_time
    SYMBOLS.fetch(symbol)
  end.join
end
