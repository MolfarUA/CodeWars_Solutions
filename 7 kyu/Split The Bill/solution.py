def split_the_bill(x):
    diff = sum(x.values())/float(len(x))
    return {k: round(x[k]-diff, 2) for k in x}
##########
def split_the_bill(spendings):
    fair_amount = sum(spendings.itervalues()) / float(len(spendings))
    return {name: round(amount - fair_amount, 2) for name, amount in spendings.iteritems()}
#########
def split_the_bill(x):
    value = 0
    for key in x:
        value+=x[key]
    m = value/len(x)
    for key in x:
        x[key]=round(x[key]-m,2)
    return x
###########
def split_the_bill(x):
    many = len(x)
    total = sum(x.values())
    new_vals = []
    new_keys = []
    for a in x.values():
        new_vals.append(round(a - (total/many), 2))
    # total the sum of the x.values, then divide by the length.
    for a in x.keys():
        new_keys.append(a)
    return dict(zip(new_keys, new_vals))
###########
def split_the_bill(x):
    total = 0
    nb = 0
    y = {}
    for j in x.values():
        total += j
        nb += 1
    print(total/nb)
    for i,j in x.items():
        if j - total / nb - int(j - total / nb) == 0:
            y[i]= int(j - total / nb)
        else:
            y[i]= round(j - total / nb,2)
    return y
#############
def split_the_bill(x):
    # Good Luck!
    #should return an object/dic with the same names, showing how much money they should 
    #pay or receive
    #value decimal: :.2 => g = float("{0:.2f}".format(x))
    mean = sum(x.values())/float(len(x))
    group = {}
    for i in x:
        group[i] = round(x[i] - mean, 2)
    return group
###########
def split_the_bill(x):
    """
    Params : x - Dict - Name : amount_paid - At least 2 key-val pairs
    Out : Dict - Name : amount_payable - +ve numbers for need to be paid, -ve for must pay
                round to 2 decimal places
    """
    values = x.values()
    tot, num = sum(values), len(values)
    
    return { k: round(v - tot/num, 2) for (k,v) in x.items() }
