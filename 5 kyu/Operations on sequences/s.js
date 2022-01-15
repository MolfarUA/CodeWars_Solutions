const BN = require('bignumber.js')

function solve(arr) {

  let [ a, b ] = [ BN(0), BN(1) ];
  
  for (let i = 0; i < arr.length; i += 2) 
    [ a, b ] = [ 
      a.times(arr[i]).minus(b.times(arr[i + 1])), 
      b.times(arr[i]).plus(a.times(arr[i + 1])) 
    ];
  
  return [ a.abs(), b.abs() ];
  
}
_____________________________________
const BN = require('bignumber.js')

function solve(arr) {
    function h(a) {
        let 
          x = new BN(a[0]), 
          y = new BN(a[1]), 
          z = new BN(a[2]), 
          t = new BN(a[3]);
        let p = x.multipliedBy(z).minus(y.multipliedBy(t));
        let q = x.multipliedBy(t).plus(y.multipliedBy(z));
        let res = [p.abs(), q.abs()];
        return res;
    }
    if (arr.length == 4)
        return h(arr);
    return solve( h(arr.slice(0,4)).concat(arr.slice(4,arr.length)));
}
_____________________________________
const BN = require("bignumber.js");

const solve = (arr) => {
  let [a, b] = [BN(0), BN(1)];

  for (let i = 0; i < arr.length; i += 2)
    [a, b] = [
      a.times(arr[i]).minus(b.times(arr[i + 1])),
      b.times(arr[i]).plus(a.times(arr[i + 1])),
    ];

  return [a.abs(), b.abs()];
};
_____________________________________
const BN = require('bignumber.js');

function solve(p) {
    let [a, b] = solver(BigInt(p[0]), BigInt(p[1]), BigInt(p[2]), BigInt(p[3]));
    for (let i = 4 ; i < p.length ; i += 2) {
        [a, b] = solver(a, b, BigInt(p[i]), BigInt(p[i + 1]));
    }
    return [a, b];
}

function solver(a, b, c, d) {
    return [a * c + b * d, abs(a * d - b * c)];
}

function abs(x) {
    return x > 0n ? x : -x;
}
