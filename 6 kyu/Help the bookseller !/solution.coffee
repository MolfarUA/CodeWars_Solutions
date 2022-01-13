stockList = (listOfArt, listOfCat) ->
  return '' if listOfArt.length is 0 or listOfCat.length is 0
  
  quantities = listOfArt.reduce (obj, art) ->
    [key, quantity] = art.split(' ')
    obj[key[0]] ?= 0
    obj[key[0]] += parseInt quantity
    obj
  , {}
    
  results = for category in listOfCat
    "(#{category} : #{quantities[category] ? 0})"
    
  results.join(' - ')
________________________________________
stockList = (listOfArt, listOfCat) ->
  if listOfArt.length && listOfCat.length then listOfCat.map((x) -> "(#{x} : #{listOfArt.reduce(((sum, y) -> sum + (if y[0] == x then +y.split(' ')[1] else 0)), 0)})").join(' - ') else ''
________________________________________
stockList = (listOfArt, listOfCat) ->
  if listOfArt.length == 0 or listOfCat.length == 0
    return ''
  dict = listOfArt.reduce(((d, book) ->
    fstletter = book[0]
    if !d[fstletter]
      d[fstletter] = 0
    d[fstletter] += parseInt(book.split(' ')[1], 10)
    d
  ), {})
  listOfCat.map((cat) ->
    '(' + cat + ' : ' + (dict[cat] or 0) + ')'
  ).join ' - '
________________________________________
stockList = (a, c) ->
  if a.length == 0 || c.length == 0
    return ""
  return c.map (_c) ->
    sum = a.filter (_a) ->
      _a.startsWith(_c)
    .map (_a) ->
      Number(_a.split(' ')[1])
    .reduce (a, b) ->
      a + b
    , 0
    return "(" + _c + " : " + sum + ")"
  .join(" - ")
________________________________________
stockList = (bks, cats) ->
  if !bks.length or !cats.length then return '' else stock = cats.map (c) ->
    "(#{c} : #{bks.filter((b) -> b[0] == c).reduce ((t, b) -> t + +b.split(' ')[1]), 0})"
  stock.join ' - '
________________________________________
stockList = (books, cats) ->
  if !books.length then '' else
    cats.map (c) ->
      count = books.filter((b) -> b[0] == c).map (b) -> +b.split(' ')[1]
      "(#{c} : #{if count.length then count.reduce (a, b) -> a + b else 0})"
    .join ' - '
