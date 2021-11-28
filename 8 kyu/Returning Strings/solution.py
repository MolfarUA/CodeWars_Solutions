def greet(name):
    print(f"Hello, {name} how are you doing today?")
    return f"Hello, {name} how are you doing today?"

greet('1234567')
#############
def greet(name):
    return f'Hello, {name} how are you doing today?'
##############
greet = "Hello, {0} how are you doing today?".format
#############
def greet(name):
    return "Hello, {} how are you doing today?".format(name)
##############
def greet(name):
    return "Hello, " + name + " how are you doing today?"
#############
def greet(name):
    return "Hello, %s how are you doing today?" % name
#############
greet = lambda name: "Hello, %s how are you doing today?" % name
###########
import unittest

def greet(name):
    return "Hello, {} how are you doing today?".format(name)
    
class TestGreet(unittest.TestCase):
    def test_greet(self):
        name = 'Ryan'
        actual = greet(name)
        self.assertEqual(actual, "Hello, Ryan how are you doing today?")
#####################
def greet(name):
    return "Hello, %s how are you doing today?" % str(name)
###############
def greet(name):
    return "Hello, %s how are you doing today?" % (name)
print(greet("Bob"))
##################
def greet(name):
    assert isinstance(name, str)
    return f"Hello, {name} how are you doing today?"
###############
def greet(name):
    return 'Hello, ' + name + ' how are you doing today?' if name else None
#################
def greet(name):
    x = 'Hello, {} how are you doing today?'
    return x.format(name)
###############
def greet(name):
    m="Hello, %s how are you doing today?"
    return m%name
##################
def greet(name):
    main_string = "Hello, <name> how are you doing today?"
    parse_string = main_string.split("<name>")
    parse_string = name.join(parse_string)
    return parse_string
###############
def greet(name):
    s= "Hello, "
    r= name 
    f= " how are you doing today?"
    return s +r+f
################
def greet(name):
    return (f"Hello, {name} how are you doing today?")
print(greet("Marian"))
################
def greet(name):
    if name !=0:
        a = name
        b = "Hello, "
        c = " how are you doing today?"
        return b+a+c
    pass
#################
def main(): 
    name =  input("Hi, what is your name?")
    #name = "Ryan"
    #name = "Shingles"
    greet(name)

def greet(name):
    return "Hello, " + name + " how are you doing today?"

if __name__ == "__main__": 
    main()
