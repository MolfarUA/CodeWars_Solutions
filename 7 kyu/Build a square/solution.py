59a96d71dbe3b06c0200009c


def generateShape(integer):
    return '\n'.join('+' * integer for i in range(integer))
_____________________________
def generate_shape(n: int) -> str:
    return '\n'.join(['+' * n] * n)
_____________________________
def generateShape(i):
    return (i-1)*(('+'*i)+'\n')+('+'*i)
_____________________________
def generateShape(n):
    string = ""
    for row in range(n):
        for col in range(n):
            string += '+'
        string += '\n'
    return(string[:-1])
_____________________________
def generate_shape(n):
    return "\n".join(["+"*n]*n)
_____________________________
generate_shape=lambda n:'\n'.join(['+'*n]*n)
_____________________________
def generate_shape(n):
    counter = 0
    list = []
    while counter < n:
        list.append('+'*n)
        counter += 1
    return "\n".join(list)
_____________________________
def generate_shape(n):
    shape = ''
    for i in range(n):
        shape += '+'
        for j in range(n-1):
            shape += '+'
        shape += '\n'
    return shape.strip()
_____________________________
def generate_shape(n):
    word = '+' * n
    return '\n'.join([word] * n)
