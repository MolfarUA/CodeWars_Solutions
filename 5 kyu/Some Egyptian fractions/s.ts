54f8693ea58bce689100065f


interface Fraction {
  numerator: number;
  denominator: number;
}

function getGCD(n1: number, n2: number) {
  if(n1 === 0 || n2 === 0) return 1;
  if(n1 === n2) return n1;
  
  const maxValue = Math.max(n1, n2);
  const minValue = Math.min(n1, n2);
  
  if(minValue === 0) return maxValue;
  
  function recursion(maxValue: number, minValue: number): number {
    const quotient = Math.floor(maxValue / minValue);
    const remainder = maxValue - quotient * minValue;
    if(remainder === 0) return minValue;
    return recursion(minValue, remainder);
  }
  
  return recursion(maxValue, minValue);
}

function getFraction(n: string): Fraction {
  if(n === '0') return {
    numerator: 0,
    denominator: 1,
  }
  
  if(n.includes('/')) {
    const [num, den] = n.split('/');
    const gcd = getGCD(+num, +den);
    const numerator =Math.floor(+num / gcd);
    const denominator =Math.floor(+den / gcd);
    return {
      numerator,
      denominator,
    }
  }
  
  if(n.includes('.')) {
    const [integer, decimal] = n.split('.');
    const den = 10**(decimal.length);
    const num = +(integer || '0') * den + +decimal;
    const gcd = getGCD(num, den);
    const numerator = Math.floor(+num / gcd);
    const denominator = Math.floor(+den / gcd);
    return {
      numerator,
      denominator,
    };
  }
  
  throw new Error('the string is not a valid number');
}

function EgyptianFractions(fraction: Fraction): Fraction[] {
  if(!fraction.numerator || !fraction.denominator) return [];
  
  function recursion(fraction: Fraction): Fraction[] {
    const gcd = getGCD(fraction.numerator, fraction.denominator);
  
    const newFraction: Fraction = {
      numerator: fraction.numerator/gcd,
      denominator: fraction.denominator/gcd,
    };
    
    const base = Math.ceil(newFraction.denominator / newFraction.numerator);
    
    const term1: Fraction = {
      numerator: 1,
      denominator: base,
    };
    
    const isEqualNumerators = term1.numerator === fraction.numerator;
    const isEqualDenominators = term1.denominator === fraction.denominator;
    
    if(isEqualNumerators && isEqualDenominators) {
      return [term1];
    }
    
    const term2Numerator = newFraction.numerator - newFraction.denominator % newFraction.numerator;
    const term2Denominator = newFraction.denominator * base;
    
    const term2GCD = getGCD(term2Numerator, term2Denominator);
    
    const smallestTerm2Numerator = Math.floor(term2Numerator / term2GCD);
    const smallestTerm2Denominator = Math.floor(term2Denominator / term2GCD);
    
    const term2: Fraction = {
      numerator: smallestTerm2Numerator,
      denominator: smallestTerm2Denominator,
    };
    
    return term2.numerator === 0
      ? [term1]
      : term2.numerator === 1
      ? [term1, term2]
      : [term1, ...recursion(term2)];
  };
  
  return recursion(fraction);
}

export function decompose(n: string): string[] {
  const nFraction = getFraction(n);
  const integer = Math.floor(nFraction.numerator / nFraction.denominator);
  nFraction.numerator = nFraction.numerator % nFraction.denominator;

  const fractionsArray = EgyptianFractions(nFraction);
  const fractions = fractionsArray.map(fr => `${fr.numerator}/${fr.denominator}`);
  
  return integer ? [`${integer}`, ...fractions] : fractions;
}
_________________________________
export function decompose(n: string): string[] {
  const target = Number.isNaN(Number(n)) ? Number(n.split("/")[0]) / Number(n.split("/")[1]) : Number(n),
        divs: number[] = [],
        nums = target >= 1 ? Math.floor(target) : 0
  let sum = nums ? nums : 0,
      div = 1
  
  while(target - sum > 0.0000000001) {
    if(sum + (1/div) <= target) {
      divs.push(div)
      sum = sum + (1/div)
    }
    if(div <= 9999999) div++
    else if(div <= 99999999) div += 5
    else div += 10
  }
  
  let result = nums ? [ nums.toString() ] : []
  return result.concat(divs.map(n => `1/${n}`))
}
