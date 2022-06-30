def areYouPlayingBanjo(name):
    return name + (' plays' if name[0].lower() == 'r' else ' does not play') + " banjo";
________________________________
def areYouPlayingBanjo(name):
    if name[0].lower() == 'r':
        return name + ' plays banjo'
    else:
        return name + ' does not play banjo'
________________________________
def areYouPlayingBanjo(name):
   return name + " plays banjo" if name[0].lower() == 'r' else name + " does not play banjo"
________________________________
def areYouPlayingBanjo(name):
    if name.startswith('R') or name.startswith('r'):
        return name + ' plays banjo'
    else:
        return name + ' does not play banjo'
________________________________
def areYouPlayingBanjo(name):
    if name[0].lower() == 'r':
        return "{} plays banjo".format(name)
    return "{} does not play banjo".format(name)
________________________________
def areYouPlayingBanjo(name):
    if name[0] == 'r' or name[0] =='R':
        return ("%s plays banjo"%name)
    else:
        return ("%s does not play banjo"%name)
________________________________
def areYouPlayingBanjo(name):
    return name + (' plays banjo' if name[0]=='r' or name[0]=='R' else ' does not play banjo')
________________________________
def are_you_playing_banjo(name):
    return f"{name} plays banjo" if name.startswith("r") or name.startswith("R") else f"{name} does not play banjo"

are_you_playing_banjo("rebe")
________________________________
def are_you_playing_banjo(name):
    isName = True if name[0] in ("R","r") else False
    return name + " plays banjo" if isName else name + " does not play banjo"
