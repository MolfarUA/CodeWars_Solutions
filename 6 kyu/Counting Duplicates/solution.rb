def duplicate_count(text)
  ('a'..'z').count { |c| text.downcase.count(c) > 1 }
end

_____________________
def duplicate_count(text)
  arr = text.downcase.split("")
  arr.uniq.count { |n| arr.count(n) > 1 }
end
____________________
def duplicate_count(text)
  hsh = Hash.new(0)
  text.downcase.chars.each { |c| hsh[c] += 1 }
  hsh.values.count { |k| k > 1 }
end
___________________
def duplicate_count(text)
  text.downcase.chars.group_by(&:to_s).count { |_, v| v.count > 1 }
end
__________________
def duplicate_count(str)
    str.downcase.each_char.find_all { |c| str.downcase.count(c) > 1 }.uniq.size
end
