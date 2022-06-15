function f(n) {
    var prime,c;
    var maxCount = 0;
    var superMax = (n-1).toString().length -1;
    for(i=n-1;i>1;i--){
      if(isPrime(i)){
        c = countEven(i);
        if(c >maxCount){
          maxCount = c;
          prime = i;
        }
      }
      if(maxCount == superMax ){
         return  prime;
      }
    }
   return prime;
}

function isPrime(k){
  for(j=2;j<=Math.sqrt(k);j++){
    if(k%j==0){
      return false;
    }
  }
  return true;
}

function countEven(n){
  return (n.toString().match(/[02468]/g)||[]).length;
}
____________________________________________
function f(n) {
  let maxEvens = 0;
  let ans = 0;

  for (let i = n - 1; i > 2; i--) {
    if (isPrime(i)) {
      if (maxEvens < countEvenNums(i)) {
        maxEvens = countEvenNums(i);
        ans = i;
      }
    }

    if (numberOfDigits(i) - 1 <= maxEvens) {
      break;
    }
  }

  return ans;
}

function numberOfDigits(n) {
  let counter = 1;
  while (true) {
    if (Math.floor(n / 10 ** counter++) === 0) return counter - 1;
  }
}

function isPrime(n) {
  if (n % 2 === 0) return false; // Not to deal with dividing by even numbers
  for (let i = 3; i * i < n + 1; i+= 2) {
    if (n % i === 0) return false;
  }

  return true;
}

function countEvenNums(n) {
  let counter = 0;
  while (n > 0) {
    if ((n % 10) % 2 === 0) counter++;
    n = Math.floor(n / 10);
  }

  return counter;
}
____________________________________________
let evenDigitCount = function(n) {
  return [...String(n)].filter(d=>"02468".includes(d)).length;
}

let eratosthenes = function(n) {
  let xs = new Array(n);
  for (let i=2; i<=n; i++) xs[i] = true;
  for (let i=2; i<=n; i++) if (xs[i]) for (let j=i*2; j<=n; j+=i) xs[j] = false;
  return xs.map((e,i) => [e,i]).filter(e => e[0]).map(([e,i]) => i);
};

let PRIMES = eratosthenes(5000000);
let PED = PRIMES.reduce((acc,p) => {
  acc.set(p, evenDigitCount(p));
  return acc;
}, new Map());

function f(n) {
  var a,b;
  for (let p of PRIMES) {
    if (p >= n) break;
    let c = PED.get(p);
    if (a == null || c >= a) [a,b] = [c,p];
  }
  return b;
}
