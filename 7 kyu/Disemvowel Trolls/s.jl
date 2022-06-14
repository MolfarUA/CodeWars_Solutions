function disemvowel(str)
  replace(str, r"[aeiou]"i => "")
end
______________________________
function disemvowel(str)
  filter(char -> char ∉ "aeiouAEIOU", str)
end
______________________________
function disemvowel(str)
  str=replace(str,"a"=>"");str=replace(str,"A"=>"")
  str=replace(str,"e"=>"");str=replace(str,"E"=>"")
  str=replace(str,"i"=>"");str=replace(str,"I"=>"")
  str=replace(str,"o"=>"");str=replace(str,"O"=>"")
  str=replace(str,"u"=>"");str=replace(str,"U"=>"")
  return str
end
______________________________
function disemvowel(str)
  return join(filter(c->lowercase(c) ∉ ["a", "e", "i", "o", "u"], split(str, "")), "")
end
______________________________
# Trolls are attacking your comment section! A common way to deal with this
# situation is to remove all of the vowels from the trolls' comments,
# neutralizing the threat. Your task is to write a function that takes a string
# and return a new string with all vowels removed. For example, the string
# "This website is for losers LOL!" would become "Ths wbst s fr lsrs LL!".
# Note: for this kata y isn't considered a vowel.

function disemvowel(str)

  vowels = ['a','e','i','o','u','A','E','I','O','U']
  res_str = ""
  for s in str
    if (length( findall( x -> x == s, vowels )) != 0)
      continue
    end
    res_str = res_str * string(s)
  end
  return res_str
end
