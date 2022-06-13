function powersOfTwo(n){
  var result = [];
  for (var i = 0; i <= n; i++) {
    result.push(Math.pow(2, i));
  }
  return result;
}
___________________________________
function powersOfTwo(n) {
  return Array.from({length: n + 1}, (v, k) => 2 ** k);
}
___________________________________
function powersOfTwo(n){
  var arr = [];
  
  for (var i=0; i<=n; ++i){
    arr.push(Math.pow(2, i));
  }
  
  return arr;
}
___________________________________
function powersOfTwo(n) {
  return [...Array(n + 1)].map((_, i) => 2 ** i)
}
___________________________________
var powersOfTwo = n => Array.from({length : n + 1}, (val, i) => Math.pow(2, i));
