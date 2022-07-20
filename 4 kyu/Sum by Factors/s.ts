54d496788776e49e6b00052f


function getPrimes(input: number) {
  let n = Math.abs(input)
  const primes = new Set<number>()
  for (let i = 2; i < n; i++) {
    while (n % i === 0) {
      primes.add(i)
      n /= i
    }
  }
  
  if (n !== 1) {
    primes.add(n)
  }
  
  return Array.from(primes)
}

export function sumOfDivided(lst: number[]): number[][] {
  const sumByPrimes: Record<number, number> = {}
  for (const n of lst) {
    const primes = getPrimes(n)
    
    for (const prime of primes) {
      sumByPrimes[prime] = (sumByPrimes[prime] || 0) + n
    }
  }
  return Object.entries(sumByPrimes).map(([k, v]) => [parseInt(k), v])
}
________________________________________________
function getPrimes(limit: number) {
  let primes: boolean[] = [false, false]
  
  for (let i = 2; i <= limit; i++) {
    primes[i] = true;
  }
  
  const sieve_limit = Math.sqrt(limit);

  for (let i = 2; i <= sieve_limit; i++) {
    if (primes[i]) {
      for (let n = i * i; n <= limit; n += i) {
        primes[n] = false
      }
    }
  }

  return primes
}

function getLargestNumber(list: number[]) {

  let largest_n = 0;

  list.forEach(i => {
    if (i > largest_n) {
      largest_n = i
    }
    if (-i > largest_n) {
      largest_n = -i
    }
  })

  return largest_n
}

export function sumOfDivided(list: number[]): number[][] {
  const result: [number, number][] = [];

  getPrimes(getLargestNumber(list)).forEach((isPrime, prime) => {
    if (isPrime) {
      let isFactor = false;
      let sum = 0;
      list.forEach(n => {
        if (n % prime === 0) {
          isFactor = true;
          sum += n;
        }
      })
      if (isFactor){
        result.push( [prime, sum])
      }
    }
  })

  return result
}
________________________________________________
export interface PrimeDecomp {
  prime: number,
  time: number
}

export interface NumberDecomp {
  num: number,
  decompose: PrimeDecomp[]
}
export interface SumOfDivided {
  prime: number,
  sum: number,
}

export function sumOfDivided(lst: number[]): number[][] {
  let numDecomps = lst.map<NumberDecomp>(num=>{
    return {num: num, decompose: decompose(num)}
  })
  let sumOfDivided : SumOfDivided[] = [];
  numDecomps.forEach(numDecomp => {
    numDecomp.decompose.forEach(primeDecomp=>addTosumOfDivided(numDecomp.num, primeDecomp.prime, sumOfDivided));
  })
  return sumOfDivided
    .sort((a,b)=>a.prime-b.prime)
    .map(sumOfDivided => [sumOfDivided.prime, sumOfDivided.sum])
}

export function decompose(num: number): PrimeDecomp[] {
  if (num < 0) num*=-1;
  let currentDivider = 2;
  let remaining = num;
  let primeDecomps: PrimeDecomp[] = [];
  while(remaining>=currentDivider) {
    if (remaining%currentDivider==0){
      remaining=remaining/currentDivider;
      addToDecomp(currentDivider, primeDecomps);
    } else {
      currentDivider++;
    }
  }


  return primeDecomps;
}

export function addToDecomp(prime: number, primeDecomps: PrimeDecomp[] ): PrimeDecomp[] {
  let primeFactor = primeDecomps.find(primeDecomp => primeDecomp.prime == prime);
  if (primeFactor) {
    primeFactor.time++
  } else {
    primeDecomps.push({prime: prime, time: 1})
  }
  return primeDecomps;
}

export function addTosumOfDivided(num: number, prime: number, sumOfDivided: SumOfDivided[]): SumOfDivided[] {
  let sumOfPrime = sumOfDivided.find(sumOfd=> sumOfd.prime==prime);
  if (sumOfPrime) {
    sumOfPrime.sum += num;
  } else {
    sumOfDivided.push({prime: prime, sum: num});
  }
  return sumOfDivided;
}
