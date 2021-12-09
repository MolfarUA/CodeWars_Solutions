def zombie_shootout(zombies, distance, ammo, shot=0):
    if not zombies:
        return f'You shot all {shot} zombies.'
    if distance <= 0:
        return f'You shot {shot} zombies before being eaten: overwhelmed.'
    if not ammo:
        return f'You shot {shot} zombies before being eaten: ran out of ammo.'
    return zombie_shootout(zombies - 1, distance - 0.5, ammo - 1, shot + 1)
#########
def zombie_shootout(zomb, dist, pill):
    if zomb <= dist*2 and zomb <= pill: return 'You shot all ' + str(zomb) + ' zombies.'
    if zomb > dist*2 and zomb <= pill: return 'You shot ' + str(dist*2) + ' zombies before being eaten: overwhelmed.'
    if zomb > dist*2 and zomb > pill and dist*2 <= pill: return 'You shot ' + str(dist*2) + ' zombies before being eaten: overwhelmed.'
    if zomb > pill: return 'You shot ' + str(pill) + ' zombies before being eaten: ran out of ammo.'
###########
def zombie_shootout(zombies, distance, ammo):
    results = {f"You shot all {zombies} zombies.": zombies,
               f"You shot {distance * 2} zombies before being eaten: overwhelmed.": distance * 2,
               f"You shot {ammo} zombies before being eaten: ran out of ammo.": ammo}
    
    return min(results, key=results.get)
##########
def zombie_shootout(zombies, distance, ammo):
    if distance * 2 < min(ammo+1, zombies):
        return f"You shot {distance*2} zombies before being eaten: overwhelmed."
    if ammo < zombies:
        return f"You shot {ammo} zombies before being eaten: ran out of ammo."
    return f"You shot all {zombies} zombies."
##########
def zombie_shootout(zombies, range, ammo):
    distance = range*2
    if zombies > ammo < distance: 
        return f"You shot {ammo} zombies before being eaten: ran out of ammo."
    elif zombies > distance: 
        return f"You shot {distance} zombies before being eaten: overwhelmed."
    return f"You shot all {zombies} zombies."   
##########
def zombie_shootout(zombies, distance, ammo):
    z = zombies
    d = distance
    a = ammo

    while d >= 0:
        z = z - 1
        a = a - 1
        d = d - 0.5

        if z <= 0:
            return "You shot all {} zombies.".format(zombies)
        if d<=0 and a>=0:
            return "You shot {} zombies before being eaten: overwhelmed.".format(zombies-z)
        if z>0 and a<=0:
            return "You shot {} zombies before being eaten: ran out of ammo.".format(zombies-z)
###########
def zombie_shootout(zombies, distance, ammo):
    kills = 0
    while ammo and zombies and distance:
        ammo -= 1
        zombies -= 1
        kills += 1
        distance -= 0.5
    if zombies and not ammo and distance:
        return f'You shot {kills} zombies before being eaten: ran out of ammo.'
    if zombies:
        return f'You shot {kills} zombies before being eaten: overwhelmed.'
    return f'You shot all {kills} zombies.'
#############
def zombie_shootout(zombies, distance, ammo):
    zombies_shot = 0
    
    for i in range((distance + 1) * 2):
        if distance == 0 and zombies > 0:
            return overwhelmed(zombies_shot)
        
        elif ammo == 0 and zombies > 0:
            return no_ammo(zombies_shot)
        
        elif zombies == 0:
            return you_win(zombies_shot)
        
        zombies, ammo, distance, zombies_shot = calculate_stats(zombies, ammo, distance, zombies_shot)
        
        
def calculate_stats(zombies, ammo, distance, zombies_shot):
        zombies -= 1
        ammo -= 1
        distance -= 0.5
        zombies_shot += 1
        
        return zombies, ammo, distance, zombies_shot


def overwhelmed(zombies_shot):
    return f'You shot {zombies_shot} zombies before being eaten: overwhelmed.'


def no_ammo(zombies_shot):
    return f'You shot {zombies_shot} zombies before being eaten: ran out of ammo.'
    

def you_win(zombies_shot):
    return f'You shot all {zombies_shot} zombies.'
#################
def zombie_shootout(zombies, distance, ammo):
    
    x=0
    
    while (zombies > 0) and (distance > 0) and (ammo > 0):
        x+=1
        zombies -= 1
        distance -= 0.5
        ammo -= 1
    
    if zombies == 0:
        return f"You shot all {x} zombies."
    elif distance == 0:
        return f"You shot {x} zombies before being eaten: overwhelmed."
    else:
        return f"You shot {x} zombies before being eaten: ran out of ammo."
###################
def zombie_shootout(zombies, distance, ammo):
    zombies_shot = 0
    
    for i in range((distance + 1) * 2):
        if distance == 0 and zombies > 0:
            return overwhelmed(zombies_shot)
        
        elif ammo == 0 and zombies > 0:
            return no_ammo(zombies_shot)
        
        elif zombies == 0:
            return you_win(zombies_shot)
            
        zombies -= 1
        ammo -= 1
        distance -= 0.5
        zombies_shot += 1


def overwhelmed(zombies_shot):
    return f'You shot {zombies_shot} zombies before being eaten: overwhelmed.'

def no_ammo(zombies_shot):
    return f'You shot {zombies_shot} zombies before being eaten: ran out of ammo.'
    
def you_win(zombies_shot):
    return f'You shot all {zombies_shot} zombies.'
