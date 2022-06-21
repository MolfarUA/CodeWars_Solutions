5870fa11aa0428da750000da


function execute(code) {
  code = code.replace(/[LFR]\d+/g, (m) => m[0].repeat(+m.slice(1)));
  
  let  i = 0,  j = 0,
      di = 0, dj = 1,
      grid = [["*"]],
      rows, cols;

  for (let k = 0; k < code.length; k++) {
    rows = grid.length;
    cols = grid[0].length;
    
    switch(code[k]) {
      case("F"):
        [i,j] = [i+di, j+dj];
        if (i < 0)     grid = [Array(cols).fill(" "), ...grid];
        if (i >= rows) grid = [...grid, Array(cols).fill(" ")];
        if (j < 0)     grid = grid.map(row => [" ", ...row]);
        if (j >= cols) grid = grid.map(row => [...row, " "]);
        i = Math.max(0, i);
        j = Math.max(0, j);
                                      break;
      case("L"): [di,dj] = [-dj, di]; break;
      case("R"): [di,dj] = [ dj,-di]; break;
    }

    grid[i][j] = "*";
  }
  
  return grid.map(row => row.join("")).join("\r\n");
}
__________________________
function execute(code) {
  var y = 0, x = 0, d = 1, minY = 0, minX = 0, maxY = 0, maxX = 0;
  const P = [[y,x]], L = [2,0,3,1], R = [1,3,0,2];
  for (const c of code.match(/[FLR]\d*/g) || []) {
    let n = c.length > 1 ? +c.slice(1) : 1;
    switch (c[0]) {
      case 'L': do d = L[d]; while (--n > 0); break;
      case 'R': do d = R[d]; while (--n > 0); break;
      case 'F':
        switch (d) {
          case 0: do P.push([--y, x]); while (--n > 0); if (y < minY) minY = y; break;
          case 1: do P.push([y, ++x]); while (--n > 0); if (x > maxX) maxX = x; break;
          case 2: do P.push([y, --x]); while (--n > 0); if (x < minX) minX = x; break;
          case 3: do P.push([++y, x]); while (--n > 0); if (y > maxY) maxY = y; break;
        }
    }
  }
  const h = maxY - minY + 1, w = maxX - minX + 1;
  const M = Array.from({length: h}, _ => Array.from({length: w}, _ => ' '));
  for (const [y, x] of P) M[y - minY][x - minX] = '*';
  return M.map(r => r.join('')).join('\r\n');
}
__________________________
const TURN_LEFT = {
  UP: 'LEFT',
  LEFT: 'DOWN',
  DOWN: 'RIGHT',
  RIGHT: 'UP',
}

const TURN_RIGHT = Object.entries(TURN_LEFT).reduce((acc, [k, v]) => ({ ...acc, [v]: k }), {})

const DIRECTIONS = { UP: 'UP', RIGHT: 'RIGHT', DOWN: 'DOWN', LEFT: 'LEFT' }

const DIRECTIONS_VALUE = {
  RIGHT: [0, 1],
  UP: [-1, 0],
  LEFT: [0, -1],
  DOWN: [1, 0],
}

const createField = (minX, maxX, minY, maxY) => (
  [...Array(maxY - minY + 1)].map(() => [...Array(maxX - minX + 1)])
)

const execute = (code) => {
  const robot = new Robot()
  ;(code.match(/(\w(\d*))/g) || []).forEach((match) => {
    const [letter, repetitions] = [match[0], match.substring(1) || 1]
    for (let i = 0; i < repetitions; i++) {
      robot.parse(letter)
    }
  })
  return robot.history
    .reduce((acc, [originalY, originalX]) => {
      const [x, y] = [originalX - robot.minX, originalY - robot.minY]
      if (!acc[y]) acc[y] = []
      acc[y][x] = '*'
      return acc
    }, createField(robot.minX, robot.maxX, robot.minY, robot.maxY))
    .map(row => [...row].map(x => x || ' ').join(''))
    .join('\r\n')
}

class Robot {
  constructor() {
    this.position = [0, 0]
    this.direction = DIRECTIONS.RIGHT
    this.minX = 0
    this.maxX = 0
    this.minY = 0
    this.maxY = 0
    this.history = [this.position]
  }

  parse(letter) {
    switch (letter) {
      case 'F':
        this.move()
        break
      case 'R':
        this.turn(TURN_RIGHT)
        break
      case 'L':
        this.turn(TURN_LEFT)
        break
      default:
        throw new Error(`Invalid input: ${letter}`)
    }
  }

  turn(directionMap) {
    this.direction = directionMap[this.direction]
  }

  move() {
    const x = this.position[1] + DIRECTIONS_VALUE[this.direction][1]
    const y = this.position[0] + DIRECTIONS_VALUE[this.direction][0]
    if (x < this.minX) this.minX = x
    if (x > this.maxX) this.maxX = x
    if (y < this.minY) this.minY = y
    if (y > this.maxY) this.maxY = y
    this.position = [y, x]
    this.history.push(this.position)
  }
}
