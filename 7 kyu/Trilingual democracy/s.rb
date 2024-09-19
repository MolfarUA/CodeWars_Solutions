def trilingual_democracy(group)
  group.chars.map(&:ord).reduce(:^).chr
end
________
def trilingual_democracy(group)
  group.bytes.reduce(:^).chr
end
___________
def first_unique_value(array)=
  array.each { |g| return g if array.count(g) == 1}
  
GROUPS = ['D', 'F', 'I', 'K']

def trilingual_democracy(group)
  group = group.split('')
  return group.first               if group.uniq.size == 1
  return first_unique_value(group) if group.uniq.size == 2
  return (GROUPS - group).first    if group.uniq.size == 3
end

______________
# input is a string of three chars from the set 'D', 'F', 'I', 'K'
# output is a single char from this set
def trilingual_democracy(group)
  all_languages = 'DFIK'
  langs = group.chars 
  case langs.uniq.size
    when 3 then all_languages.delete(group)
    when 2 then langs.min_by {|lang| langs.count(lang)}
    when 1 then langs.first
    else raise ArgumentError, "Something went wrong"
  end
end
