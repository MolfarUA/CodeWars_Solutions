pred = (s) ->
  s == 'needle'

findNeedle = (haystack) ->
  'found the needle at position ' + haystack.findIndex(pred)
________________________
findNeedle = (haystack) ->
  return "found the needle at position #{haystack.indexOf('needle')}"
________________________
findNeedle = (haystack) ->
  "found the needle at position #{haystack.indexOf('needle')}"
________________________
findNeedle = (s) ->
  i = 0
  for val,key in s
    if val == 'needle'
      return 'found the needle at position ' + key
________________________
findNeedle = (haystack) ->
  j = 0
  i = 0
  while i < haystack.length
    if haystack[i] == 'needle'
      j = i
      break
    i++
  'found the needle at position ' + j
