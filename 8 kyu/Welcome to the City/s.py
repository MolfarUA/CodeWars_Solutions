def say_hello(name, city, state):
    return "Hello, {}! Welcome to {}, {}!".format(" ".join(name), city, state)
_______________________________________
def say_hello(name, city, state):
    return f"Hello, {' '.join(name)}! Welcome to {city}, {state}!"
_______________________________________
def say_hello(name, city, state):
    return 'Hello, %s! Welcome to %s, %s!' % (' '.join(name), city, state)
_______________________________________
def say_hello(name, city, state):
    if len(name) == 2:
        return(f'Hello, {name[0].title()} {name[1].title()}! Welcome to {city.title()}, {state.title()}!')
    elif len(name) == 3:
          return(f'Hello, {name[0].title()} {name[1]} {name[2].title()}! Welcome to {city.title()}, {state.title()}!')
    elif len(name) == 4:
          return(f'Hello, {name[0].title()} {name[1].title()} {name[2].title()} {name[3].title()}! Welcome to {city.title()}, {state.title()}!')
_______________________________________
def say_hello(name: list, city: str, state: str) -> str:
    full_name = " ".join(name)
    return f"Hello, {full_name}! Welcome to {city}, {state}!"
_______________________________________
def say_hello(name, city, state):
    stra = " ".join(map(str,name))
    return f'Hello, {stra}! Welcome to {city}, {state}!'
_______________________________________
def say_hello(names, city, state):
    result = " ".join(names)
    return f"Hello, {result}! Welcome to {city}, {state}!"
_______________________________________
def say_hello(name, city, state):
    if len(name) == 1:
        return 'Hello, {}! Welcome to {}, {}!'.format(name[0], city, state)
    elif len(name) == 2:
        return 'Hello, {} {}! Welcome to {}, {}!'.format(name[0], name[1], city, state)
    elif len(name) == 3:
        return 'Hello, {} {} {}! Welcome to {}, {}!'.format(name[0], name[1],name[2], city, state)
    elif len(name) == 4:
        return 'Hello, {} {} {} {}! Welcome to {}, {}!'.format(name[0], name[1],name[2],name[3], city, state)
_______________________________________
def say_hello(name, city, state):
    first_last_name = ''
    for x in name:
        first_last_name += x + ' '
    return 'Hello, ' + first_last_name.strip() + '! Welcome to ' + city + ', ' + state + '!'
