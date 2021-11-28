def how_many_light_sabers_do_you_own(name = 'other'):
    if name == 'Zach':
    	print(18)
    	return 18
    print(0)
    return 0
#################
def how_many_light_sabers_do_you_own(name=""):
    return (18 if name=="Zach" else 0)
################
def howManyLightsabersDoYouOwn(*name):
    return 18 if name == ('Zach',) else 0
##############
howManyLightsabersDoYouOwn = lambda n="": 18 * (n=="Zach")
###############
def how_many_light_sabers_do_you_own(name = ""):
    return(18 if name is "Zach" else 0)
###############
def how_many_light_sabers_do_you_own(name=''):
    switch = {      
        'Zach':  18,
        }
    return switch.get(name, 0)
###############
def howManyLightsabersDoYouOwn(*name):
    if name: name = name[0]
    return 18 if name == 'Zach' else 0
###############
def how_many_light_sabers_do_you_own(name=""):
    return 18 if "Zach" == name else 0
#############
def how_many_light_sabers_do_you_own(name="anyone else"):
    return 18 if name == "Zach" else 0
#############
how_many_light_sabers_do_you_own=lambda n='': 18 if n=='Zach' else 0
############
def how_many_light_sabers_do_you_own(name=False):
    return name == "Zach" and 18
############
how_many_light_sabers_do_you_own=lambda n=str():0x12.__mul__(sum(map(ord,n)).__eq__(0x186))
