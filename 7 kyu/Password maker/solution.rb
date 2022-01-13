def make_password(phrase)
  phrase.split.map { |w| w[0] } .join.tr("IOSios", "105105")
end
__________________________________
CONFIG = {'o' => '0', 'O' => '0', 
          'i' => '1', 'I' => '1', 
          's' => '5', 'S' => '5', }

def make_password(phrase)
    phrase.split(' ').map{|s| s[0]}.join.gsub(/[iIoOsS]/,CONFIG)
end
__________________________________
def make_password(phrase)
  phrase.split.map { |s| s[0] }.join.tr('iIoOsS', '110055')
end
__________________________________
def make_password(phrase)
  pw = phrase.split(/\s+/).map{|s| s[0]}.join
  pw.gsub! /i/i, '1'
  pw.gsub! /o/i, '0'
  pw.gsub! /s/i, '5'
  pw
end
__________________________________
def make_password(phrase)
  firsts = []
  phrase.split.each do |word|
      firsts << word[0]
    end
  return firsts.join.gsub(/[iIoOsS]/, "i" => "1", "I" => "1", "o" => "0", "O" => "0", "s" => "5", "S" => "5")
end
__________________________________
def make_password(phrase)
  phrase.split.map{|m| m[0]}.join.tr 'iIoOsS','110055'
end
