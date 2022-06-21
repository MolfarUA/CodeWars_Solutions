525c65e51bf619685c000059


def cakes(recipe, available):
    return min(available.get(k, 0)/recipe[k] for k in recipe)
________________________________
def cakes(recipe, available):
    try:
        return min([available[a]/recipe[a] for a in recipe])
    except:
        return 0
________________________________
def cakes(recipe, available):
    return min(available.get(k, 0) // v for k,v in recipe.iteritems())
________________________________
def cakes(recipe, available):
    list = []
    for ingredient in recipe:
        if ingredient in available:
            list.append(available[ingredient]/recipe[ingredient])
        else:
            return 0
    return min(list)
________________________________
def cakes(recipe, available):
    return min((available.get(k, 0) // v for k, v in recipe.items()))
________________________________
def cakes(recipe, available):
    res = []
    for k in recipe.keys():
        try: res.append(available[k] // recipe[k])
        except: return 0
    return min(res)
________________________________
def cakes(recipe, available):
    amount_per_ingredient = []
    for ingredient in recipe:
        if ingredient not in available or available[ingredient] < recipe[ingredient]:
            return 0
        else:
            amount_per_ingredient.append(available[ingredient] / recipe[ingredient])
    return min(amount_per_ingredient)
________________________________
def cakes(recipe, available):
    return min([available.get(ingredient)//recipe[ingredient] if available.get(ingredient) else 0 for ingredient in recipe])
________________________________
def cakes(recipe, available):
    maxCakes = []
    for ingredient in recipe.keys():
        try:
            maxCakes.append(int(available[ingredient]/recipe[ingredient]))
        except KeyError:
            return 0
    return min(maxCakes)
________________________________
def cakes(recipe, available):
    howmany=[]
    for key in recipe.keys():
        if key in available.keys():
            howmany.append(available[key]//recipe[key])
        else:
            return 0
    return min(howmany)
________________________________
def cakes(recipe, available):
    out = None
    for key in recipe.keys():
        if key not in available.keys():
            return 0
        amount = available[key] // recipe[key]
        if out is None or amount < out:
            out = amount
    return out
________________________________
def cakes(recipe, available):
    tab = [];
    for k, v in recipe.items():
        if k not in available:
            tab.append(0);
        else:
            tab.append(available[k]//recipe[k]);
    return min(tab)
