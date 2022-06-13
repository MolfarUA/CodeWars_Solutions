def parse(data):
    '''Returns a list according to the data input'''
    output = 0
    output_array = []
    for letter in data:
        if letter == 'i':
            output += 1
        elif letter == 'd':
            output -= 1
        elif letter == 's':
            output *= output
        elif letter == 'o':
            output_array.append(output) 
    return output_array
__________________________________________
def parse(data):
    value = 0
    res=[]
    for c in data:
        if c=="i": value+=1
        elif c=="d": value-=1
        elif c=="s": value*=value
        elif c=="o": res.append(value)
    return res
__________________________________________
def parse(data):
    arr = []
    value = 0
    for c in data:
        if c == "i":
            value += 1
        elif c == "d":
            value -= 1
        elif c == "s":
            value = value**2
        elif c == "o":
            arr.append(value)
    return arr
__________________________________________
def parse(data):
    action = {'i': lambda v, r: v + 1,
              'd': lambda v, r: v - 1,
              's': lambda v, r: v * v,
              'o': lambda v, r: r.append(v) or v}
    v, r = 0, []
    for a in data:
        v = action[a](v, r) if a in action else v
    return r
__________________________________________
class Deadfish:
    commands = {
        'i': lambda df: df.i(),
        'd': lambda df: df.d(),
        's': lambda df: df.s(),
        'o': lambda df: df.o()
    }

    def __init__(self):
        self.value = 0
        self.outputs = []

    def i(self): self.value += 1
    def d(self): self.value -= 1
    def s(self): self.value **= 2
    def o(self): self.outputs.append(self.value)

    def apply(self, command):
        try: Deadfish.commands[command](self)
        except KeyError: pass

def parse(commands):
    df = Deadfish()
    [df.apply(c) for c in commands]
    return df.outputs
__________________________________________
COMMANDS = {
    'i': lambda x: x + 1,
    'd': lambda x: x - 1,
    's': lambda x: x * x,
}

def parse(data):
    result, x = [], 0
    for c in data:
        if c == 'o':
            result.append(x)
        elif c in COMMANDS:
            x = COMMANDS[c](x)
    return result
__________________________________________
def parse(data):
    number = 0
    arr = []
    for i in data:
        if i in "idso":
            if i == "i":
                number += 1
            elif i == "d":
                number -= 1
            elif i == "s":
                number = number ** 2
            elif i == "o":
                arr.append(number)

    return arr
__________________________________________
def parse(data):
    val = 0
    output = []
    for x in data:
        if x == 'o':
            output.append(val)
        if x == 'i':
            val += 1
        if x == 'd':
            val -= 1
        if x == 's':
            val = val**2
    return output
__________________________________________
def parse(data):
    x=0
    arr=[]
    for a in data:
        if a=="i":
            x+=1
        if a=="d":
            x-=1
        if a=="s":
            x*=x
        if a=="o":
            arr.append(x)   
    return arr
__________________________________________
def parse(data):
    current = 0
    result = []
    for i in data:
        if i == 'i':
            current += 1
        elif i == 'd':
            current -= 1
        elif i == 's':
            current **= 2
        elif i == 'o':
            result.append(current)
            
    return result
__________________________________________
def parse(data):
    
    valor_inicial = 0
    mensagem = []
    
    for a in data :
        match a:
            case 'i':
                valor_inicial += 1
            case 'd':
                valor_inicial -= 1
            case 's':
                valor_inicial **= 2
            case 'o':
                mensagem.append(valor_inicial)
            case _:
                pass
            
    return mensagem
__________________________________________
def parse(data):
    data = "".join([i for i in data if i in "idso"])
    res = []
    val = 0
    for i in data:
        if i  == "i":
            val += 1
        elif i == "d":
            val -= 1
        elif i == "s":
            val *= val
        else:
            res.append(val)
    return res
__________________________________________
def parse(data):
    number = 0
    array = []
    for letter in data:
        match letter:
            case 'i':
                number += 1
            case 'd':
                number -= 1
            case 's':
                number **= 2
            case 'o':
                array.append(number)
            case _:
                pass
    return array
__________________________________________
def parse(data):
    num = 0
    result = []
    for k in data:
        if k == 'i':
            num += 1
        elif k == 'd':
            num -= 1
        elif k == 's':
            num = num ** 2
        elif k == 'o':
            result.append(num)
    return result
