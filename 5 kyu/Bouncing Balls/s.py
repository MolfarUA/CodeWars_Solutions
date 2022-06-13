def bouncingBall(h, bounce, window):
    if not 0 < bounce < 1: return -1
    count = 0
    while h > window:
        count += 1
        h *= bounce
        if h > window: count += 1
    return count or -1
_______________________________________________
from math import log

def bouncingBall(h, bounce, window):
    if not (h > 0 and 0 < bounce < 1 and window < h):
        return -1
    return 1 + 2*int(log(window/float(h), bounce))
_______________________________________________
def bouncingBall(h, bounce, window):
    seen = -1
    
    if 0 < bounce < 1:
        while h > window > 0:
            seen += 2
            h *= bounce
    
    return seen
_______________________________________________
def bouncing_ball(h, bounce, window):
    if h>0 and (bounce>0 and bounce<1) and window<h:
        vista = 1
        rimbalzo = h*bounce
        while rimbalzo>window:
            vista+=2
            h = rimbalzo
            rimbalzo*=bounce
        return vista
    return -1
_______________________________________________
def bouncing_ball(h, bounce, window):
    bt = []
    if h > 0:
        if 0 < bounce < 1:
            if window < h:
                while h > window:
                    bt.append(h)
                    h *= bounce
            else:
                return -1
        else:
            return -1
    else:
        return -1
    ft = ((len(bt) - 1) * 2)// 2
    total = len(bt) + ft
    return total
_______________________________________________
def bouncing_ball(h, bounce, window):
    if h <= 0 or bounce <= 0 or bounce >=1 or window >= h:
        return -1
    passes = 1
    while True:
        h *= bounce
        if h > window:
            passes +=2
        else:
            return passes
_______________________________________________
def bouncing_ball(h, bounce, window):
    if h > 0 and 0 < bounce < 1 and window < h:
        counter = 0
        while h > window:
            counter += 1
            h = h * bounce
            if h > window:
                counter += 1
            else:
                pass
        return counter
    else:
        return -1
_______________________________________________
def bouncing_ball(h, bounce, window):
    if 0 < h and 0 < bounce and bounce < 1 and window < h:
        bounce_count = -1
        while h > window:
            bounce_count = bounce_count + 2
            h = h * bounce
    else:
        bounce_count = -1

    return(bounce_count)
_______________________________________________
def bouncing_ball(h, bounce, window):
    answer = 0
    if h > 0 and bounce > 0 and bounce < 1 and window < h:
        while h > window:
            answer += 1
            if h * bounce > window:
                answer += 1
                h = h * bounce
            else:
                return answer
    else:
        return -1
