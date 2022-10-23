583203e6eb35d7980400002a


countSmileys = (arr) ->
  arr.reduce ((a, b) ->
    a + /[:;][-~]?[)D]/.test(b)
  ), 0
__________________________
countSmileys = (a) -> (a.filter (c) -> /[:;][~-]?[)D]/.test(c)).length
__________________________
countSmileys = (arr) ->
  arr.filter((x) -> /^[:;][-~]?[\)D]/.test(x)).length
