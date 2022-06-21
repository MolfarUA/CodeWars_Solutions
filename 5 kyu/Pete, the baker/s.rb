525c65e51bf619685c000059


def cakes(recipe, available)
  recipe.collect { | k, v | available[k].to_i / v }.min
end
________________________________
def cakes(recipe, available)
  result = []

  return 0 if recipe.keys.count > available.keys.count
  
  recipe.each do |ingredient, amount|
    if (available[ingredient])
      result << (available[ingredient]/ amount)
    else
      result << 0
    end
  end
  
  result.min
end
________________________________
def cakes(recipe, available)
  recipe
    .map { |(ingredient, qnty)| (available[ingredient] || 0) / qnty }
    .min
end
