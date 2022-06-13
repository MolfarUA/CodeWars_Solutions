function findNb(m) {
  var n = 0
  while (m > 0) m -= ++n**3
  return m ? -1 : n
}
_________________________________________
function findNb(m) {
  let n = 0;
  let sum = 0;
  while (sum < m) {
    n++;
    sum += Math.pow(n, 3);
  }
  return sum === m ? n : -1;
}
_________________________________________
function findNb(m) {
  let n = Math.sqrt( Math.sqrt(m)*2 + 0.25 ) - 0.5
    return Number.isInteger(n) ? n : -1
}
_________________________________________
var findNb = m =>
{
  var n = Math.floor((4*m)**.25);
  var sum = x => (x*(x+1)/2)**2;
  return sum(n) == m ? n : -1;
}
