solution=(m1,m2,M1,M2,v,t)=>(M1/m1+M2/m2)*0.082*(t+273.15)/v

#########
function solution(M1, M2, m1, m2, V, T) {
    M1 = m1 * 0.001/M1;
    M2 = m2 * 0.001/M2;
    T = T + 273.15;
  var R = 0.082;

  return (((M1 + M2) * R * T) / V) * 1000;
}

################
solution=(s,t,u,p,i,d)=>(u/s+p/t)*0.082*(d+273.15)/i

#############
const solution = (Mol1, Mol2, mass1, mass2, Vol, Tempr) => {
  let Press = 0.082;
  let M1 = mass1 * 0.001/Mol1;
  let M2 = mass2 * 0.001/Mol2;
  let T = Tempr + 273.15;

  return (((M1 + M2) * Press * T) / Vol) * 1000;
}

##############
const solution = (M1, M2, m1, m2, V, T) => {
  const R = .082;
  const n = m1 / M1 + m2 / M2;
  return n * (T + 273.15) * R / V; 
}

############
solution= (molarMass1, molarMass2, givenMass1, givenMass2, volume, temp) => {
  return (givenMass1/molarMass1 + givenMass2/molarMass2) * 0.082 * (temp+273.15) / volume;
}
