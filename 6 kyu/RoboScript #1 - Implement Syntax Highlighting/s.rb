58708934a44cfccca60000c4


def highlight(code)
  code.gsub(/F+|\d+|R+|L+/) do |match|
    case match
    when /F+/
      "<span style=\"color: pink\">#{match}</span>"
    when /L+/
      "<span style=\"color: red\">#{match}</span>"
    when /R+/
      "<span style=\"color: green\">#{match}</span>"
    when /\d+/
      "<span style=\"color: orange\">#{match}</span>"
    end
  end
end
__________________________
def highlight(code)
  code.gsub(/(F+)/)     { |m| span(m, 'pink') }
      .gsub(/(L+)/)     { |m| span(m, 'red') }
      .gsub(/(R+)/)     { |m| span(m, 'green') }
      .gsub(/([0-9]+)/) { |m| span(m, 'orange') }
end

def span(input, color)
  "<span style=\"color: #{color}\">#{input}</span>"
end
__________________________
def highlight code
    code.gsub(/\d+/){|c| "<span style=\"color: orange\">#{c}</span>"}
        .gsub(/R+/){|c| "<span style=\"color: green\">#{c}</span>"}
        .gsub(/F+/){|c| "<span style=\"color: pink\">#{c}</span>"}
        .gsub(/L+/){|c| "<span style=\"color: red\">#{c}</span>"}
end
__________________________
def highlight(code)
  s_F_pink = "<span style=\"color: pink\">"
  s_L_red = "<span style=\"color: red\">"
  s_R_green = "<span style=\"color: green\">"
  s_09_orange = "<span style=\"color: orange\">"
  s_end = "</span>"
  i = 0
  str = String.new
  
  while i < code.size
    case code.chars[i]
    when 'F'
      unless (i > 0 && code.chars[i-1] == 'F')
        str += s_end if (i > 0 && code.chars[i-1].match(/[\(|\)]/).nil?)
        str += s_F_pink
      end
    when 'L'
      unless (i > 0 && code.chars[i-1] == 'L')
        str += s_end if (i > 0 && code.chars[i-1].match(/[\(|\)]/).nil?)
        str += s_L_red
      end
    when 'R'
      unless (i > 0 && code.chars[i-1] == 'R')
        str += s_end if (i > 0 && code.chars[i-1].match(/[\(|\)]/).nil?)
        str += s_R_green
      end
    when '0'..'9'
      unless (i > 0 && !code.chars[i-1].match(/[0-9]/).nil?)
        str += s_end if (i > 0 && code.chars[i-1].match(/[\(|\)]/).nil?)
        str += s_09_orange
      end
    when '(', ')'
      unless (i > 0 && !code.chars[i-1].match(/[\(|\)]/).nil?)
        str += s_end if (i > 0 && code.chars[i-1].match(/[\(|\)]/).nil?)
      end
    end      
    str += code.chars[i]
    i += 1
  end
  str += s_end if (i > 0 && !(code.chars[i-1].match(/[\(|\)]/)))
end
