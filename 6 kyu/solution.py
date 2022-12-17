58b1ae711fcffa34090000ea


def controller(events):

    out, state, dir, moving = [], 0, 1, False
    
    for c in events:
        if   c == 'O':      dir *= -1
        elif c == 'P':      moving = not moving
        if moving:          state += dir
        if state in [0,5]:  moving, dir = False, 1 if state == 0 else -1
        out.append(str(state))
        
    return ''.join(out)
_________________________________
def controller(events):
    state = 0
    movement = False
    direction = True
    output = ''
    for event in events:
        if event is 'P':
            movement = not movement
        if event is 'O':
            direction = not direction
        state = state + (-1, 1)[direction] * movement
        if state in (0, 5):
            direction = not state
            movement  = False
        output += str(state)
    return output
_________________________________
def controller(events):
    pos, speed, dir, res = 0, 0, 1, ''
    for e in events:
        if   e == 'P': speed = not speed
        elif e == 'O' and speed: dir *= -1
        pos += speed * dir
        if pos in (0, 5) and speed: speed, dir = 0, dir * -1
        res += str(pos)
    return res
_________________________________
def controller(events):
    positions = []
    move = direction = last_pos = False
    for event in events:
        if event == 'O':
            direction = not direction
        elif event == 'P':
            move = not move
        last_pos += [1, -1][direction] * move
        print(event, last_pos, move, direction)
        if last_pos in (0, 5):
            move = False
            direction = bool(last_pos)
        positions.append(str(last_pos))
    return ''.join(positions)
_________________________________
def controller(events):
    output = ''
    moving = False # implies stationary
    direction = 1 # implies opening, -1 implies closing
    door_position = 0
    
    for i in events:
        
        if door_position == 0:
            direction = 1
            moving = False
        elif door_position == 5:
            direction = -1
            moving = False
        
        if i == 'P':
            if moving:
                moving = False
            else:
                moving = True
        elif i == 'O':
            if direction == 1:
                direction = -1
            else:
                direction = 1
        
        if moving:
            door_position = door_position + direction
                
        output += str(door_position)
        
    return output
