5b71af678adeae41df00008c


function shortestDistance(a, b, c) {
  const count = (x, y, z) => Math.sqrt( Math.pow(x, 2) + (y + z) ** 2 );
    return Math.min( count( a, b, c ), count( b, c, a ), count( c, a, b ) );
}
____________________________
function shortestDistance(a, b, c) {
  return Math.min(
    Math.hypot((a + b), c),
    Math.hypot((a + c), b),
    Math.hypot((c + b), a),
  );
}
____________________________
const shortestDistance = (...d) => Math.hypot(d.sort((a, b) => a < b)[0], d[1] + d[2]);
