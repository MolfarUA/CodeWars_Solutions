5601c5f6ba804403c7000004


def bar_triang((xA, yA), (xB, yB), (xC, yC)):
    x0 = round((xA + xB + xC) / 3.0, 4)
    y0 = round((yA + yB + yC) / 3.0, 4)
    return [x0, y0]
__________________________________
def bar_triang(a, b, c):
    return [round(sum(x)/3.0, 4) for x in zip(a, b, c)]
__________________________________
def bar_triang(pointA, pointB, pointC): # points A, B and C will never be aligned
    return [round((pointA[0] + pointB[0] + pointC[0]) / 3.0, 4), round((pointA[1] + pointB[1] + pointC[1]) / 3.0, 4)]
__________________________________
def bar_triang(pointA, pointB, pointC): 
    a = (pointA[0] + pointB[0] + pointC[0]) / 3.0
    b = (pointA[1] + pointB[1] + pointC[1]) / 3.0
    return [round(a, 4), round(b, 4)]
__________________________________
def bar_triang(*args):
    return map(lambda a: round(sum(a) / 3.0, 4), zip(*args))
__________________________________
def bar_triang(a, b, c): 
    z=(a[0]+b[0]+c[0])/3
    z=int(z*100000)
    if z%10>=5:
        z=z//10+1
        z=z/10000
    else:
        z=z//10
        z=z/10000
    x=(a[1]+b[1]+c[1])/3
    x=int(x*100000)
    if x%10>=5:
        x=x//10+1
        x=x/10000
    else:
        x=x//10
        x=x/10000
    return [z,x]
__________________________________
def bar_triang(a,b,c): 
    x1,x2,x3 = a[0],b[0],c[0]
    y1,y2,y3 = a[-1],b[-1],c[-1]
    x = round((x1 + x2 + x3) / 3, 4)
    y = round((y1 + y2 + y3) / 3, 4)
    return [x,y]
__________________________________
def bar_triang(point_a, point_b, point_c): 
    x0 = round((point_a[0] + point_b[0] + point_c[0]) / 3, 4)
    y0 = round((point_a[1] + point_b[1] + point_c[1]) / 3, 4)
    mas = [x0, y0]
    return mas
__________________________________
def bar_triang(A, B, C):
  # Calculate midpoints of sides
  M1 = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2]
  M2 = [(B[0] + C[0]) / 2, (B[1] + C[1]) / 2]
  M3 = [(C[0] + A[0]) / 2, (C[1] + A[1]) / 2]

  # Calculate barycenter
  O = [(M1[0] + M2[0] + M3[0]) / 3, (M1[1] + M2[1] + M3[1]) / 3]

  # Round result to four decimal places
  O = [round(x, 4) for x in O]

  return O
__________________________________
def bar_triang(point_a, point_b, point_c): 
    p = lambda x,y,z: (x+y+z)/3
    base_x = p(point_a[0],point_b[0],point_c[0])
    base_y = p(point_a[1],point_b[1],point_c[1])
    return [round(base_x,4),round(base_y,4)]
