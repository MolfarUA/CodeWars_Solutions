5ab6538b379d20ad880000ab



def area_or_perimeter(l , w):
    return l * w if  l == w else (l+w)*2
###########
area_or_perimeter = lambda a, b : a * b if a == b else 2 * (a + b)
##########
def area_or_perimeter(l , w):
    if l == w:
        tot = l * w
    else:
        tot = l * 2 + w * 2
    return tot
##########
def area_or_perimeter(l , w):
    return l*w if l==w else l+l+w+w
###########
def area_or_perimeter(l , w):
    if l == w:
        return l * l
    else:
        return (w * 2) + (l * 2)
###########
def area_or_perimeter(length, width):
    if length  == width:
        return length * length
    else:
        return 2 * (length + width)
###########
def area_or_perimeter(l , w):
    return [(2*l+2*w),(w*w)][l==w]
#########
def area_or_perimeter(l , w):
    solucion = 0
    if(l == w):
        '''Area Cuadrado'''
        solucion = l * w
    else:
        '''Perimetro del Rectangulo'''
        solucion = 2 * (l + w)
    return solucion
###################
area_or_perimeter = lambda l , w: (l + w) * 2 if not l == w else w * l
###################
def area_or_perimeter(l , w):
    if l==w:
        s=l*l
    else:
        s=2*(l+w)
    return s
###################
def area_or_perimeter(l , w):
    if l * w == w * w:
            return l * w
    else: 
        z = (l*2) + (w*2)
        return z
###################
def area_or_perimeter(l , w):
    if l == w:
        rez = l*w
    else: 
        rez = 2 *(l+w)
    return rez
###################
def area_or_perimeter(l , w):
  result = 0;
  if (l == w):
    result = l * w;
  else:
    result = (2 * l) + (2 * w);
  return result;
