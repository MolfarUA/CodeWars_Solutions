toCamelCase = (str) ->
  str.replace /(-|_)./g, (x) -> x[1].toUpperCase()
________________________
toCamelCase = (s) -> s.replace(/[_-](.)/g, (x)->x[1].toUpperCase())
________________________
toCamelCase = (str) ->
  if str.length == 0
    return str;
  
  return str
    .split(/[-_]+/g)
    .map((word, i) => ( if i > 0 then word[0].toUpperCase() else word[0]) + word.substring(1))
    .join('')  
________________________
toCamelCase = (str) ->
  arr=str.split(/[-_]/g)
  return arr.shift()+arr.map((x)->x[0].toUpperCase()+x.slice(1).toLowerCase()).join("")
________________________
toCamelCase = (s) -> s.replace(/(-|_)(\w)/g,([a,b])->b.toUpperCase '')
________________________
toCamelCase = (str) -> (
  algorithm = (splitOn) -> str.split(splitOn)[0]+str.split(splitOn)[1..-1].map((substr) -> substr[0].toUpperCase()+substr[1..-1]).join("")
  algorithm(if "-" in str then "-" else "_")
)
