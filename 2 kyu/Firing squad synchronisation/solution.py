Q, A, B, C, D, E, N, X = 'Q A B C D fire N X'.split()

rules = {Q: {N: {N: X, Q: Q, A: C, B: B, C: Q, D: Q},
             Q: {N: Q, Q: Q, A: C, B: B, C: Q, D: Q},
             A: {N: C, Q: C, A: C, B: B, C: X, D: C},
             B: {N: B, Q: B, A: B, B: B, C: A, D: X},
             C: {N: Q, Q: Q, A: X, B: A, C: Q, D: Q},
             D: {N: Q, Q: Q, A: C, B: X, C: Q, D: Q}},

         A: {N: {N: E, Q: B, A: E, B: A, C: C, D: C},
             Q: {N: B, Q: B, A: B, B: X, C: A, D: X},
             A: {N: E, Q: B, A: E, B: A, C: C, D: C},
             B: {N: A, Q: X, A: A, B: A, C: X, D: A},
             C: {N: C, Q: A, A: C, B: X, C: C, D: C},
             D: {N: C, Q: X, A: C, B: A, C: C, D: C}},

         B: {N: {N: X, Q: D, A: A, B: X, C: A, D: B},
             Q: {N: D, Q: D, A: C, B: D, C: D, D: D},
             A: {N: A, Q: C, A: A, B: A, C: X, D: A},
             B: {N: X, Q: D, A: A, B: X, C: A, D: B},
             C: {N: A, Q: D, A: X, B: A, C: A, D: X},
             D: {N: B, Q: D, A: A, B: B, C: X, D: B}},

         C: {N: {N: X, Q: X, A: D, B: B, C: X, D: C},
             Q: {N: X, Q: X, A: D, B: B, C: X, D: C},
             A: {N: D, Q: D, A: D, B: D, C: D, D: X},
             B: {N: B, Q: B, A: D, B: B, C: B, D: X},
             C: {N: X, Q: X, A: D, B: B, C: X, D: C},
             D: {N: C, Q: C, A: X, B: X, C: C, D: C}},

         D: {N: {N: X, Q: X, A: Q, B: Q, C: X, D: X},
             Q: {N: X, Q: X, A: Q, B: Q, C: A, D: X},
             A: {N: Q, Q: Q, A: Q, B: X, C: B, D: Q},
             B: {N: Q, Q: Q, A: X, B: Q, C: X, D: Q},
             C: {N: X, Q: A, A: B, B: X, C: X, D: A},
             D: {N: X, Q: X, A: Q, B: Q, C: A, D: X}}}

initial_state = Q 
trigger_state = A

def normal_rule(left, current, right):
    return rules[current][left][right]

def first_rule(current, right):
    return normal_rule(N, current, right)

def last_rule(left, current):
    return normal_rule(left, current, N)
  
_____________________________________________
initial_state='idle'
trigger_state='general'

def normal_rule(prev, target, next):  #rule for the inner robots
    if target == 'general':
        if prev == 'general' and next == 'general': return 'fire'
        if prev == 'general': return 'leg-right-1'
        if next == 'general': return 'leg-left-1'
        return 'double-leg-1'
    if prev == 'general' and next == 'general': return 'double-hand-back'
    if prev == 'general': return 'hand-right'
    if next == 'general': return 'hand-left'
    if any(p in (('hand-right', 'leg-left-2'), ('leg-right-2', 'hand-left'),
                 ('hand-right', 'double-leg-2'), ('double-leg-2', 'hand-left'),
                 ('double-hand-front', 'leg-left-2'), ('leg-right-2', 'double-hand-front'),
                 ('double-hand-front', 'double-leg-2'), ('double-leg-2', 'double-hand-front'),
                ) for p in ((prev, target), (target, next))): return 'general'
    if (prev, target) in (('hand-right', 'leg-left-0'), ('hand-right', 'double-leg-0'),
                         ('double-hand-front', 'leg-left-0'), ('double-hand-front', 'double-leg-0')): return 'general'
    if (target, next) in (('leg-right-0', 'hand-left'), ('double-leg-0', 'hand-left'),
                         ('leg-right-0', 'double-hand-front'), ('double-leg-0', 'double-hand-front')): return 'general'
    if prev in ('leg-right-2', 'double-leg-2') and target == 'double-hand-front' and next in ('leg-left-2', 'double-leg-2'): return 'general'
    if prev == 'hand-right' and next == 'hand-left': return 'double-hand-back'
    if next in ('hand-left', 'double-hand-front'): return 'hand-left'
    if prev in ('hand-right', 'double-hand-front'): return 'hand-right'
    if target == 'double-hand-back': return 'double-hand-front'
    if target == 'double-leg-1': return 'double-leg-2'
    if target == 'leg-right-1': return 'leg-right-2'
    if target == 'leg-right-0': return 'leg-right-1'
    if prev in ('leg-right-2', 'double-leg-2'): return 'leg-right-0'
    if target == 'leg-left-1': return 'leg-left-2'
    if target == 'leg-left-0': return 'leg-left-1'
    if next in ('leg-left-2', 'double-leg-2'): return 'leg-left-0'
    return 'idle'

def first_rule(target, next):  #rule for the first robot (will receive the order)
    if target == 'general':
        if next == 'general': return 'fire'
        return 'leg-right-1'
    if next == 'general': return 'hand-left'
    if (target, next) in (('hand-right', 'leg-left-2'), ('leg-right-2', 'hand-left'),
                          ('hand-right', 'double-leg-2'), ('double-leg-2', 'hand-left'),
                          ('double-hand-front', 'leg-left-2'), ('leg-right-2', 'double-hand-front'),
                          ('double-hand-front', 'double-leg-2'), ('double-leg-2', 'double-hand-front')): return 'general'
    if (target, next) in (('leg-right-0', 'hand-left'), ('double-leg-0', 'hand-left'),
                         ('leg-right-0', 'double-hand-front'), ('double-leg-0', 'double-hand-front')): return 'general'
    if next in ('hand-left', 'double-hand-front'): return 'hand-left'
    if target == 'hand-left': return 'hand-right'
    if target == 'leg-right-1': return 'leg-right-2'
    if target == 'leg-right-0': return 'leg-right-1'
    if target == 'leg-left-2': return 'leg-right-0'
    if target == 'leg-left-1': return 'leg-left-2'
    if target == 'leg-left-0': return 'leg-left-1'
    if next in ('leg-left-2', 'double-leg-2'): return 'leg-left-0'
    return 'idle'

def last_rule(prev, target):   #rule for the last robot
    if target == 'general':
        if prev == 'general': return 'fire'
        return 'leg-left-1'
    if prev == 'general': return 'hand-right'
    if (prev, target) in (('hand-right', 'leg-left-2'), ('leg-right-2', 'hand-left'),
                          ('hand-right', 'double-leg-2'), ('double-leg-2', 'hand-left'),
                          ('double-hand-front', 'leg-left-2'), ('leg-right-2', 'double-hand-front'),
                          ('double-hand-front', 'double-leg-2'), ('double-leg-2', 'double-hand-front')): return 'general'
    if (prev, target) in (('hand-right', 'leg-left-0'), ('hand-right', 'double-leg-0'),
                         ('double-hand-front', 'leg-left-0'), ('double-hand-front', 'double-leg-0')): return 'general'
    if prev == 'leg-right-2' and target == 'hand-left': return 'general'
    if prev in ('hand-right', 'double-hand-front'): return 'hand-right'
    if target == 'hand-right': return 'hand-left'
    if target == 'leg-left-1': return 'leg-left-2'
    if target == 'leg-right-1': return 'leg-right-2'
    if target == 'leg-right-0': return 'leg-right-1'
    if prev in ('leg-right-2', 'double-leg-2'): return 'leg-right-0'
    if target == 'leg-left-1': return 'leg-left-2'
    if target == 'leg-left-0': return 'leg-left-1'
    if target == 'leg-right-2': return 'leg-left-0'
    return 'idle'
  
__________________________________________________________________________________
initial_state=(0,0,0,0,0,0)
trigger_state=(0,1,0,1,1,0)

def normal_rule(P, T, N):    
    if T[4] and N[4] and P[4]:
        return 'fire'
    
    if (T[3]==3 and N[0]) or (T[1] and N[2]==3):
        return (1,0,1,0,1,0)
    
    if (P[3]==3 and T[0]) or (P[1] and T[2]==3):
        return (0,1,0,1,1,0)
    
    if (T[3]==1 and N[0]) or (P[1] and T[2]==1):
        return (1,1,1,1,1,0)
    
    if (P[3]==1 and T[0]) or (T[1] and N[2]==1):
        return (0,0,0,0,0,0)
    
    cross=N[0] and P[1]
    lh=T[5] or (N[0] and not cross)
    rh=T[5] or (P[1] and not cross)
    
    if T[2] in (1,2):
        lf=T[2]+1
    else:
        lf=N[2]==3
    
    if T[3] in (1,2):
        rf=T[3]+1
    else:
        rf=P[3]==3

    return (lh,rh,lf,rf,0,cross)

def sym(T):
    return (T[1],T[0],T[3],T[2],T[4],T[5])

def first_rule(target, next):
    return normal_rule(sym(target), target, next)

def last_rule(prev, target):
    return normal_rule(prev, target, sym(target))
