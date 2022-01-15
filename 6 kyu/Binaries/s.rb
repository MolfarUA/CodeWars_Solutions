def code(strng)
    dict = ['10', '11', '0110', '0111', '001100', '001101', '001110', '001111', '00011000', '00011001']
    strng.chars.map { |c| dict[c.to_s.to_i]}.join("")
end

def decode(str)
    ret = ""
    i = 0
    lg = str.length
    while (i < lg) do 
        zero_i = i
        while ((zero_i < lg) && (str[zero_i] != '1')) do
            zero_i += 1
        end
        l = zero_i - i + 2
        ss = str[zero_i + 1..zero_i + l - 1]
        ret += ss.to_i(2).to_s(10)
        i = zero_i + l
    end
    ret
end
__________________________
def code(strng)
  return "" if strng.size == 0
  num = strng[0].to_i.to_s(2)
  "0" * (num.size - 1) + "1" + num + code(strng[1..-1])
end


def decode(str)
  return "" if str.size == 0
  count = 0
  while str[0] == '0'
    count += 1
    str = str[1..-1]
  end
  num = str[1..count + 1]
  num.to_i(2).to_s + decode(str[count + 2..-1])
end
__________________________
DECODE = {'10'=> 0, '11'=> 1, '0110'=> 2, '0111'=> 3, '001100'=> 4, '001101'=> 5, 
          '001110'=> 6,'001111'=> 7, '00011000'=> 8, '00011001'=> 9}

def code(str)
  str.chars.map {|n| '0' * (n.to_i.to_s(2).size - 1) + '1' + n.to_i.to_s(2)}.join('')
end

def decode(str)
  str.scan(/#{DECODE.keys.join('|')}/).map {|encoded_digit| DECODE[encoded_digit]}.join('')
end
__________________________
$CODES = %w[10 11 0110 0111 001100 001101 001110 001111 00011000 00011001]
def code(strng)
  strng.chars.map{|c| $CODES[c.to_i]}.join
end

def decode(str)
  str.scan(/#{$CODES.join('|')}/).map{|c| $CODES.index(c)}.join
end
__________________________
def code s
  s.each_char.map{|d| '0'*(s=d.to_i.to_s(2);s.size-1)+'1'+s}.join
end

H=('0'..'9').map{|d| [code(d),d]}.to_h
R=Regexp.new(H.keys.join'|')

def decode s
  s.gsub(R){H[$&]}
end
__________________________
def code(strng)
  strng.chars.map { |x| "0"*((b = x.to_i.to_s(2)).chars.count - 1) + "1" + b }.join
end

def decode(str)
  code_arr = []
  while str.include?("1")
    g = str.slice!(0, (str.index("1") + 1) * 2)
    code_arr << (g.slice((g.length/2), g.length)).to_i(2)
  end
  code_arr.join
end
__________________________
def code(str)
  str.chars.map { |c| "0" * ((b = c.to_i.to_s(2)).length - 1) + "1" + b }.join
end

def decode(str)
  dec = ""
  while str != ""
    len = str.match(/^0*1/)[0].length
    dec += str[len...len+len].to_i(2).to_s
    str = str[len+len..-1]
  end
  dec
end
