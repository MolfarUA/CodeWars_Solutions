559b8e46fa060b2c6a0000bf


const f = n => 
  n > 1 ? n * f(n - 1) : n;

const diagonal = (n, p) => 
  Math.round(f(n + 1) / f(p + 1) / f(n - p));
_____________________________
const fact = n => eval([...Array(n + 1).keys()].slice(1).join('*'));
const choose = (n, k) => Math.round(fact(n) / (fact(k) * fact(n - k)));
const diagonal = (n, p) => choose(n + 1, p + 1);
_____________________________
function diagonal(n, p) {
  const f = a => a > 1 ? a * f(a - 1) : a == 0 ? 1 : a;
  let sum = 0;

  for (let i = p; i <= n; i++) {
    sum += f(i) / (f(p) * f(i - p));
  }

  return sum;
}
