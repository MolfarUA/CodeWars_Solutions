def bouncingBall(h, bounce, window):
    if (h <= 0) or (bounce <= 0) or (bounce >= 1) or (window >= h):
        return -1
    else:
        i = 1
        while h > window:
            i += 2
            h = h * bounce
    return i - 2
##############
def bouncingBall(h, bounce, window):
    if not 0 < bounce < 1: return -1
    count = 0
    while h > window:
        count += 1
        h *= bounce
        if h > window: count += 1
    return count or -1
############
from math import log

def bouncingBall(h, bounce, window):
    if not (h > 0 and 0 < bounce < 1 and window < h):
        return -1
    return 1 + 2*int(log(window/float(h), bounce))
#############
def bouncingBall(h, bounce, window):
    seen = -1
    
    if 0 < bounce < 1:
        while h > window > 0:
            seen += 2
            h *= bounce
    
    return seen
############
# The height of the ball after bouncing can be expressed as an exponential function:
#
# f(x) = h * bounce^x
# f(x) is the height the ball reaches after x bounces
# h is initial height
# bounce is the decay factor
#
# By solving the equation f(x) = window, we get the number of 
# bounces that will finally put the ball at the exact window height.
#
# Example:
# f(x) = 3 * 0.66^x
# f(x) = 1.5  -->  x ~= 1.67
# So the first bounce will put the ball a bit above window height,
# but the second will put it a bit below.
# This means the ball will pass the window 2 times (one bounce).
#
# If a bounce puts the ball at the exact window height (an exact 
# number of bounces, x is an integer), this would mean the ball 
# won't pass the window, only appear in front of it.
# However, due to the restriction in this assignment, the ball
# can only be seen if it's height is _strictly_ greater than the 
# window height.

import math

def bouncingBall(h, bounce, window):
    # If parameters don't fulfil conditions, return -1
    if not (h > 0 and 0 < bounce < 1 and window < h):
        return -1
    # Solve equation for f(x) = window, using logarithms
    bounces = math.log(window / h, bounce)
    # Get actual number of bounces that still puts the ball above window height
    exactBounces = math.floor(bounces)
    # If last bounce is not strictly higher than window height, it can't be seen
    if bounces == exactBounces: 
        exactBounces -= 1
    # The ball will pass the window two times for each bounce, up and down, 
    # plus one for the initial drop past window, before first bounce
    passes = exactBounces * 2 + 1
    return passes
################
def bouncing_ball(h, bounce, window):
    if (h <= 0) or (bounce <= 0) or (bounce >= 1) or (window >= h):
        return -1
    else:
        i = 1
        while h > window:
            i += 2
            h = h * bounce
    return i - 2
#############
def bouncing_ball(h, bounce, window):
    if not(h > 0 and 0 < bounce < 1 and window < h):
        return -1
    else:
        count = 1
        h *= bounce
        while h > window:
            count +=2
            h *= bounce
        return count
############
def bouncing_ball(h, bounce, window):
    num=-1
    if h<= 0:
        return -1
    if bounce <= 0 or bounce >= 1:
        return -1
    if window > h:
        return -1
    while h > window:
        h*=bounce
        num+=2
    return num
#############
def bouncing_ball(h, bounce, window):
    i = 0
    if (h > 0) and (1>bounce>0) and (window < h):
        while h > window:
            i = i + 1
            h = h * bounce
            if h > window:
                i = i + 1
            else:
                break
    
    else:
        return -1
    
    return i
_________________________________________
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
