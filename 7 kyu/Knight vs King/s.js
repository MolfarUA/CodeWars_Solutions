564e1d90c41a8423230000bc


function knightVsKing(knightPosition, kingPosition) {
  var diffX = Math.abs(knightPosition[1].charCodeAt() - kingPosition[1].charCodeAt());
  var diffY = Math.abs(knightPosition[0] - kingPosition[0]);
  
  if (diffX <= 1 && diffY <=1) {
    return 'King'
  } else if (diffX == 1 && diffY == 2 || diffX == 2 && diffY == 1) {
    return 'Knight'
  } 
  return 'None';
}
_______________________________________
function knightVsKing([x1, y1], [x2, y2]) {
  let dx = x2 - x1, dy = y2.charCodeAt() - y1.charCodeAt(), d = dx * dx + dy * dy;
  return d == 5 ? 'Knight' : d < 3 ? 'King' : 'None';
}
_______________________________________
const knightVsKing = ([ kN, kL ], [ bN, bL ]) => {
  [ kL, bL ] = [kL, bL].map(ch => ch.charCodeAt(0) - 64);
  const [ dx, dy ] = [ Math.abs(kN-bN), Math.abs(kL-bL) ];
  console.log(dx,dy)
  return dx && dy && dx+dy === 3 ? "Knight" : dx && dy && dx+dy === 2 || dx+dy === 1 ? "King" : "None";
}
