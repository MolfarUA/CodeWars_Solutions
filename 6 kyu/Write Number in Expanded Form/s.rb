5842df8ccbd22792a4000245


def expanded_form(num)
  num.to_s
     .chars
     .reverse
     .map.with_index { |d, idx| d.to_i * 10**idx }
     .reject(&:zero?)
     .reverse
     .join (' + ')
end
_________________________
def expanded_form(num)
  num.to_s.chars.reverse.map.with_index{|i,j| i == "0" ? nil : i + "0" * j }.compact.reverse.join(" + ")
end
_________________________
def expanded_form(num)
 num.digits
    .map
    .with_index {|i, idx| i * 10**idx}
    .reject(&:zero?)
    .reverse
    .join(' + ')
end
