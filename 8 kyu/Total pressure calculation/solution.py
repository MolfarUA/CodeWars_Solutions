def solution(M1, M2, m1, m2, V, T) :
    return (m1/M1+m2/M2)*0.082*(T+273.15)/V
  
##############
def solution(molar_mass1, molar_mass2, given_mass1, given_mass2, volume, temp) :
    
# 1 - Calculate the amount of substance in moles
    n1 = given_mass1 / molar_mass1
    n2 = given_mass2 / molar_mass2
# 2 - Convert the temperature from Celcius to kelvin  
    Temp_Kelvin = temp + 273.15
# 3 - Enter the gas constant
    R = 0.082
# 4 - Calculate the ideal gas law       
    P1 = (n1 * R * Temp_Kelvin) / volume
    P2 = (n2 * R * Temp_Kelvin) / volume
# 5 - Apply Dalton's law
    P = P1 + P2
    return P
  
###############
def solution(M1, M2, m1, m2, V, T):
    return (m1 / M1 + m2 / M2) * (T + 273.15) * .082 / V
  
###################
def solution(molar_mass1, molar_mass2, given_mass1, given_mass2, volume, temp) :
    t = temp + 273.15
    R = 0.082
    n_mol1 = given_mass1 / molar_mass1
    n_mol2 = given_mass2 / molar_mass2
    return (n_mol1 * R * t/volume) + (n_mol2 * R * t/volume)
    
##################
def solution(molar_mass1, molar_mass2, given_mass1, given_mass2, volume, temp) :
    p_total = ( ((given_mass1/molar_mass1)+(given_mass2/molar_mass2)) * (0.082) * (temp+273.15) )/ volume
    return p_total
  
###################
def solution(molar_mass1, molar_mass2, given_mass1, given_mass2, volume, temp) :
    temp_k = temp + 273.15
    r = 0.082
    return (((given_mass1 / molar_mass1) + (given_mass2 / molar_mass2)) * r * temp_k) / volume 
  
#################
def solution(molar_mass1, molar_mass2, given_mass1, given_mass2, volume, temp):
    return (given_mass1/molar_mass1 + given_mass2/molar_mass2)*.082*(temp + 273.15)*volume**(-1)
  
##############
def solution(molar_mass1, molar_mass2, given_mass1, given_mass2, volume, temp) :
    T=temp+273.15
    R=0.082
    P= (((given_mass1/molar_mass1)+(given_mass2/molar_mass2))*R*T)/volume
    return P
