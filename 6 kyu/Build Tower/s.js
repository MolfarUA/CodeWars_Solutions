576757b1df89ecf5bd00073b


function towerBuilder(n) {
  return Array.from({length: n}, function(v, k) {
    const spaces = ' '.repeat(n - k - 1);
    return spaces + '*'.repeat(k + k + 1) + spaces;
  });
}
_____________________________
function towerBuilder(nFloors) {
  var tower = [];
  for (var i = 0; i < nFloors; i++) {
    tower.push(" ".repeat(nFloors - i - 1)
             + "*".repeat((i * 2)+ 1)
             + " ".repeat(nFloors - i - 1));
  }
  return tower;
}
_____________________________
function towerBuilder(nFloors) {
  return Array(nFloors).fill(null).map(
    (el, i)=>([
      ...Array(nFloors-i-1).fill(' '),
      ...Array(2*i+1).fill('*'),
      ...Array(nFloors-i-1).fill(' ')
    ]).join('')
  )
}
_____________________________
function towerBuilder(nFloors) {
  const build = []
  let step = 0
  for(let i = 1 ; i <= nFloors; i++){
      build.push(new Array(i + step).fill('*').join(''))
    step +=1
    
  }
  const result = []
  for(let item of build){
    const space = new Array(step-1).fill(' ').join('')
    result.push(space + item + space)
    step-= 1
  }
  return result
}
_____________________________
function towerBuilder(nFloors) {
  if (nFloors === 1) {
    return ['*'];
  }
let string1 = '*'
let string2 = '**'
let result = []
for (let i = 0; i < nFloors-1; i++) {
  if (result.length===0) {
    result.push (string1)
  }
  string1 = string1.concat(string2)
  result.push (string1)
}

for (let i = 0; i < result.length; i++) {
 result[i] = Array(result[i]) 
}

for (let i = 0; i < result.length; i++) {
  for (let j = 0; j < result[i].length; j++){
   while (result[i][j].length !== result.slice(-1).toString().length) {
    result[i][j] = result[i][j] + ' '
    result[i][j] = ' ' + result[i][j]
    } 
  }
 result[i] = result[i].toString();
 }

return result
  }
_____________________________
function towerBuilder(nFloors) {
  let result = []

  for (let i = 0; i < nFloors; i++) {
    let spaces = (" ").repeat(nFloors - i - 1)
    let stars = ("*").repeat(i * 2 + 1)
    result.push(spaces + stars + spaces)
  }

  return result
}
_____________________________
function towerBuilder(nFloors){
  let stars = [];
  
  for (let i = 0; i < nFloors; i++) {
    
    let spaceNum = nFloors - i - 1
    let space = " ".repeat(spaceNum)
    let num = 2 * i + 1
    let blocks = "*".repeat(num)
    stars[i] = space + blocks + space
  }
  return stars
}
