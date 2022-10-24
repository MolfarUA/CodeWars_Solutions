5a2a597a8882f392020005e5

function bloxSolver (map) {
  const initialPosition = findPosition(map, 'B')
  const exit = findPosition(map, 'X')

  let variants = [{
    position: initialPosition,
    path: [],
  }]
  const cache = {}
  while (variants.length) {
    const nextVariants = []
    for (let j = 0; j < variants.length; j++) {
      const variant = variants[j]
      const [x1, y1, x2, y2] = variant.position

      if (isPositionsEqual(variant.position, exit)) return variant.path.join('')

      for (let i = 0; i < 4; i++) {
        const d = [-1, 1, 1, -1][i]
        const [a1, a2, b1, b2] = [[y1, y2, x1, x2], [x1, x2, y1, y2]][i % 2]
        const a = d > 0 ? Math.max(a1, a2) : Math.min(a1, a2)
        const k = (Math.abs(1 - Math.abs(a1 - a2)) - Math.abs(b1 - b2)) * d
        const position = [[b1, a + d, b2, a + d + k], [a + d, b1, a + d + k, b2]][i % 2]
        const path = variant.path.concat(['U', 'R', 'D', 'L'][i])
        const key = position.join('')

        if (!cache[key] && isPositionValid(map, position)) {
          cache[key] = true
          nextVariants.push({
            position,
            path,
          })
        }
      }
    }
    variants = nextVariants
  }
  return ''
}

function findPosition (map, el) {
  for (let y = 0; y < map.length; y++) for (let x = 0; x < map[y].length; x++) {
    if (map[y][x] === el) return [x, y, x, y]
  }
}

function get (map, x, y) {
  return map[y] && map[y][x]
}

function isPositionValid (map, position) {
  const [x1, y1, x2, y2] = position
  return !(['0', undefined].includes(get(map, x1, y1)) || ['0', undefined].includes(get(map, x2, y2)))
}

function isPositionsEqual (position1, position2) {
  for (let i = 0; i < 4; i++) {
    if (position1[i] !== position2[i]) return false
  }
  return true
}
_________________________________
class Square {
  constructor() {
    if (arguments.length == 1 && arguments[0] instanceof Square) {
      this.copy(arguments[0]);
    } else {
      this.set(...arguments);
    }
  }
  rotX(x) {
    let dz = this.z;
    let dx = this.x - x;
    this.x = x + (dx < 0 ? dz : -dz);
    this.z = Math.abs(dx) - 1;
    return this;
  }
  rotY(y) {
    let dz = this.z;
    let dy = this.y - y;
    this.y = y + (dy < 0 ? dz : -dz);
    this.z = Math.abs(dy) - 1;
    return this;
  }
  set(x,y,z) {
    this.x = x || 0;
    this.y = y || 0;
    this.z = z || 0;
    return this;
  }
  copy(other) {
    this.set(other.x, other.y, other.z);
    return this;
  }
  clone() {
    return new Square(this);
  }
  hashXY() {
    return `${this.x}:${this.y}`;
  }
}

class Block {
  constructor() {
    if (arguments.length == 1 && arguments[0] instanceof Block) {
      this.copy(arguments[0]);
    } else {
      this.set(...arguments);
    }
  }
  init(x,y) {
    this.p1.x = this.p2.x = x;
    this.p1.y = this.p2.y = y;
    this.p1.z = 0;
    this.p2.z = 1;
  }
  rollLeft() {
    let x = Math.min(this.p1.x, this.p2.x) - 1;
    this.p1.rotX(x);
    this.p2.rotX(x);
    return this;
  }
  rollRight() {
    let x = Math.max(this.p1.x, this.p2.x) + 1;
    this.p1.rotX(x);
    this.p2.rotX(x);
    return this;
  }
  rollUp() {
    let y = Math.min(this.p1.y, this.p2.y) - 1;
    this.p1.rotY(y);
    this.p2.rotY(y);
    return this;
  }
  rollDown() {
    let y = Math.max(this.p1.y, this.p2.y) + 1;
    this.p1.rotY(y);
    this.p2.rotY(y);
    return this;
  }
  set(p1,p2) {
    if (this.p1 == null) this.p1 = new Square();
    if (this.p2 == null) this.p2 = new Square();
    this.p1.copy(p1 || new Square());
    this.p2.copy(p2 || new Square());
    return this;
  }
  setP1(x,y,z) {
    this.p1.set(x,y,z);
    return this;
  }
  setP2(x,y,z) {
    this.p2.set(x,y,z);
    return this;
  }
  copy(other) {
    this.set(other.p1, other.p2);
    return this;
  }
  clone() {
    return new Block(this);
  }
  hashXY() {
    let ps = [this.p1, this.p2].sort((a,b)=>a.x-b.x||a.y-b.y||a.z-b.z);
    let [a,b] = ps;
    return `${a.hashXY()};${b.hashXY()}`;
  }
}

class Board {
  constructor(grid) {
    this.grid = grid;
    this.h = grid.length;
    this.w = grid[0].length;
    this.init();
  }
  init() {
    this.block = new Block();
    this.exit = null;
    for (let y=0; y<this.h; y++) {
      for (let x=0; x<this.w; x++) {
        switch (this.grid[y][x]) {
          case 'B': this.block.init(x,y); break;
          case 'X': this.exit = [y,x]; break;
        }
      }
    }
  }
  fits(comp) {
    if (comp instanceof Square) {
      return comp.x>=0 && comp.y>=0 && comp.x<this.w && comp.y<this.h 
        && '1BX'.includes(this.at(comp));
    } else if (comp instanceof Block) {
      return this.fits(comp.p1) && this.fits(comp.p2);
    } else {
      return false;
    }
  }
  at(p) {
    return this.grid[p.y][p.x];
  }
  completes(b) {
    return this.at(b.p1)=='X' && this.at(b.p2)=='X' ;
  }
}

function bloxSolver(arr) {
  let board = new Board(arr);
  let queue = [];
  let seen = new Set();
  let moves = [
    ['U', b => b.rollUp()],
    ['D', b => b.rollDown()],
    ['L', b => b.rollLeft()],
    ['R', b => b.rollRight()]
  ];
  queue.push([board.block, []]);
  while (queue.length) {
    let [block, path] = queue.shift();
    let hash = block.hashXY();
    if (seen.has(hash)) 
      continue;
    seen.add(hash);
    if (!board.fits(block)) 
      continue;
    if (board.completes(block)) 
      return path.join``;
    for (let [sym,move] of moves) {
      queue.push([move(block.clone()), path.concat([sym])]);
    }
  }
  return null;
}
_________________________________
const moves = {
  up: {
    U: (x, y) => [x, y-2,x, y-1,'vert'],
    D: (x, y) => [x, y+1,x, y+2,'vert'],
    L: (x, y) => [x-2, y,x-1, y,'horz'],
    R: (x, y) => [x+1, y,x+2, y,'horz']
    },
  vert: {
    U: (x, y) => [x, y-1,x, y-1,'up'],
    D: (x, y) => [x, y+2,x, y+2,'up'],
    L: (x, y) => [x-1, y,x-1, y+1,'vert'],
    R: (x, y) => [x+1, y,x+1, y+1,'vert']
    },
  horz: {
    U: (x, y) => [x, y-1,x+1, y-1,'horz'],
    D: (x, y) => [x, y+1,x+1, y+1,'horz'],
    L: (x, y) => [x-1, y,x-1, y,'up'],
    R: (x, y) => [x+2, y,x+2, y,'up']
    }
}
 
function bloxSolver(arr){
  let startX, startY, goalX, goalY, winner;
  for (let i = 0; i < arr.length; i++) {
    for (let j = 0; j < arr[i].length; j++) {
      if (arr[i][j] == 'B') [startY, startX] = [i, j];
      if (arr[i][j] == 'X') [goalY, goalX] = [i, j];
    }
  }
  
  const seen = new Set();
  seen.add('up,' + startX + ',' + startY); 
  
  const player = {x: startX, y: startY, state:'up', memory:[]};
  const que = [];
  const dir = [...'UDLR'];
  dir.forEach(d => que.push([d, player]));
  
  function flood(d, prevTurn) {
    const [x, y, x2, y2, state] = moves[prevTurn.state][d](prevTurn.x, prevTurn.y);
    const backtrackCheck = state + ',' + x + ',' + y;
    if (!seen.has(backtrackCheck) && arr[y] && arr[y2] && arr[y][x] && arr[y2][x2] && 
      arr[y][x] != 0 && arr[y2][x2] != 0) {
      seen.add(backtrackCheck);
      const nextTurn = {x: x, y: y, state: state, memory: prevTurn.memory.concat(d)}         
      if (x == goalX && y == goalY && state == 'up') {
        winner = nextTurn
      } else {
        dir.forEach(d => que.push([d, nextTurn]));
      }      
    }
  }
  
  while(!winner) {
    const next = que.shift();
    flood(next[0], next[1]);
  }

  return winner.memory.join('')
}
_________________________________
function bloxSolver(arr){
  let end,H=arr.length,W=arr[0].length,result=false
  const q = [{rc:0,moves:''}], ext = new Set(), 
  validCoords=(coords)=> !ext.has(coords.toString()) && coords.every(([r,c])=> 0 <= c && c < W && 0 <= r && r < H && '1BX'.includes(arr[r][c]))
  arr.forEach((x,r)=>{let a=x.indexOf('B'),b=x.indexOf('X'); if (~a) q[0].rc = [[r,a]]; if (~b) end = [r,b]})
  while(q.sort((a,b)=>a.moves.length-b.moves.length).length) {
    const p = q.shift(), [r,c] = p.rc[0], [y,x] = p.rc.length === 1 ? [-1,0] : p.rc[1], 
    data = y ===-1 ? [['U',[r-2,c],[r-1,c]], ['D',[r+1,c],[r+2,c]], ['L',[r,c-1],[r,c-2]], ['R',[r,c+2],[r,c+1]]] :
           c === x ? [['U',[r-1,c]],         ['D',[y+1,c]],         ['L',[r,c-1],[y,c-1]], ['R',[r,c+1],[y,c+1]]] :
                     [['U',[r-1,c],[r-1,x]], ['D',[r+1,c],[r+1,x]], ['L',[r,x-1]],         ['R',[r,c+1]]]
    if (p.rc.toString() === end.toString() &&(result===false || p.moves.length < result.length)) result = p.moves
    ext.add(p.rc.toString())
    for (let [d,...coords] of data)
      if (validCoords(coords)) 
        q.push({rc:coords.slice(), moves:p.moves+d})
  }
  return result
}
