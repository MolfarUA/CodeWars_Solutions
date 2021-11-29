exec("".join(map(chr,[int("".join(str({':(': 4, ':/': 7, ':D': 1, '=/': 6, ':P': 2, '=)': 5, ';)': 9, ':)': 0, ':{': 8, ':S': 3}[i]) for i in x.split())) for x in 
""":D :) :)  :D :) :D  :D :) :P  :S :P  :D :P :P  :D :) :D  :D :D :(  :D :D :D  :/ :)  :D :D
:/  :D :) :D  :D :) :{  :( :)  :D :) :)  :D :) =)  :D :D =)  :D :D =/  ;) :/  :D :D :)  ;) ;)  
:D :) :D  ;) =)  :D :D =/  :D :D :D  ;) =)  :D :D :P  :D :D :/  :D :) ;)  :D :D :P  :( :(  :S 
:P  :D :) ;)  :D :D :P  :D :) :S  :( :(  :S :P  :D :) :P  :D :D :/  :D :) :D  :D :) :{  ;) =)  
:D :) :{  :D :) :D  :D :) :P  :D :D =/  :( :D  =) :{  :D :)  :S :P  :S :P  :S :P  :S :P  :D :D 
:(  :D :) :D  :D :D =/  :D :D :/  :D :D :(  :D :D :)  :S :P  :D :) :)  :D :) =)  :D :D =)  :D 
:D =/  ;) :/  :D :D :)  ;) ;)  :D :) :D  ;) =)  :D :D =/  :D :D :D  ;) =)  :D :D :P  :D :D :/  
:D :) ;)  :D :D :P  :S :P  =/ :)  =/ :D  :S :P  :D :) ;)  :D :D :P  :D :) :S  :S :P  :( :P  :S 
:P  :D :) :P  :D :D :/  :D :) :D  :D :) :{  ;) =)  :D :) :{  :D :) :D  :D :) :P  :D :D =/  :D :)"""
.split("  ")])))
#################
def zeroFuel(distance_to_pump, mpg, fuel_left):
    return distance_to_pump <= mpg * fuel_left
############
zeroFuel = lambda distance, mpg, gallons: mpg * gallons >= distance
###########
def zero_fuel(distance_to_pump, mpg, fuel_left):
    if fuel_left >= distance_to_pump / mpg:
        print("We got to the pump")
        return True
    else:
        print("We pushed the car to the pump(((")
        return False
print(zero_fuel(50,25,2))
############
def zeroFuel(distance_to_pump, mpg, fuel_left):
    return mpg*fuel_left >= distance_to_pump
############
def zeroFuel(a, b, c):
    return b * c >= a
############
zero_fuel = lambda d, m, f : d <= m * f
############
def zeroFuel(distance_to_pump, mpg, fuel_left):
    return fuel_left >= distance_to_pump/mpg
###########
zero_fuel = lambda *arg: arg[0] <= arg[1] * arg[2]
###########
def zero_fuel(distance_to_pump, mpg, fuel_left):
   return not distance_to_pump > mpg * fuel_left;
############
def zero_fuel(distance_to_pump, mpg, fuel_left):
    return fuel_left >= distance_to_pump / mpg
##########
def zero_fuel(distance_to_pump, mpg, fuel_left):
    a = mpg * fuel_left
    if a < distance_to_pump:
        return False
    else:
        return True
#############
def zero_fuel(distance_to_pump, mpg, fuel_left):
    a = distance_to_pump - mpg * fuel_left
    if a <= 0:
        return True
    elif a > 0:
        return False
#########
zero_fuel = lambda _,__,___: ___*__>=_
