55225023e1be1ec8bc000390


def greet(name):
    if name == "Johnny":
        return "Hello, my love!"
    return "Hello, {name}!".format(name=name)
__________________________________
def greet(name):
    if name == "Johnny":
        return "Hello, my love!"
    else:
        return "Hello, {name}!".format(name=name)
__________________________________
def greet(name):
    return "Hello, my love!" if name == 'Johnny' else "Hello, {name}!".format(name=name)
__________________________________
def greet(name):
    
    if name =="Johnny":
        return "Hello, my love!"
    if name != "Johnny":
        return "Hello, {name}!".format(name=name)
__________________________________
def greet(name: str):
    if name == 'Johnny':
        return "Hello, my love!"
    else:
      return "Hello, {name}!".format(name=name)
__________________________________
def greet(name):
    x=' '
    if name == "Johnny":
        return "Hello, my love!"
    else:
        return "Hello,"+x+name+"!"
__________________________________
def greet(name):
    
    if name == "Johnny":
        name1="Hello, my love!";
        return name1;
    else :
        name1="Hello, "+name+"!";
        return name1;
__________________________________
def greet(name):
    if not(name == "Johnny"): return f"Hello, {name}!"
    else: return "Hello, my love!"
__________________________________
def greet(name):
    a = "Hello, " + name + "!"
    if name == "Johnny":
        return "Hello, my love!"
    return a
__________________________________
def greet(name):
    pass
def greet(name):
    
    if name =="Johnny":
        return "Hello, my love!"
    else:    
        return "Hello, {name}!".format(name=name)
