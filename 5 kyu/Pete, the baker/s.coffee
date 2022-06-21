525c65e51bf619685c000059


cakes = (r, a) -> Math.min ((a[x] ? 0) // y for x, y of r)...
________________________________
cakes = (recipe, available) ->
  ingredients = Object.keys(recipe)
  if ingredients.every((x) -> Object.keys(available).includes(x)) then Math.min(ingredients.map((x) -> available[x] // recipe[x])...) else 0
________________________________
cakes = (recipe, available) ->
  return Math.floor Math.min Object.keys(recipe).map((ingredient) -> (available[ingredient] or 0) / recipe[ingredient])...
________________________________
cakes = (needs, has) ->
  Object.keys(needs).reduce((acc, key) ->
    Math.min (Math.floor (has[key] / needs[key]) or 0), acc
  , Infinity)
