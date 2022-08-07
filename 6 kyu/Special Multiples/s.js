55e785dfcb59864f200000d9


function countSpecMult(n, mxval) {
  var  next = 1
  ,  primes = [2]
  , product = 2;

  while (primes.length < n) {
    next += 2;

    if (!primes.every(p => next % p))
      continue;

    primes.push(next);
    product *= next; 
  }

  return mxval / product | 0;
}
_________________________________
var primes=[2,3,5,7,11,13,17,19,23];
var countSpecMult=(n,m)=>(m/primes.slice(0,n).reduce((p,c)=>p*c,1))|0;
_________________________________
const prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

function countSpecMult(n, mxval) {
  const prod = prime.slice(0, n).reduce((a, b) => a * b, 1)
  return ~~(mxval / prod)
}
