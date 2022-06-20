58cb43f4256836ed95000f97


function find_difference(a, b) {
  return Math.abs(a.reduce((previous, current) => previous * current) - b.reduce((previous, current) => previous * current));
}
________________________
function find_difference(a, b) {
  return Math.abs(a[0]*a[1]*a[2]-b[0]*b[1]*b[2]);
}
________________________
function volume(c) {
  return c.reduce((x, y) => x * y);
}

function find_difference(a, b) {
  return Math.abs(volume(a) - volume(b));
}
