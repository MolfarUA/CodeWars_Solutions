58475cce273e5560f40000fa


f=a=>!(Math.sqrt(a)%1)?Math.sqrt(a):f(a-1);
approxRoot=(a)=>(b=>+(b+(a-b**2)/((b+1)**2-b**2)).toFixed(2))(f(a));
____________________________
function approxRoot(n) {
  var k=0;
  while (k*k<n)
    k++;
  return +((k-1)+((n-(k-1)*(k-1))/(k*k-(k-1)*(k-1)))).toFixed(2)
}
____________________________
function approxRoot(n) {
  const base = Math.sqrt(n), floor = Math.floor(base), ceil = Math.ceil(base);
  return Number.isInteger(Math.sqrt(n))
    ? Math.sqrt(n)
    : +(floor + (n - floor * floor) / (ceil * ceil - floor * floor)).toFixed(2)
}
