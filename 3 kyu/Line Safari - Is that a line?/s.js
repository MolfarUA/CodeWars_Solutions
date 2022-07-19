59c5d0b0a25c8c99ca000237


function line(grid) {
  let is = (a,b)=>b.includes(a), moves = [[-1,0],[0,1],[1,0],[0,-1]], g  // `g` used for working grid
  
  let trav = ([r,c], dir) => {
    g[r][c] = ' '
    let X = moves.map(([R,C])=>[R+r,C+c])    // Coordinates
    let P = X.map(([R,C])=>g[R]&&g[R][C]||' ').map((d,i)=>d!='-|-|'[i]?d:' '), [U,R,D,L] = P  // Path pieces
    let go = d => trav(X['URDL'.indexOf(d)], d)  // Recurser
    
    switch (grid[r][c]) {
      case 'X': return dir && g.every(w=>w.every(q=>q==' '))     // Made it to the end!
                || (P.join``.match(/\S/g)||[]).length == 1 && go('URDL'[P.findIndex(l=>l!=' ')])   // Start...
      case '|': return is(dir,'UD') && go(dir)      // Keep moving vertically
      case '-': return is(dir,'RL') && go(dir)      // Keep moving horizontally
      case '+': return is(dir,'RL')
        ? is(U,'|+X') && is(D,'- ') && go('U') || is(D,'|+X') && is(U,'- ') && go('D')  // Turn from horiz or vert
        : is(R,'-+X') && is(L,'| ') && go('R') || is(L,'-+X') && is(R,'| ') && go('L')  // Turn from vert to horiz
    }
    return false  // Dead end
  }
  return grid.some((w,r) => [...w].some((s,c) => s=='X' && (g = grid.map(y=>[...y]), trav([r,c])) ))
}
_______________________________________
const line = grid => {
  
  const DIRECTIONS = [[-1, 0], [1, 0], [0, -1], [0, 1]];
  
  const lineLength = `${grid}`.replace(/\s|,/g, '').length;
  const [startX, startY] = grid.reduce((acc, row, rowIdx) => 
                             acc[1] === -1 ? [rowIdx, row.indexOf('X')] : acc, [-1, -1]);
  const [endX, endY] = grid.reduceRight((acc, row, rowIdx) => 
                             acc[1] === -1 ? [rowIdx, row.lastIndexOf('X')] : acc, [-1, -1]);  

  const moveNext = ([x, y], path) => {
    const point = grid[x] && grid[x][y];
    const [lastX, lastY] = path[path.length - 1] || [];
    const isFinalPoint = point === 'X' && path.length && (x !== path[0][0] || y !== path[0][1]);
       
    if (isFinalPoint) return path.length === lineLength - 1;
    
    const nextStep = DIRECTIONS.filter(([offsetX, offsetY]) => {   
      const [nextX, nextY] = [x + offsetX, y + offsetY];
      const nextPoint = grid[nextX] && grid[nextX][nextY];
      
      const isOnPath = nextPoint && nextPoint !== ' ';
      const wasThere = path.some(([pX, pY]) => nextX === pX && nextY === pY);
      const checkHorizontal = /^[X\-+]+$/.test(point + nextPoint) || Math.abs(nextY - y) - 1 || nextX - x;
      const checkVertical =   /^[X|+]+$/ .test(point + nextPoint) || Math.abs(nextX - x) - 1 || nextY - y;
      const checkEdge = point !== '+' || (lastY - nextY) * (lastX - nextX);
          
      return isOnPath && !wasThere && checkHorizontal && checkVertical && checkEdge;
    })
     
    if (nextStep.length !== 1) return false;
      
    const [[offsetX, offsetY]] = nextStep;
    return moveNext([x + offsetX, y + offsetY], [...path, [x, y]]);
  }
  
  return moveNext([startX, startY], []) || moveNext([endX, endY], []);
  
}
_______________________________________
function line(grid) {
  const maxX = grid[0].length - 1;
  const maxY = grid.length - 1;

  const some = (comparator) => {
    for (let x = 0; x <= maxX; x++) {
      for (let y = 0; y <= maxY; y++) {
        if (comparator(grid[y][x], [x, y])) {
          return true;
        }
      }
    }

    return false;
  };

  const filter = (comparator) => {
    const results = [];

    for (let x = 0; x <= maxX; x++) {
      for (let y = 0; y <= maxY; y++) {
        if (comparator(grid[y][x], [x, y])) {
          results.push([x, y]);
        }
      }
    }

    return results;
  };

  const isOutside = ([x, y]) => x < 0 || x > maxX || y < 0 || y > maxY;

  const moves = {
    left: ([x, y]) => {
      const nextX = x - 1;
      const nextY = y;
      const char = !isOutside([nextX, nextY]) ? grid[nextY][nextX] : undefined;
      return char !== undefined && char !== ' ' && char !== '|' ? [nextX, nextY] : [x, y];
    },

    right: ([x, y]) => {
      const nextX = x + 1;
      const nextY = y;
      const char = !isOutside([nextX, nextY]) ? grid[nextY][nextX] : undefined;
      return char !== undefined && char !== ' ' && char !== '|' ? [nextX, nextY] : [x, y];
    },

    up: ([x, y]) => {
      const nextX = x;
      const nextY = y - 1;
      const char = !isOutside([nextX, nextY]) ? grid[nextY][nextX] : undefined;
      return char !== undefined && char !== ' ' && char !== '-' ? [nextX, nextY] : [x, y];
    },

    down: ([x, y]) => {
      const nextX = x;
      const nextY = y + 1;
      const char = !isOutside([nextX, nextY]) ? grid[nextY][nextX] : undefined;
      return char !== undefined && char !== ' ' && char !== '-' ? [nextX, nextY] : [x, y];
    }
  };

  const explore = function ([x, y], possibleMoves, visitedCells) {
    const hasBeenVisited = ([x, y]) =>
      visitedCells.some(([pathX, pathY]) => pathX === x && pathY === y);

    let results = [];

    for (const move of possibleMoves) {
      const [nextX, nextY] = move([x, y]);

      if (hasBeenVisited([nextX, nextY])) {
        continue;
      }

      let result;

      const char = grid[nextY][nextX];

      if (char === 'X') {
        result = !some(
          (char, [x, y]) => char !== ' ' && !hasBeenVisited([x, y]) && !(x === nextX && y === nextY)
        );
      } else {
        let nextPossibleMoves;

        if (char === '-' || char === '|') {
          nextPossibleMoves = [move];
        } else if (char === '+') {
          if (move === moves.left || move === moves.right) {
            nextPossibleMoves = [moves.up, moves.down];
          } else {
            nextPossibleMoves = [moves.left, moves.right];
          }
        } else {
          throw new Error(`Invalid character found in the grid: '${char}'`);
        }

        const nextVisitedCells = [...visitedCells, [nextX, nextY]];

        result = explore([nextX, nextY], nextPossibleMoves, nextVisitedCells);
      }

      results.push(result);
    }

    if (!results.some((result) => result === true)) {
      return false;
    }

    if (results.some((result) => result === false)) {
      return false;
    }

    return true;
  };

  const terminators = filter((char) => char === 'X');

  return terminators.some((terminator) =>
    explore(terminator, [moves.left, moves.right, moves.up, moves.down], [terminator])
  );
}
