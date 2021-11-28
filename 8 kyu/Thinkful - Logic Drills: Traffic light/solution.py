update_light = {'red': 'green', 'yellow': 'red', 'green': 'yellow'}.__getitem__
############
def update_light(current):
    return {"green": "yellow", "yellow": "red", "red": "green"}[current]
##############
def update_light(current):
    if current == "green":
        return "yellow"
    elif current == "yellow":
        return "red"
    elif current == "red":
        return "green"
    else:
        return "This is not a traffic light color."
################
def update_light(current):
    color = ['green', 'yellow', 'red']
    return color[(color.index(current)+1)%len(color)]
##############
update_light = {"green":"yellow", "yellow":"red", "red":"green"}.get
#############
def update_light(current):
    light_order = {'red':'green', 'yellow':'red', 'green':'yellow'}
    
    return light_order[current]
###############
def update_light(current):
    change = {"green": "yellow", "yellow": "red", "red": "green"}
    return change[current]
###############
def update_light(current):
    if current=="green":
        return "yellow"
    elif current=="yellow":
        return "red"
    return "green"
###############
def update_light(_c): return {'green':'yellow','yellow':'red','red':'green'}[_c]
################
def update_light(current):
    current = str(current)
    if current == 'green':
        return 'yellow'
    elif current == 'yellow':
        return 'red'
    elif current == 'red':
        return 'green'
    else:
        return "Your input value of {} needs to be either \
        'green', 'yellow', or 'red'."
##################
update_light = lambda c,l=["yellow","green","red"]: l[l.index(c)-1]
###############
def update_light(current):
    return 'yellow' if current == 'green' else ('green' if current == 'red' else 'red')
#################
def update_light(current):
  return {"green": "yellow", "yellow": "red", "red": "green"}.get(current)
######################
def update_light(current):
    arr =['green', 'yellow', 'red']
    return arr[(arr.index(current)+1) % 3]
###################
update_light=lambda l,t=['red','yellow','green']:t[t.index(l)-1]
##################
def update_light(current):
    traffic_lights = ['green', 'yellow', 'red']
    return traffic_lights[(traffic_lights.index(current) + 1) % len(traffic_lights)]
##################
TRANSITIONS_DCT = {'green': 'yellow',
                  'yellow': 'red',
                  'red': 'green'}

def update_light(current): return TRANSITIONS_DCT[current]
################
def update_light(current):
  return 'yellow' if current == 'green' else 'red' if current == 'yellow' else 'green'
#################
def update_light(current):
    lights = ["green","yellow","red"]
    value = lights.index(current)
    if current in lights and value != 2:
        return lights[value+1]
    else:
        return lights[0]
####################
from itertools import cycle

def update_light(current):
    lights = cycle(["green", "yellow", "red"])
    while True:
        if next(lights) == current:
            return next(lights)
    return 'yellow' if current == 'green' else ('green' if current == 'red' else 'red')
