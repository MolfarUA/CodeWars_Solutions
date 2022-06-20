55e7d9d63bdc3caa2500007d


function gcd(a, b) {
  return b ? gcd(b, a % b) : Math.abs(a);
}

function lcm(a, b) {
  return Math.abs(a * b) / gcd(a, b);
}

function smallest(n) {
  return n == 1 ? 1 : lcm(n, smallest(n - 1));
}
________________________________
function smallest ( n ) {
   function out(x, y){
     return y === 0 ? x : out(y, x % y);
   } 
   return Array.from({length: n}, (_, i)=> i + 1).reduce((a, b) => (a * b) / out(a, b));
}
________________________________
function smallest(n) {
  var l=1;
  for(var i=2;i<=n;i++)
    l *= i / ((a, b) => {
        while(b > 0) { a %= b; if (a == 0) return b; b %= a; }
        return a;
      })(l, i);
  return l
}
