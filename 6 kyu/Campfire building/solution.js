function isConstructable(a) {
  for ( let i=1; i*i<=a; i++ )
    if ( Number.isInteger(Math.sqrt(a-i*i)) )
      return true;
  return false;
}
__________________________________
function isConstructable(a)
{
  // Your solution here
  let factors = factorize(a);
  for(let i = 0; i<factors.length; i++){
    let factorNumber = factors[i];
    if(Number.isInteger((factorNumber-3)/4)){
      let ocurrences = factors.reduce((numOcurrences, arrNumber) => (arrNumber === factorNumber ? numOcurrences + 1 : numOcurrences), 0);
      if(!Number.isInteger(ocurrences/2)){return false}
    }
  }
  
  return true;
}

function factorize(number){
  let factors = [];
  let remainingFactorize = number;
  for(let i = 2; i <= remainingFactorize; i++)
  {
    if(i>remainingFactorize/2){
      factors.push(remainingFactorize);
      break;
    }
    if(remainingFactorize%i===0){
      remainingFactorize /=i;
      factors.push(i);
      i=1;
    }
  }
  return factors;
}
__________________________________
function isConstructable(a)
{
  return [...Array(Math.floor(a**.5)+1).keys()]
    .map(i=>a-i*i)
    .some(n=>n**.5==Math.floor(n**.5));
}
__________________________________
function isConstructable(a)
{
  const sideLength = Math.floor(Math.sqrt(a));
  for (let i = sideLength; i >= 0; i--) {
    const b2 = a - i * i;
    const isSquared = Math.sqrt(b2);
    if (Math.floor(isSquared) - isSquared === 0) {
      return true;
    } 
  }
  return false;
}

// A = a2 + b2
// b2 = A - a2
