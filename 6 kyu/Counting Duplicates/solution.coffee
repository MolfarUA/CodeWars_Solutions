duplicateCount = (text) ->
  text = text.toLowerCase()
  Array.from(new Set(text)).filter((x) -> text.indexOf(x) != text.lastIndexOf(x)).length
______________________
duplicateCount = (text) ->
  text = text.toLowerCase().split ''
  dict = {}
  count = 0
  for l in text
    unless dict[l]?
      dict[l] = 0
    if dict[l] is 1
      count += 1
    dict[l] += 1
  count
  
______________________
duplicateCount = (text) ->
  text = text.split ''
  dict = {}
  count = 0
  for l in text
    l = l.toLowerCase()
    unless dict[l]?
      dict[l] = 0
    if dict[l] is 1
      count += 1
    dict[l] += 1
  count
  
____________________
duplicateCount = (text) ->
  duplicatesCount = 0
  countMap = {}

  for c in text.toLowerCase()
    if typeof countMap[c] != "number"
      countMap[c] = 1
    else
      countMap[c] += 1

  for char, count of countMap
    ++duplicatesCount if count > 1

  duplicatesCount
  
___________________
duplicateCount = (text) ->
  (text.toLowerCase().split('').sort().join('').match(/(.+)\1/g) || []).length
