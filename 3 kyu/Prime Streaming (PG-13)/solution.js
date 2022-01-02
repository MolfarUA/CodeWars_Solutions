class Primes {
  static * stream() {
  yield 2 
  var n = 3
   while (true) {
     if (isPrime(n)) {
       yield n
     }
     n += 2
   }
  }
}

function isPrime(n) {
  for (var a = 3; a <= ~~Math.sqrt(n); a+=2) {
    if (n%a == 0) return false;
    }
  return true;
}
___________________________________________________________
class Primes {
  static *stream() {
      yield 2; yield 3; yield 5; yield 7;
      let map = new Map();
      let gen = Primes.stream();
      gen.next() && gen.next();
      let x = 3; let i = 7;
      while (true) {
        i+=2;
        let val = map.get(i) || -1;
        if (val > -1) map.delete(i);
        else if (i < x*x){
          yield i;
          continue;
        }
        else {
          val = x*2;
          x = gen.next()['value'];
        }
        let key = i + val;
        while (map.has(key)) key+=val;
        map.set(key, val);
      }
  }
}
___________________________________________________________
limit = 15495863
const sieve = [0,0].concat(new Array(limit-2).fill(1))
const sl = sieve.length
const already_set = []
class Primes {
  static * stream() {
      for (let i=0;i<sl;i++){
        if (sieve[i]){
           yield i
           if (!already_set[i]){
             already_set[i]==1
             for (let k = i*i;k<limit;k+=i) sieve[k] = 0
            }
        }
      }
  }
}
___________________________________________________________
const isPrime = function(n) {
  if (n <= 3) {
    return n > 1;
  } else if (n % 2 === 0 || n % 3 === 0) {
    return false;
  }
  
  let i = 5;
  const sqrt = parseInt(Math.sqrt(n));
  while (i <= sqrt) {
    if (n % i === 0 || n % (i + 2) === 0)
      return false;
    i += 6;
  }
  
  return true;
}

class Primes {
  static * stream() {
    let i = 2;
    while (true) {
      if (isPrime(i))
        yield i;
      i++;
    }
  }
}
