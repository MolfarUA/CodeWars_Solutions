5875b200d520904a04000003

def enough(cap, on, wait):
    return max(0, wait - (cap - on))

#########################
def enough(cap, on, wait):
    all_passengers = on + wait
    if cap > all_passengers:
        return 0
    else:
        return all_passengers - cap

__________________________________
def enough(cap, on, wait):
    # Your code here
    if (on + wait) <= cap:
        return 0
    else:
        spaces = cap - on
        
        return wait - spaces
________________________________
def enough(cap, on, wait):
    equal = on + wait
    if cap >= equal:
        return 0

    elif cap < equal:
        return equal - cap

    elif cap < equal:
        return on - wait

print(enough(81, 53, 44))
