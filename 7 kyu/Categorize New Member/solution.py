def openOrSenior(data):
  return ["Senior" if age >= 55 and handicap >= 8 else "Open" for (age, handicap) in data]
################
def openOrSenior(data):
    res = []
    for i in data:
      if i[0] >= 55 and i[1] > 7:
        res.append("Senior")
      else:
        res.append("Open")
    return res
###############
def openOrSenior(members):
    return ["Senior" if m[0]>54 and m[1]>7 else "Open" for m in members]
#############
def openOrSenior(data):
    return ["Senior" if age >= 55 and handicap > 7 else "Open" for age, handicap in data]
###########
def openOrSenior(data):
    list =[]
    for age, hcap in data:
    
        if age >= 55 and hcap > 7:
            list.append('Senior')
            
        else: list.append('Open')
        
    return list
#############
def openOrSenior(data):
    return ['Senior' if x[0] > 54 and x[1] > 7 else 'Open' for x in data]
#################
def openOrSenior(data):
    return map(lambda d: 'Senior' if d[0] >= 55 and d[1] > 7 else 'Open', data)
#############
def openOrSenior(data):
    return ['Senior' if x[0]>=55 and x[1]>7  else 'Open' for x in data]
###########
def openOrSenior(data):
    categories = []
    for i in data:
        a,h = i
        if a > 54:
            if h > 7: categories += ["Senior"]
            else: categories += ["Open"]
        else: categories += ["Open"]
    return categories
#############
def openOrSenior(data):
    return ['Senior' if (i[0] >= 55) and (i[1] > 7) else 'Open' for i in data]
###########
def openOrSenior(data):
    def categorize(age, handicap):
        if age >= 55 and handicap > 7:
            return 'Senior'
        return 'Open'

    return [ categorize(*item) for item in data ]
############
def openOrSenior(data):
    return [['Open', 'Senior'][age >= 55 and handicap > 7] for age, handicap in data]
############
def openOrSenior(data):
    # Hmmm.. Where to start?
    ret = []
    for datum in data:
        age, handicap = datum
        if age >= 55 and handicap > 7:
            ret.append('Senior')
        else:
            ret.append('Open')
    return ret
#############
def openOrSenior(data):
    memberCategories = []
    for member in data:
        if member[0] >= 55 and member[1] > 7:
            memberCategories.append("Senior")
        else:
            memberCategories.append("Open")
    return(memberCategories)
#############
def openOrSenior(data):
    newlist = []
    for lists in data:
      if lists[0] >= 55 and lists[1] > 7:
        newlist.append('Senior')
      else:
        newlist.append('Open')
    return newlist
