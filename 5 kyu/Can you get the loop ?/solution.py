def loop_size(node):
    turtle, rabbit = node.next, node.next.next
    
    # Find a point in the loop.  Any point will do!
    # Since the rabbit moves faster than the turtle
    # and the kata guarantees a loop, the rabbit will
    # eventually catch up with the turtle.
    while turtle != rabbit:
        turtle = turtle.next
        rabbit = rabbit.next.next
  
    # The turtle and rabbit are now on the same node,
    # but we know that node is in a loop.  So now we
    # keep the turtle motionless and move the rabbit
    # until it finds the turtle again, counting the
    # nodes the rabbit visits in the mean time.
    count = 1
    rabbit = rabbit.next
    while turtle != rabbit:
        count += 1
        rabbit = rabbit.next

    # voila
    return count

_____________________________________________
def loop_size(node):
    index = {}
    i = 0
    while True:
        if node in index:
            return i - index[node]
        index[node] = i
        node = node.next
        i += 1
_____________________________________________
def loop_size(n):
    l = []
    while not n in l:
        l.append(n)
        n = n.next
    return len(l) - l.index(n)
_____________________________________________
from itertools import count

def loop_size(node):
    for i in count(): 
        node.index = i
        try:
            return node.index - node.next.index + 1
        except AttributeError:
            node = node.next
_____________________________________________
def loop_size(node): 
    visited = []
    while True:
        if hasattr(node, 'visited'):
            break
        else:
            visited.append(node)
            node.visited = True
            node = node.next
    return len(visited) - visited.index(node)
_____________________________________________
def loop_size(n):
    l = {}
    while n not in l:
        l[n], n = len(l), n.next
    return len(l)-l[n]
_____________________________________________
def loop_size(node):
    seen = {}
    while node not in seen:
        seen[node] = len(seen)
        node = node.next
    return len(seen) - seen[node]
_____________________________________________
def loop_size(node):
    count = 1
    travel = {node:count}
    while 1:
        node = node.next
        count += 1
        if node in travel:
            return count - travel[node]
        travel[node] = count
_____________________________________________
def loop_size(node):
    i = 0
    node.serial = i
    while not hasattr(node.next, 'serial'):
        node = node.next
        i += 1
        node.serial = i
    return i - node.next.serial + 1
