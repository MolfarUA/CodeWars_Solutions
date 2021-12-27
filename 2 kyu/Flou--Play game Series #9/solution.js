function playFlou(gameMap){
    const m = gameMap.split`\n`.map(x=>x.split``.slice(1,-1)).slice(1,-1)
    const dir = {'Up':[-1,0], 'Down':[1,0], 'Left':[0,-1], 'Right':[0,1]}
    const blocks = m.reduce((a,row,r) => 
      a.concat(row.reduce((b,v,c) => v === 'B' ? b.concat([[r,c]]) : b, [])), [])
    const canGo = (r, c, [R,C]) => m[r+R] && m[r+R][c+C] === '.'
    const turn = d => ({'Left':'Up', 'Up':'Right', 'Right':'Down', 'Down':'Left'})[d]
    const go = (r, c, d) => {
        const moveArr = []
        while (1) {
            const [R,C] = dir[d]
            while (canGo(r, c, [R,C])) {
                m[r+=R][c+=C] = 'x'
                moveArr.push([r,c])
            }
            if (!canGo(r, c, dir[d=turn(d)])) return moveArr
        }
    }
    const usedBlocks = new Set(), result = [], totalDots = m.length * m[0].length - blocks.length
    return (DFS = moves => {
        if (moves === totalDots && blocks.length === usedBlocks.size) return result
        for (const i in blocks) {
            if (usedBlocks.has(i)) continue
            const [r,c] = blocks[i]
            for (let d in dir)
                if (canGo(r,c,dir[d])) {
                    const moveArr = go(r,c,d)
                    result.push([r,c,d])
                    usedBlocks.add(i)
                    if (d = DFS(moves + moveArr.length)) return d
                    result.pop()
                    usedBlocks.delete(i)
                    moveArr.forEach(([R,C]) => m[R][C] = '.')
                }
        }
        return false
    })(0)
}

______________________________________________________________________
function playFlou(gameMap) {
  
  let grid = gameMap.split`\n`.map(r=>[...r].map(c=>'+-|'.includes(c)?'#':c));
  let [h, w] = [grid.length, grid[0].length];
  let [partial,solution] = [[],[]];
  let inbound = (y,x) => y>=0 && x>=0 && y<h && x<w;
  let unhash = c => [Math.floor(c/w), c%w];
  let hash = (y,x) => y*w+x;
  let solved = () => [...Array(h*w).keys()].every(c=>([y,x]=unhash(c),grid[y][x]!='.'));
  let dirs = [[0,1,'Right'],[1,0,'Down'],[0,-1,'Left'],[-1,0,'Up']];
  let colors = [...Array(h*w).keys()].reduce((hs,i)=>{
    let [y, x] = unhash(i);
    if (!'#.'.includes(grid[y][x])) hs.push(({color:i,used:false,path:[]}));
    return hs;
  },[]);
  
  let walk = (color, di) => {
    let [y,x] = unhash(color.color);
    let [dy,dx,sym,k] = [null,null,null,null];
    do {
      k = 0;
      [dy,dx,sym] = dirs[di];
      while (inbound(y+dy,x+dx) && grid[y+dy][x+dx] == '.') {
        y+=dy;
        x+=dx;
        grid[y][x] = 'b';
        color.path.push(hash(y,x));
        k++;
      }
      di = (di+1)%dirs.length;
    } while (k > 0);
  }
  
  let restore = color => {
    while (color.path.length) {
      let c = color.path.pop();
      let [y,x] = unhash(c);
      grid[y][x] = '.';
    }
  }
  
  let dfs = () => {
    if (solution.length) return true;
    if (solved() && colors.every(c=>c.used)) {
      solution.push(partial.slice()); return true;
    }
    for (let color of colors) {
      if (color.used) continue;
      let [y,x] = unhash(color.color);
      color.used = true;
      for (let di=0; di<dirs.length; di++) {
        let [dy,dx,sym] = dirs[di];
        partial.push([y-1,x-1,sym]);
        walk(color, di);
        if (color.path.length && dfs()) return true;
        restore(color);
        partial.pop();
      }
      color.used = false;
    }
    return false;
  }
  
  return dfs() ? solution[0] : false;
}

____________________________________________________
var ii=0
function playFlou(gameMap){
  const INICIAL_CELL_CHAR = 'B'
  const EMPTY_CELL_CHAR = '.'
  let move = 0

  // Convert a gamemap into a 2d array board
  let makeBoard = gameMap => gameMap.split("\n").map( row => row.split("") )

  // Get all initial cells (character B)
  const getInitialCells = board => {
    const res = []
    board.forEach( (row, y) => {
      row.forEach( (cell, x) => {
        if (cell === INICIAL_CELL_CHAR) res.push([y,x])
      })
    })
    return res
  }

  // Given a board and coordinates returns an array of all posible moves
  const getValidPosibleDirections = (cell, board) => {
    const res = []
    const y = cell[0]
    const x = cell[1]
    if (board[y][x + 1] === EMPTY_CELL_CHAR) res.push('Right')
    if (board[y][x - 1] === EMPTY_CELL_CHAR) res.push('Left')
    if (board[y + 1][x] === EMPTY_CELL_CHAR) res.push('Down')
    if (board[y - 1][x] === EMPTY_CELL_CHAR) res.push('Up')
    return res
  }

  const moveBlock = (cell, i, direction, board) => {
    let y = cell[0]
    let x = cell[1]
    let iterate = true
    while (iterate) {
      if (direction === "Right") x++;
      if (direction === "Left")  x--;
      if (direction === "Down")  y++;
      if (direction === "Up")    y--;
      board[y][x] = i
      switch (direction) {
        case "Right": 
          if (board[y][x + 1] !== EMPTY_CELL_CHAR) {
            if (board[y + 1][x] === EMPTY_CELL_CHAR) direction = "Down"
            else iterate = false
          }
          break;
        case "Left": 
          if (board[y][x - 1] !== EMPTY_CELL_CHAR) {
            if (board[y - 1][x] === EMPTY_CELL_CHAR) direction = "Up"
            else iterate = false
          }
          break;
        case "Down": 
          if (board[y + 1][x] !== EMPTY_CELL_CHAR) {
            if (board[y][x - 1] === EMPTY_CELL_CHAR) direction = "Left"
            else iterate = false
          }
          break;
        case "Up": 
          if (board[y - 1][x] !== EMPTY_CELL_CHAR) {
            if (board[y][x + 1] === EMPTY_CELL_CHAR) direction = "Right"
            else iterate = false
          }
          break;
      }
    }
  }

  const undoMoveBlock = (actualmove, board) => {
    board.forEach( (row, y) => {
      row.forEach( (cell, x) => {
        if (cell === actualmove) board[y][x] = EMPTY_CELL_CHAR
      })
    })
  }

  const boardIsFilled = (board) => {
    for (y=0;y<board.length; y++) {
      const row = board[y]
      for (x=0;x<row.length; x++) {
        if (board[y][x] === EMPTY_CELL_CHAR) return false
      }
    }
    return true
  }

  const traverse = (cells, board) => {
    const solution = []
    for (let i = 0; i<cells.length; i++) {
      const cell = cells[i]
      const posibleDirections = getValidPosibleDirections(cell, board)
      if (posibleDirections.length === 0) return [] // No moves left
      for (let direction of posibleDirections) {
        solution.push([...cell, direction])
        let actualmove = move++
        moveBlock(cell, actualmove, direction, board)
        const otherCells = [...cells.slice(0,i), ...cells.slice(i+1,cells.length)]
        if (otherCells.length === 0) {
          if (boardIsFilled(board)) return solution
        } else {
          let moreMoves = traverse(otherCells, board)
          if (moreMoves.length > 0) return [...solution, ...moreMoves]  // Solution  found
        }
        undoMoveBlock(actualmove, board)
        solution.pop()
      }
    }
    return solution
  }

  let board = makeBoard(gameMap)
  let initialCells = getInitialCells(board)
  let solution = traverse(initialCells, board).map( pos => {
    return [pos[0] - 1, pos[1] - 1, pos[2]] // Move coordinates to origin
  })
  return solution.length > 0 ? solution : false
}

______________________________________________________________________
const dirs = {
  Right: {x: 1, y: 0, next: 'Down'},
  Down: {x: 0, y: 1, next: 'Left'},
  Left: {x: -1, y: 0, next: 'Up'},
  Up: {x: 0, y: -1, next: 'Right'},
};

const isEmpty = (rows, x, y) => rows[y] && rows[y][x] === '.';

const move = (rows, {x, y}, dir) => {
  let d = dirs[dir];
  if (!isEmpty(rows, x + d.x, y + d.y)) return false;
  rows = rows.map((r) => [...r]);
  while (true) {
    if (isEmpty(rows, x + d.x, y + d.y)) {
      x += d.x;
      y += d.y;
      rows[y][x] = 'x';
    } else {
      d = dirs[d.next];
      if (!isEmpty(rows, x + d.x, y + d.y)) break;
    }
  }
  return rows;
};

const removeIndex = (arr, i) => {
  const n = [...arr];
  n.splice(i, 1);
  return n;
};

const findSolution = (rows, blocks, solution = []) => {
  if (!blocks.length && rows.every((r) => r.every((c) => c !== '.')))
    return solution;

  for (let i = 0; i < blocks.length; i++) {
    const remainingBlocks = removeIndex(blocks, i);
    for (const dir in dirs) {
      const newRows = move(rows, blocks[i], dir);
      if (!newRows) continue;
      const s = findSolution(newRows, remainingBlocks, [
        ...solution,
        [blocks[i].y, blocks[i].x, dir],
      ]);
      if (s) return s;
    }
  }
  return false;
};

const playFlou = (gameMap) => {
  const rows = gameMap
    .split('\n')
    .slice(1, -1)
    .map((r) => r.split('').slice(1, -1));

  const blocks = [];
  for (let y = 0; y < rows.length; y++) {
    for (let x = 0; x < rows[y].length; x++) {
      if (rows[y][x] === 'B') blocks.push({x, y});
    }
  }

  return findSolution(rows, blocks);
};

_______________________________________________________________
const playFlou=(map)=>{

  let ans=false
  let a=[],n=[]
  let m=map.split`\n`
  let h=m.length-2
  let w=m[0].length-2
  let occ=(a,y,x)=>y<0||x<0||y==h||x==w||a[y][x]
  let dir=[[-1,0,'Up'],[0,1,'Right'],[1,0,'Down'],[0,-1,'Left']]

  for(let i,j=0;j<h;j++)
    for(a[j]=[],i=0;i<w;i++)
      if(m[j+1][i+1]=='.') a[j][i]=0
      else a[j][i]=1, n.push([j,i])

  let f=(m,n,t,p)=>{
    if(ans) return
    if(!t && !n.length) return ans=p
    for(let z of n) for(let [y,x]=z,d=0;d<4;d++){
      let [q,r,s,j,i,e,m2,u]=dir[d]
      if(!occ(m,j=y+q,i=x+r))
        for(e=d,u=t,m2=m.map(e=>[...e]);;){
          m2[j][i]=1;u--
          if(!occ(m2,j+q,i+r)){j+=q;i+=r;continue}
          [q,r]=dir[e=(e+1)&3];if(!occ(m2,j+q,i+r))j+=q,i+=r
          else {f(m2,n.filter(e=>e!=z),u,[...p,[y,x,s]]);break}}}}

  f(a,n,h*w-n.length,[])
  return ans
}

__________________________________________________
let moves = 0;

function getInitialCells(board) {
  const result = [];
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      if (board[i][j] === 'B') {
        result.push([i, j]);
      }
    }
  }
  return result;
}

function getValidPosibleDirections(cell, board) {
  const directions = [];
  
  const [i, j] = cell;
  
  if (board[i][j + 1] === '.') {
    directions.push('Right');
  }
  if (board[i][j - 1] === '.') {
    directions.push('Left');
  }
  if (board[i + 1][j] === '.') {
    directions.push('Down');
  }
  if (board[i - 1][j] === '.') {
    directions.push('Up');
  }
  
  return directions;
}


function traverse(cells, board) {
  const movesList = [];
  for (let i = 0; i < cells.length; i++) {
    const cell = cells[i];
    const posibleDirections = getValidPosibleDirections(cell, board);
    if (posibleDirections.length === 0) {
      return [];
    }
    for (const direction of posibleDirections) {
      movesList.push([...cell, direction]);
      moves++;
      const actualMove = moves;
      moveBlock(cell, actualMove, direction, board);
      const otherCells = [...cells.slice(0,i), ...cells.slice(i+1,cells.length)]
      if (otherCells.length === 0) {
        if (isGameFinished(board)) return movesList;
      } else {
        const moreMoves = traverse(otherCells, board);
        if (moreMoves.length > 0) {
          return [...movesList, ...moreMoves];
        }
      }
      undoMoveBlock(board, actualMove);
      movesList.pop();
    }
  }
  return movesList;
}

function isGameFinished(board) {
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j< board[i].length; j++) {
      if (board[i][j] === '.') {
        return false;
      }
    }
  }
  return true;
}

function undoMoveBlock(board, direction) {
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      if (board[i][j] === direction) {
        board[i][j] = '.';
      }
    }
  }
}

function moveBlock(cell, color, direction, board) {
  let [i, j] = cell;
  let iterate = true;
  while (iterate) {
    switch (direction) {
        case 'Up': {
          i--;
          board[i][j] = color;
          if (board[i - 1][j] !== '.') {
            if (board[i][j + 1] === '.') {
              direction = 'Right';
            } else {
              iterate = false;
            }
          }
          break;
        }
        case 'Down': {
          i++;
          board[i][j] = color;
          if (board[i + 1][j] !== '.') {
            if (board[i][j - 1] === '.') {
              direction = 'Left';
            } else {
              iterate = false;
            }
          }
          break;
        }
        case 'Left': {
          j--;
          board[i][j] = color;
          if (board[i][j - 1] !== '.') {
            if (board[i - 1][j] === '.') {
              direction = 'Up';
            } else {
              iterate = false;
            }
          }
          break;
        }
        case 'Right': {
          j++;
          board[i][j] = color;
          if (board[i][j + 1] !== '.') {
            if (board[i + 1][j] === '.') {
              direction = 'Down';
            } else {
              iterate = false;
            }
          }
          break;
        }
        default: {
          break;
        }
    }
  }
}

function playFlou(gamemap) {
  const board = gamemap.split('\n').map( row => row.split(''));
  const initialCells = getInitialCells(board);
  const solution = traverse(initialCells, board).map(position => [position[0] - 1, position[1] - 1, position[2]]);
  return solution.length > 0 ? solution : false;
}
