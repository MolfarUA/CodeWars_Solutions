564e1d90c41a8423230000bc


def knightVsKing (knightPosition, kingPosition):
    dx = knightPosition[0] - kingPosition[0]
    dy = ord(knightPosition[1]) - ord(kingPosition[1])
    d = dx * dx + dy * dy
    if d == 5: return 'Knight'
    if d < 3: return 'King'
    return 'None'
_______________________________________
def knightVsKing(k,K):
    d = { abs(k[0]-K[0]), abs(ord(k[1])-ord(K[1])) }
    return 'Knight' if d=={1,2} else 'King' if set(d)<={0,1} else 'None'
_______________________________________
def knightVsKing (knightPosition, kingPosition):
    dx = abs(knightPosition[0] - kingPosition[0])
    dy = abs(ord(knightPosition[1]) - ord(kingPosition[1]))
    d = dx * dx + dy * dy
    
    if d == 5 :
        return 'Knight'
    elif d <= 2:
        return 'King'
    else:
        return 'None'
_______________________________________
def knightVsKing (a, b):
    a = (a[0], ord(a[1]) - 64)
    b = (b[0], ord(b[1]) - 64)
    move = sorted((abs(a[0] - b[0]), abs(a[1] - b[1])))
    return 'Knight' if move == [1, 2] else 'King' if move in ([0, 1], [1, 1]) else 'None'
