def f(a,b,c):
	return 3 * (a*b*c) + 2 * (a*b + b*c + a*c) + a+b+c
_____________________________________
def f(x,y,z):
    a,b,c = x+1, y+1, z+1
    return x*b*c + y*a*c + z*a*b
_____________________________________
def f(x,y,z): return x+(x+2)*y*z + y+(y+2)*x*z + z+(z+2)*x*y;
_____________________________________
def f(x,y,z):
    return x * (y + 1) * (z + 1) + (x + 1) * y * (z + 1) + (x + 1) * (y + 1) * z
_____________________________________
def f(x, y, z):
    a, b, c = x + 1, y + 1, z + 1
    return a*b*z + a*y*c + x*b*c
_____________________________________
def f(x, y, z):
    return x + y + z + 2 * (x * y + y * z + x * z) + 3 * x * y * z
_____________________________________
def f(x,y,z):
    return x + 2 * x * y + y + 2 * x * z + 3 * x * y * z + 2 * y * z + z
_____________________________________
def f(x,y,z):
    a = 3 * x + 1
    b = 2 * x * y + x + y
    return ((((8 * x + 4) - a) * y + a) - b) * z + b 
_____________________________________
def f(x,y,z):
    ### Calculate the number of lines parallel with x-axis. 
    ### Start with he "base". It has (y+1)*(z+1) lines. Then multiply "base" by number of "layers" which is x, to get the volume.
    xlines = x*(y+1)*(z+1)
    
    ### Do the same for lines parallel with y and z axis.
    ylines = (x+1)*y*(z+1)
    zlines = (x+1)*(y+1)*z
    
    # Add them together.
    return xlines+ylines+zlines    
_____________________________________
def f(x,y,z):
    s1 = (4 * x * y - x * (y - 1) - y * (x - 1)) * (z + 1)
    s2 = (x + 1) * (y + 1) * z
    return s1 + s2
_____________________________________
def f(x,y,z):
    x1, y1, z1 = x+1, y+1, z+1
    return x1*y1*z + x*y1*z1 + x1*y*z1
_____________________________________
f=lambda x,y,z:z*(3*x*y+1+2*(x+y))+2*x*y+x+y
