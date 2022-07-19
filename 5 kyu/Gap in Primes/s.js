561e9c843a2ef5a40c0000a4


function gap(g, m, n) {
    var lastPrime = 0;
    var isPrime = function(x) { 
      for (var i=2; i*i<=x; i++) { if (x % i == 0) return false; } return true;
    }
    
    for(var i = m; i <= n; i++)
        if(isPrime(i)) {
            if(i - lastPrime == g) return [lastPrime, i];
            else lastPrime = i;
        }
      
    return null;
}
__________________________________
function isPrime(n) {
   if (isNaN(n) || !isFinite(n) || n%1 || n<2) return false;
   var m = Math.sqrt(n);
   for (var i=2;i<=m;i++) if (n%i==0) return false;
   return true;
}


function gap(g, m, n) {
  let mx = 0;
  for (m, n; m < n; m++) {
    if (isPrime(m)) {
      if (m - mx === g) return [mx, m];
      mx = m;
    }
  }
  return null;
}
__________________________________
var primes = [2];
var notPrimes = [];

function gap(g, m, n) {
  if(m%2===0) m = m+1;
  for(var i = m; i < n-g; i+=2) {
    if(isPrime(i) && isPrime(i+g)) {
      var concurrent = true;
      for(var j = i+2; j<(i+g); j+=2) {
        if(isPrime(j)) { concurrent = false; break; }
      }
      if (concurrent) return [i, i+g];
    }
  }
  return null;
}

function isPrime(num) {
  if(primes.indexOf(num)!==-1) return true;
  if(notPrimes.indexOf(num)!==-1) return false;
  if(num%2===0) return false;
  if(num%3===0) return false;
  if(num%5===0) return false;
  
  for(var i = 7; i<=Math.sqrt(num); i+=2) {
    if(num%i===0) {
      notPrimes.push(num);
      return false
    }
  }
  primes.push(num);
  return true;
}
