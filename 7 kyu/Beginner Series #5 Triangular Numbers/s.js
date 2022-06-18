56d0a591c6c8b466ca00118b


function isTriangular(t) {
  return Math.sqrt(8*t + 1) % 1 == 0;
}
__________________________
function isTriangular(t) {
  var i=1, s=0;
  while (s<t)
    s+=i++;
  return s==t;
}
__________________________
function isTriangular(t) {
  const trN = x => x * (x + 1) / 2
  return Array.from({length: 32769}, (_,i)=> trN(i+1)).includes(t)
}
__________________________
function isTriangular(t) {
  for (let i = 1,n = 1;i<=t; n++){
    i = n*(n+1)/2;
    if (i==t) return true
  }
  return false;
}
__________________________
const isTriangular = t =>
  Number.isInteger((1 + (t << 3)) ** .5);
__________________________
function isTriangular(t) {
 let c = - t;
  let D = 0.25-2*c;
 let x= -0.5+Math.sqrt(D);
return x % 1 === 0 ? true: false;
  
}
__________________________
function isTriangular(t) {
  var i;
  if (t === 1) return true;
  if (t === 3) return true;
  for (i = 1; i <= (t / 2); i++) {
    if (i * (i + 1) / 2 === t) return true;
  }
  return false;
}
