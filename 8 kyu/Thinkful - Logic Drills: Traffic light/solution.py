def update_light(current):
    if current == 'green':
        current = 'yellow'
    elif current == 'yellow':
        current = 'red'
    elif current == 'red':
        current = 'green'
    
    return current
