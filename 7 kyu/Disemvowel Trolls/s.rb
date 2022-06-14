def disemvowel(str)
  str.delete('aeiouAEIOU')
end
______________________________
def disemvowel(str)
  str.gsub /[aeiou]/i, ''
end
______________________________
def disemvowel(str)
  vowels = 'aouei'
  str.delete(vowels + vowels.upcase)
end
______________________________
def disemvowel(str)
  str.tr('aeouiAEOUI', '')
end
______________________________
def disemvowel(str)
  str_arr = str.split("")
  vowels = "aeiou"
  result = []
  
  str_arr.each do |ele|
  if !vowels.include?(ele.downcase)
  result << ele
  end
  end
  return result.join
end
