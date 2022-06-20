58e230e5e24dde0996000070


const nextPrime = (n) => isPrime(n + 1) ? n + 1 : nextPrime(n + 1);

const isPrime = (n) => {
  if (n < 2) {
    return false;
  }
  
  for (var i = 2; i <= Math.sqrt(n); i++) {
    if (n % i === 0) {
      return false;
    }
  }
  
  return true;
}
__________________________
function isPrime(n) {
    if (n < 2) {
        return false;
    }
  for (let i = 2; i * i <= n; i++) {
    if (n % i === 0) {
      return false;
    }
  }
  return true;
}

function nextPrime(n) {
  let prime = n + 1;
  while (!isPrime(prime)) {
    prime += 1;
  }
  return prime;
}
__________________________
function nextPrime(n){
  if (n === 0) return 2
  if (n === 1) return 2
  

    n % 2 === 0 ? n += 1 : n += 2
    let i = 3
    for (; i <= Math.sqrt(n); i += 1) {
      if (n % i === 0) {
        if (n !== i) {
          i = 1
          n += 1
        } else if (n === i) {
          break
        }
      } 
    }
  return n
}
