def cannons_ready(gunners):
    if list(gunners.values()).count("aye") == len(gunners):
        return 'Fire!'
    else:
        return 'Shiver me timbers!'
############
def cannons_ready(gunners):
  return 'Shiver me timbers!' if 'nay' in gunners.values() else 'Fire!'
###########
def cannons_ready(gunners):
    for i in gunners:
        if gunners[i] == 'nay':
            return 'Shiver me timbers!'
    return 'Fire!'
###############
def cannons_ready(gunners):
    return 'Fire!' if all(a == 'aye' for a in gunners.itervalues()) else \
        'Shiver me timbers!'
#############
def cannons_ready(g):
  return ['Fire!','Shiver me timbers!']['nay' in g.values()]
############
def cannons_ready(gunners):
    return 'Fire!' if all(gunners[n] == 'aye' for n in gunners) else 'Shiver me timbers!'
###############
def cannons_ready(gunners):
    print(gunners)
    if all(x=="aye" for x in gunners.values()):
        return "Fire!"
    else:
        return "Shiver me timbers!"
################
def cannons_ready(gunners):
    return "Fire!" if all(gunners[y] == "aye" for y in gunners.keys()) else "Shiver me timbers!"
#############
def cannons_ready(gunners):
    for value in gunners.values():
        if value != "aye":
            set = False
            break
        else:
            set = True
    return "Fire!" if set == True else 'Shiver me timbers!'
##############
def cannons_ready(gunners):
    for i,j in gunners.items():
        if j == 'nay':
            return 'Shiver me timbers!'
        else:
            pass
    return 'Fire!'
