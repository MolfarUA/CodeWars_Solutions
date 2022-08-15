52f677797c461daaf7000740


const gcd = (a,b)=>a?gcd(b%a,a):b
function solution(numbers) {
  return numbers.reduce(gcd)*numbers.length
}
_______________________________
const gcd = (a, b) =>
  b ? gcd(b, a % b) : a;

const solution = numbers =>
  numbers.length * numbers.reduce(gcd);
_______________________________
function solution(numbers) {
  return numbers.length * numbers.reduce((p, c) => gcd(p, c));
}

function gcd(a, b)  {
  if (b === 0) return a;
  else return gcd(b, a % b);
}
