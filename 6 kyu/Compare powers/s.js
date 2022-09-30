55b2549a781b5336c0000103


function comparePowers([b1, e1], [b2, e2]) {
  let d = Math.log(b2) * e2 - Math.log(b1) * e1;
  return (d > 0) - (d < 0);
}
________________________________
var comparePowers = (n1, n2) => {var c = n2[1] * Math.log(n2[0]) - n1[1] * Math.log(n1[0]); return c < 0 ? -1 : c > 0 ? 1 : 0;}
________________________________
const comparePowers = ([a, n], [b, m]) => Math.sign(b - a ** (n / m));
