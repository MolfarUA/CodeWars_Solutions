536a155256eb459b8700077e


function createSpiral(n) {
  if (!Number.isInteger(n)||n<1) return [];
  var rs=[...Array(n)].map(x=>[...Array(n)].map(x=>0));
  rs[0][0]=1;
  for (var i=2,xx=0,yy=0;i<=n*n;) {
    while (yy+1<n&&rs[xx][yy+1]==0) rs[xx][++yy]=i++;
    while (xx+1<n&&rs[xx+1][yy]==0) rs[++xx][yy]=i++;
    while (yy-1>-1&&rs[xx][yy-1]==0) rs[xx][--yy]=i++;
    while (xx-1>-1&&rs[xx-1][yy]==0) rs[--xx][yy]=i++;
  }
  return rs;
}
_________________________
const _ = require('underscore');
const DIRECTIONS = _.range(4);

const nextDir = (dir) => (dir + 1) % DIRECTIONS.length;

const nextXY = (dir, x, y) => {
  if(dir === 0) return [x+1, y]; // right
  if(dir === 1) return [x, y+1]; // down
  if(dir === 2) return [x-1, y]; // left
  if(dir === 3) return [x, y-1]; // up
}

const canMove = (board, dir, x, y) => {
  const [nx, ny] = nextXY(dir, x, y);
  return board[ny] && board[ny][nx] === 0;
}

const move = (board, dir = 0, x = 0, y = 0, val = 1) => {
  board[y][x] = val;
  if (!_.any(DIRECTIONS, (d) => canMove(board, d, x, y))) return;
  if(canMove(board, dir, x, y)) {
    [x, y] = nextXY(dir, x, y);
    val += 1;
  } else {
    dir = nextDir(dir);
  }
  move(board, dir, x, y, val);
}

const createSpiral = (n) => {
  if(!Number.isInteger(n) || n < 1) return [];
  const board = _.times(n, () => Array(n).fill(0));
  move(board);
  return board;
}
_________________________
function createSpiral(N) {
  if(N < 1 || !Number.isInteger(N)) return [];
  let result = Array.from(Array(N), a => Array.from(Array(N)));
  let matrix = result.map((row, rowIdx)=>row.map((col, colIdx)=>[rowIdx, colIdx]));
  let transpose = array => array[0].map((x,i) => array.map(x => x[i])).reverse();
  let counter = 0, cells = N+N;
  
  while(--cells) {
    matrix.splice(0, 1)[0].forEach(([row, col]) => result[row][col] = ++counter);
    matrix = matrix.length && transpose(matrix);
  }
  
  return result;
}
