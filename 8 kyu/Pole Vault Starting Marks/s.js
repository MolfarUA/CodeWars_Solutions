5786f8404c4709148f0006bf


function startingMark(bodyHeight){
  // Remember: Body height of 1.52 m --> starting mark: 9.45 m
  //           Body height of 1.83 m --> starting mark: 10.67 m
  // All other starting marks are based on these guidelines!
  
  var m = (10.67 - 9.45) / (1.83 - 1.52);
  return Math.round((10.67 + m * bodyHeight - m * 1.83) * 100) / 100;
}
____________________________________
const startingMark = bodyHeight =>
  +(bodyHeight * 3.9354 + 3.4681).toFixed(2);
____________________________________
function startingMark(bodyHeight) {
    var a = {x: 1.52, y: 9.45},
        b = {x: 1.83, y: 10.67},
        m = (b.y - a.y) / (b.x - a.x);
    return Math.round((m * bodyHeight + b.y - m * b.x) * 100) / 100;
}
____________________________________
const startingMark = (x) => {
  const m = 3.93548;
  const b = 3.46806;
  const y = m*x + b;
  return Math.round(y * 100) / 100;
};
