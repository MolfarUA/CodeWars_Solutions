function pairZeros(arr) {
  var seenZero = 0;
  return arr.filter(function(num){
    return num != 0 || seenZero++ % 2 == 0;
  });
}
_____________________________________
var pairZeros = (a, f) => a.filter(n => n || (f = !f));
_____________________________________
function pairZeros(a, f) {
  return a.filter(function(n) { return (n != 0 || (f = !f)); });
}
_____________________________________
const pairZeros = (arr, flag) =>
  arr.filter(val => val || (flag = !flag));
_____________________________________
var pairZeros = arr => 
  arr
    .join('')
    .replace(/0([^0]*)0/g, '0$1')
    .split('')
    .map(Number)
