586beb5ba44cfc44ed0006c3



sumEvenNumbers = input => input.filter(x => x % 2 == 0).reduce((x, y) => x + y, 0)
_______________________________________
function sumEvenNumbers(input) {
  return input.filter(function(el) {
    return el % 2 == 0;
  }).reduce(function(a, b) {
    return a + b;
  });
}
_______________________________________
const sumEvenNumbers = a => a.reduce((r, e) => r + (e % 2 ? 0 : e), 0);
_______________________________________
const sumEvenNumbers = (input) => input.reduce((acc, cur) => cur % 2 === 0 ? cur + acc : acc, 0);
