createPhoneNumber = (numbers) ->
  "(###) ###-####".replace /#/g, -> numbers.shift()
_______________________________
createPhoneNumber = (numbers) ->
  num = [[0..2], [3..5], [6..9]].map (range) ->
    (range.map (r) -> numbers[r]).join ''
  
  "(#{num[0]}) #{num[1]}-#{num[2]}"
_______________________________
createPhoneNumber = (numbers) ->
  x = numbers.toString(numbers).replace(/,/g, "")
  return "(" + x.substr(0, 3) + ") " + x.substr(3, 3) + "-" + x.substr(6, 4)
_______________________________
createPhoneNumber = (n) ->
  "(#{n[0..2].join('')}) #{n[3..5].join('')}-#{n[6..10].join('')}"
_______________________________
createPhoneNumber = (s) ->
  s = s.join ''
  "(#{s[0..2]}) #{s[3..5]}-#{s[6..9]}"
