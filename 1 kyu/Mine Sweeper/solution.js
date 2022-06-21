5c1d796370fee68b1e000611


function solveMine(map, n) {
    const solver = new Solver(map, n);
    return solver.solve();
}

class Solver {
    constructor(map, totalMines) {
        this.totalMines = totalMines;
        this.grid = new Grid(map);
        this.constraints = new Constraints(this.grid, totalMines);
    }

    solve() {
        this.solveBasic();

        if (this.constraints.length === 0) {
            return this.grid.toString();
        }

        const solutions = this.findAllSolutions();

        if (solutions.length > 0) {
            this.flag(solutions.knownMines);
            this.open(solutions.knownEmpty);

            if (solutions.knownMines.length > 0 || solutions.knownEmpty.length > 0) {
                return this.solve();
            }
        }

        return '?';
    }

    solveBasic() {
        let changed = false;

        this.constraints.forEach(c => {
            if (c.total === 0) {
                this.open(c.cells);
                changed = true;
            }

            if (c.total === c.length) {
                this.flag(c.cells);
                changed = true;
            }
        });

        if (changed) {
            this.constraints.reduce();
            this.solveBasic();
        }
    }

    findAllSolutions() {
        let solutions = new Solutions();

        const search = (fringe) => {
            const solution = fringe.clone();
            const unsolvedCell = fringe.unsolvedCell;

            if (!unsolvedCell) {
                solutions.push(solution);
                return;
            }

            for (let i = 0; i <= 1; i++) {
                solution.set(unsolvedCell, i);

                if (!solution.meetsConstraints(this.constraints)) {
                    continue;
                }

                search(solution);
            }
        };

        search(Fringe.create(this.grid));

        return solutions;
    }

    open(cells) {
        cells.slice().forEach(cell => {
            const [row, col] = cell;
            this.grid.open(row, col);
            this.constraints.removeCell(row, col);
            this.constraints.addFromCell(this.grid, row, col);
        });
    }

    flag(cells) {
        cells.slice().forEach(cell => {
            const [row, col] = cell;
            this.grid.flag(row, col);
            this.constraints.flagCell(row, col);
        });
    }
}

class Constraints {
    constructor(grid, totalMines) {
        this.constraints = [];

        const covered = [];

        grid.forEach((row, col) => {
            if (grid.isOpened(row, col)) {
                this.addFromCell(grid, row, col);
            }

            if (grid.isCovered(row, col)) {
                covered.push([row, col]);
            }
        });

        this.add(covered, totalMines);

        this.reduce();
    }

    get length() {
        return this.constraints.length;
    }

    add(cells, value) {
        if (cells.length > 0) {
            this.constraints.push(new Constraint(cells, value));
        }
    }

    addFromCell(grid, row, col) {
        let value = grid.valueAt(row, col);
        let cells = [];

        grid.forEachNeighbor(row, col, (i, j) => {
            if (grid.isCovered(i, j)) {
                cells.push([i, j]);
            }

            if (grid.isFlagged(i, j)) {
                value--;
            }
        });

        this.add(cells, value);
    }

    reduce() {
        for (let i = 0; i < this.constraints.length; i++) {
            for (let j = 0; j < this.constraints.length; j++) {
                if (i === j) continue;

                const a = this.constraints[i];
                const b = this.constraints[j];
                if (a.isSubsetOf(b)) {
                    b.removeCells(a.cells);
                    b.total -= a.total;
                }
            }
        }

        this.constraints = this.constraints.filter(c => c.length > 0);
    }

    removeCell(row, col, flag = false) {
        this.forEach(c => c.remove(row, col, flag));
    }

    flagCell(row, col) {
        this.removeCell(row, col, true);
    }

    forEach(cb) {
        this.constraints.forEach((c, i) => cb(c, i));
    }
}

class Constraint {
    constructor(cells, total) {
        this.cells = cells;
        this.total = total;
    }

    get length() {
        return this.cells.length;
    }

    isSubsetOf(constraint) {
        return this.cells.every(cell => constraint.indexOf(...cell) !== -1);
    }

    indexOf(row, col) {
        return this.cells.findIndex(cell => cell[0] === row && cell[1] === col);
    }

    remove(row, col, flag = false) {
        const index = this.indexOf(row, col);
        if (index !== -1) {
            this.cells.splice(index, 1);

            if (flag) {
                this.total--;
            }
        }
    }

    removeCells(cells) {
        cells.forEach(cell => this.remove(...cell));
    }
}

class Solutions {
    constructor() {
        this.fringes = [];
        this.empty = {};
        this.mines = {};
    }

    get length() {
        return this.fringes.length;
    }

    get knownMines() {
        const mines = [];

        for (let key in this.mines) {
            const cell = key.split(',').map(Number);
            if (this.mines[key] === 1) {
                mines.push(cell);
            }
        }

        return mines;
    }

    get knownEmpty() {
        const empty = [];

        for (let key in this.empty) {
            const cell = key.split(',').map(Number);
            if (this.empty[key] === 0) {
                empty.push(cell);
            }
        }

        return empty;
    }

    push(fringe) {
        this.fringes.push(fringe);

        if (this.fringes.length === 1) {
            for (let cell in fringe.cells) {
                this.empty[cell] = 0;
                this.mines[cell] = 1;
            }
        }

        for (let cell in fringe.cells) {
            this.empty[cell] |= fringe.cells[cell];
            this.mines[cell] &= fringe.cells[cell];
        }
    }
}

class Fringe {
    constructor(cells = []) {
        this.cells = {};

        cells.forEach(c => {
            this.cells[c] = null;
        });
    }

    static create(grid) {
        const cells = [];

        grid.forEach((row, col) => {
            if (grid.isFringe(row, col)) {
                cells.push([row, col]);
            }
        });

        return new Fringe(cells);
    }

    clone() {
        const fringe = new Fringe();
        fringe.cells = Object.assign({}, this.cells);
        return fringe;
    }

    meetsConstraints(constraints) {
        let valid = true;

        constraints.forEach(c => {
            valid = valid && this.meetsConstraint(c);
        });

        return valid;
    }

    meetsConstraint(constraint) {
        let total = 0;
        let found = 0;

        for (let cell in this.cells) {
            const [row, col] = cell.split(',').map(Number);
            const value = this.cells[cell];

            if (value !== null && constraint.indexOf(row, col) > -1) {
                found++;
                total += value;

                if (total > constraint.total) {
                    return false;
                }
            }
        }

        if (found === constraint.length && total !== constraint.total) {
            return false;
        }

        return true;
    }

    set(cell, value) {
        this.cells[cell] = value;
    }

    get unsolvedCell() {
        let unsolvedCell = null;

        for (let cell in this.cells) {
            if (this.cells[cell] === null) {
                unsolvedCell = cell;
                break;
            }
        }

        return unsolvedCell;
    }
}

class Grid {
    constructor(map) {
        this.grid = map.split('\n').map(row => {
            return row.split(' ').map(value => value === '?' ? this.COVERED : +value);
        });
    }

    get FLAGGED() { return 9; }
    get COVERED() { return -1; }

    toString() {
        return this.grid.map((row, i) => {
            return row.map((value, j) => {
                if (this.isFlagged(i, j)) return 'x';
                if (this.isCovered(i, j)) return '?';
                return value;
            }).join(' ');
        }).join('\n');
    }

    open(row, col) {
        this.grid[row][col] = +open(row, col);
    }

    flag(row, col) {
        this.grid[row][col] = this.FLAGGED;
    }

    isFlagged(row, col) {
        return this.valueAt(row, col) === this.FLAGGED;
    }

    isCovered(row, col) {
        return this.valueAt(row, col) === this.COVERED;
    }

    isOpened(row, col) {
        return !this.isFlagged(row, col) && !this.isCovered(row, col);
    }

    isFringe(row, col) {
        if (!this.isCovered(row, col)) return false;

        let isFringe = false;
        this.forEachNeighbor(row, col, (i, j) => {
            isFringe = isFringe || this.isOpened(i, j);
        });

        return isFringe;
    }

    valueAt(row, col) {
        return this.grid[row][col];
    }

    forEach(cb) {
        this.grid.forEach((row, i) => {
            row.forEach((value, j) => cb(i, j, value));
        });
    }

    forEachNeighbor(row, col, cb) {
        for (let i = -1; i < 2; i++) {
            for (let j = -1; j < 2; j++) {
                if (i === 0 && j === 0) continue;

                if (this.inGrid(row + i, col + j)) {
                    cb(row + i, col + j, this.valueAt(row + i, col + j));
                }
            }
        }
    }

    inGrid(row, col) {
        return row >= 0 && row < this.grid.length
            && col >= 0 && col < this.grid[0].length;
    }
}
___________________________________________________________________
function solveMine(map,mines) {

    let hypothetical__Mode = false /* when this is true, the functions will act differently -- opening a tile will turn the value to 'O', flagging it will turn it to 'M' */
    
    'M' // hypothetically a mine
    'O' // hypothetically safe
    
    const board = map.split`\n`.map(s => s.split(' ')),
          H = board.length,
          W = board[0].length,
          M = Array(H).fill().map((_,r) =>      /* the data machine */
              Array(W).fill().map((_,c) => ({
                V: +board[r][c] || board[r][c], // value of tile, could be 'x','?', or a digit
                R: NaN,                         // number of undiscovered mines a tile is touching
                X: NaN,                         // number of flagged neighbors
                U: NaN,                         // number of unknown neighbors
                SU:new Set(),                   // set of unknown neighbors
              })))
              
    function neighbors(r,c) { 
      return [[-1,-1],[-1,0],[-1,1],[0,-1],[0, 1],[1,-1],[1,0],[1,1]]
        .map(([dr,dc]) => [r+dr,c+dc])
        .filter(([r,c]) => 0 <= r && r < H && 0 <= c && c < W)
    }       
    function takefrom_MN(r,c,x) { return neighbors(r,c).filter(([R,C]) => x.includes(M[R][C].V)) }   // get neighbors of a certain kind
    function open_unknowns(r,c) { takefrom_MN(r,c,'?').forEach(([R,C]) => OPEN(R,C)) }               // open the neighbors
    function flag_unknowns(r,c) { takefrom_MN(r,c,'?').forEach(([R,C]) => FLAG(R,C)) }               // flag the neighbors
    function OPEN(r,c) { !(M[r][c].V = hypothetical__Mode ? 'O' : +open(r,c)) && open_unknowns(r,c) }// if we get a 0, open recursively around
    function FLAG(r,c) {   M[r][c].V = hypothetical__Mode ? 'M' : 'x', mines-- }                     // flag and decrease the number of mines
    function*coords()  { for (let r=0;r<H;r++) for(let c=0;c<W;c++) yield[r,c] }                     // make it easier to loop through the board
    function* tiles()  { for(let r=0;r<H;r++)for(let c=0;c<W;c++)yield M[r][c] }                     // make it easier to loop through the board
            
    const K = (r,c) => r + '-' + c,             // make key
          V = x => x.split('-').map(x => +x),   // parse key
          updateTile = (r,c) => {
              if (board[r][c] == '0') M[r][c].V = 0
              const unknowns = takefrom_MN(r,c,'?').map(([R,C])=>K(R,C))
              const flagged  = takefrom_MN(r,c,(hypothetical__Mode ? 'xM' : 'x'))
  
              M[r][c].X = flagged.length          // number of flagged neighbors
              M[r][c].R = M[r][c].V - M[r][c].X   // number of Remaining neighbors
              M[r][c].U = unknowns.length         // number of Unknowns neighbors
              M[r][c].SU  = new Set(unknowns)     // Set of Unknown neighbors
          },
          updateAllTiles = () => {
              for (const [r,c] of coords()) 
                  if (!'x?MO'.includes(M[r][c].V)) 
                      updateTile(r,c)
          },
          
          
          
          // SOLVING METHODS RETURN TRUE IF A DIFFERENCE WAS MADE
          
          trivial_moves = () => { 
              let redo
              for (const [r,c] of coords()) {
                  const  T = M[r][c], v = T.V, key = K(r,c)
                  if (!'x?MO'.includes(v) && T.U)  {
                      if (v === T.X && T.U) { open_unknowns(r,c), redo = true }
                      if (v === T.X  + T.U) { flag_unknowns(r,c), redo = true }
                  }
              }
              return redo 
          },
          subset_analysis = () => {
              /*
                  SUBSET EXTRACTION
                  a is a tile, x = a.R, s = a.SU (.R = remaining mines, SU = set of unknowns)
                  for each digit neighbor, b, of a
                      if b.SU is a proper subset of a.SU,
                      x -= b.R, (x is the remaining number of mines touching
                      s -= b.SU (set difference)
                  if x is 0 then we can open any remaining (r,c) in s
              */
              let redo
              for (const [r,c] of coords()) {
              
                  const a = M[r][c], A = new Set(a.SU)
                  let x = a.R
                  if (!x) continue
                  for (const [R,C] of coords()) {
                      if (Math.abs(R-r) < 3 && Math.abs(C-c) < 3 && !(r === R && c === C)){   // if a and b can share a square and a != b
                          const b = M[R][C]
                          if (!isNaN(a.V) && !isNaN(b.V)) {                                   // make sure both of their values are digits
                              const B = [...b.SU]
                              if (A.size > B.length && B.every(x => A.has(x))) {              // check that B is a proper subset of A
                                  x -= b.R                                                    // subtract # of remaining mines in B from x
                                  B.forEach(e => A.delete(e))                                 // delete all the values of A that are in B
                              }
                          }
                      }
                      
                  }
                  if (x === 0) redo = +A.forEach(v => OPEN(...V(v))) || 1                     // if the remaining areas cannot have mines, we can open them
              }
              return redo
          },
          comboResearch = () => {
              const k_combinations = (set, k) => {
                  let i, j, combs = [], head, tailcombs
                  if (k > set.length || k <= 0) return []
                  if (k === set.length) return [set]
                  if (k === 1) return set.reduce((a,v)=>a.concat([[v]]),[])
                  for (i = 0; i < set.length - k + 1; i++) {
                      head = set.slice(i, i + 1)
                      tailcombs = k_combinations(set.slice(i + 1), k - 1)
                      for (j = 0; j < tailcombs.length; j++) 
                          combs.push(head.concat(tailcombs[j]))
                  }
                  return combs
              },
              resetHypotheticalMode = () => {
                  for (const T of tiles()) {
                      if (T.V === 'M') mines++
                      if ('MO'.includes(T.V)) T.V = '?'
                  }
                  hypothetical__Mode = false
                  updateAllTiles()
              }
              
              for (const T of tiles()) {
                  const s = T.SU,        // our tile's set of unknowns
                  safe = new Set(),      // tiles which don't lead to a contradiction when assumed as mines
                  isMine = new Set(T.SU) // tiles that were mines in every single combination
                  
                  for (const combo of k_combinations([...s],T.R)) {                    // try this combo, see what it leads to
                      hypothetical__Mode = true                                        // now we don't open mines
                      for (const [R,C] of combo.map(V)) FLAG(R,C)                      // test a combo
                      while(updateAllTiles() || trivial_moves() || subset_analysis()); // loop through methods
                      if (mines < 0 || M.some(row=>row.some(T => T.R < 0))) {          // check for a contradiction
                        resetHypotheticalMode()
                        continue
                      }
                      for (const rc of combo) safe.add(rc)
                      for (const rc of isMine) if (!combo.includes(rc)) isMine.delete(rc)
                      
                      resetHypotheticalMode()
                  }
                  for (const rc of s) if (!safe.has(rc)) return OPEN(...V(rc)) || 1
                  for (const rc of isMine) return FLAG(...V(rc)) || 1
              }
          },
          marked = {}, // excusively for the following function
          recursifuc = (_mines) => {
              const seen = new Set()
              return (function(_mines){
                  if (!_mines) for (let i in marked) delete marked[i]
                  if (_mines === mines) for (let [r,c] of coords()) if (M[r][c].V === '?' && !marked[K(r,c)]) { OPEN(r,c); return true }
                  if (_mines > mines) return false 
                  for (const T of tiles())
                      if (T.R && ![...T.SU].some(x => marked[x])) {
                          T.SU.forEach(x => marked[x] = true)
                          _mines += T.R
                          const key = Array.from(coords()).filter(([r,c]) => marked[K(r,c)]).sort().join``
                          if (!seen.has(key))
                              if (arguments.callee(_mines)) return true
                          seen.add(key)
                          T.SU.forEach(x => marked[x] = false)
                          _mines -= T.R
                      }
              })(_mines)  
          }
          
    for (const [r,c] of coords()) if (board[r][c] === '0') updateTile(r,c)                               // absorb given data
    while(updateAllTiles() || trivial_moves() || subset_analysis() || comboResearch() || recursifuc(0)); // loop through solver methods
    
    return mines ? '?' : M.map(s => s.map(x=>x.V).join` `).join`\n`
}
_______________________________________________________
function solveWithSteppedRules(rules, getProgress, isDone) {
  let lastProgress = getProgress(), i = 0;
  while (!isDone()) {
    rules[i]();
    let progress = getProgress();
    i = progress > lastProgress ? 0 : i + 1;
    if (i >= rules.length) { return false; }
    lastProgress = progress;
  }
  return true;
}

function iterateCombosOfSizeN(arr, func, n) {
  let numCombos = 1 << arr.length;
  let combo = new Array(n);
  for (let i = 0; i < numCombos; ++i) {
    let bits = 0;
    for (let j=0; j<32; ++j) { if (i & (1<<j)) {bits++; } }
    if (bits === n) {
      for (let j = 0, p = 0; j < arr.length; ++j) {
        if (i & (1 << j)) { combo[p++] = arr[j]; }
      }      
      if (!func(combo)) { return; }
    }
  }
}

function iterateValidCombosOfSizeN(arr, isValid, func, n) {
  iterateCombosOfSizeN(arr, c => isValid(c) ? func(c) : true, n);
}

function solveMine(map,n) {
  let workingMap = map.split('\n').map(s => s.split(' '));
  const strWidth = map.indexOf('\n') + 1;
  const width = strWidth / 2, height = (map.length+1) / strWidth;
  const iterate = func => { 
    for (let y = 0; y < height; ++y) { 
      for (let x = 0; x < width; ++x) {
        func(x, y);
      }
    }
  };
  const iterateIf = (func, ifFunc) => iterate((x, y) => {
    if (ifFunc(x, y)) {
      func(x, y);
    }
  });
  const readMap = (x, y) => workingMap[y][x];
  const isUnknown = (x, y) => readMap(x, y) === '?';
  const isKnown = (x, y) => readMap(x, y) !== '?';
  const isMine = (x, y) => readMap(x, y) === 'x';
  const isNum = (x, y) => { let c = readMap(x, y); return c !== 'x' && c !== '?'; }
  const countUnknowns = () => {
    let num = 0;
    iterate((x, y) => num += isUnknown(x, y) ? 1 : 0);
    return num.toString();
  };
  const remaining = [n, +countUnknowns()], MINES = 0, UNKNOWN = 1;

  const updateMap = (x, y, m) => workingMap[y][x] = m;
  const clickSafe = (x, y) => { updateMap(x, y, open(y, x)); --remaining[UNKNOWN]; }
  const clickMine = (x, y) => { updateMap(x, y, 'x'); --remaining[MINES]; --remaining[UNKNOWN]; }

  const box = (x, y, func) => { 
    const leftOk = x > 0, rightOk = x < width - 1, topOk = y > 0, bottomOk = y < height - 1;
    const left = x - 1, right = x + 1, top = y - 1, bottom = y + 1;
    if (leftOk) { func(left, y); }
    if (rightOk) { func(right, y); }
    if (topOk) { func(x, top); }
    if (bottomOk) { func(x, bottom); }
    if (leftOk && topOk) { func(left, top); }
    if (rightOk && topOk) { func(right, top); }
    if (rightOk && bottomOk) { func(right, bottom); }
    if (leftOk && bottomOk) { func(left, bottom); }   
  };
  
  const boxUnknowns = (x, y, func) => box(x, y, (h, v) => { if (isUnknown(h, v)) { func(h, v); } });
  const clickSafeBox = (x, y) => boxUnknowns(x, y, clickSafe);
  const clickMineBox = (x, y) => boxUnknowns(x, y, clickMine);
  const boxCount = (x, y, conditionFunc) => { 
    let num = 0; 
    box(x, y, (h, v) => num += conditionFunc(h, v) ? 1 : 0);
    return num.toString();
  };
  const unknownBoxCount = (x, y) => boxCount(x, y, isUnknown);
  const mineBoxCount = (x, y) => boxCount(x, y, isMine);

  const numberSolvedRule = () => iterateIf((x, y) => {
    const mines = mineBoxCount(x, y), unknowns = unknownBoxCount(x, y), num = readMap(x, y);
    if (mines === num) { clickSafeBox(x, y); }
    else if ((num - mines) === +unknowns) { clickMineBox(x, y); }
  }, isKnown);
  
  const getAllUnknownXYs = () => {
    let unknowns = new Array(remaining[UNKNOWN]), i = 0;
    iterateIf((x, y) => unknowns[i++] = [x, y], isUnknown);
    return unknowns;
  };
  
  const isMineComboValid = combo => {
    const comboContains = (x, y) => combo.some(m => m[0] === x && m[1] === y);
    const comboTouchingBoxCount = (x, y) => boxCount(x, y, comboContains);
    const comboBoxCount = (x, y) => boxCount(x, y, comboContains);
    const countMinesWithCombo = (x, y) => ((+mineBoxCount(x, y)) + (+comboBoxCount(x, y))).toString();
    const isSquareValidWithCombo = (x, y) => countMinesWithCombo(x, y) === readMap(x, y);
    
    let valid = true;
    iterateIf((x, y) => {
      valid = isSquareValidWithCombo(x, y);
    }, (x, y) => isNum(x, y) && valid);
    return valid;
  };
  
  const allCombosRule = () => {
    let unknowns = getAllUnknownXYs(), inNoCombos = unknowns, inAllCombos = unknowns, comboCount = 0;
    iterateValidCombosOfSizeN(unknowns, isMineComboValid, c => {
      c.forEach(p => { inNoCombos = inNoCombos.filter(u => u[0] !== p[0] || u[1] !== p[1]); });
      inAllCombos = inAllCombos.filter(u => c.some(p => p[0] === u[0] && p[1] === u[1]));
      ++comboCount;
      return true;
    }, remaining[MINES]);
    if (comboCount > 0) {
      inAllCombos.forEach(u => clickMine(u[0], u[1]));
      inNoCombos.forEach(u => clickSafe(u[0], u[1]));
    }
  };
  const rules = [numberSolvedRule, allCombosRule];
  const getProgress = () => -remaining[UNKNOWN];
  const isDone = () => remaining[UNKNOWN] === 0;
  const resultFromDidSolve = didSolve => didSolve ? workingMap.map(r => r.join(' ')).join('\n') : '?';
  return resultFromDidSolve(solveWithSteppedRules(rules, getProgress, isDone));
}
_________________________________________________________________
function Tile(row, col, value, workingValue) { // workingValue is optional
  this.row = row;
  this.col = col;
  this.value = value; // this.value is what one would see on the tile, be it 0, 1, 2, 3, a question mark, or a flag.
  this.workingValue = workingValue; // this.workingValue is a variable exlusive to numbered tiles. It tracks how many more mines one needs to reach its value. If a Tile with value 2 had one flag around it (assumed to be placed correctly), then its this.workingValue would equal 1 to say, "I need one more mine to be satisfied."
  if (this.workingValue === undefined) {
    this.workingValue = value;
  }
  if (this.value != "?" && this.value != "x") {
    // If the value isn't an unknown nor a mine, convert the string to an int.
    this.value = parseInt(this.value);
    this.workingValue = parseInt(this.workingValue);
  }
  
  this.clone = function() {
    return new Tile(this.row, this.col, this.value, this.workingValue);
  }
  
  this.updateWorkingValue = function(minefield) {
    this.workingValue = this.value - minefield.getTilesSurrounding(this).filter(function(tile) { return tile.value == "x"; }).length;
    return this.workingValue;
  };
}

function Minefield(map, n) {
  /***
        ? => unknown
        number => how many surrounding mines
          # => placeholder value for hypothetical numbers
        x => mine
          * => contradiction/guessed mine
  ***/
  this.minefield = map;
  if (typeof this.minefield == "string") {
    this.minefield = minefieldMatrixToTiles(minefieldStringToMatrix(this.minefield));
  }
  this.n = n;
  
  this.clone = function() {
    var clonedMinefield = [], row, col;
    for (row = 0; row < this.minefield.length; row++) {
      clonedMinefield.push([]);
      for (col = 0; col < this.minefield[row].length; col++) {
        clonedMinefield[row].push(this.getTile(row, col));
      }
    }
    return new Minefield(clonedMinefield, this.n);
  };
  
  // Make a getUnknownTiles() function and a getNumericTiles() function?
  this.getTile = function(row, col) {
    return this.minefield[row][col].clone();
  };
  this.getUnclonedTile = function(row, col) {
    return this.minefield[row][col];
  };
  this.getTiles = function() {
    var tiles = [], row, col;
    for (row = 0; row < this.minefield.length; row++) {
      for (col = 0; col < this.minefield[row].length; col++) {
        tiles.push(this.getTile(row, col));
      }
    }
    return tiles;
  };
  this.getUnclonedTiles = function() {
    var tiles = [], row, col;
    for (row = 0; row < this.minefield.length; row++) {
      for (col = 0; col < this.minefield[row].length; col++) {
        tiles.push(this.getUnclonedTile(row, col));
      }
    }
    return tiles;
  };
  this.getTilesSurrounding = function(tile) {
    var tiles = [], i, j;
    for (i = tile.row - 1; i <= tile.row + 1; i++) {
      for (j = tile.col - 1; j <= tile.col + 1; j++) {
        if ((i == tile.row && j == tile.col) || i < 0 || i > this.minefield.length-1 || j < 0 || j > this.minefield[i].length-1) { continue; }
        tiles.push(this.getTile(i, j));
      }
    }
    return tiles;
  };
  this.getUnclonedTilesSurrounding = function(tile) {
    var tiles = [], i, j;
    for (i = tile.row - 1; i <= tile.row + 1; i++) {
      for (j = tile.col - 1; j <= tile.col + 1; j++) {
        if ((i == tile.row && j == tile.col) || i < 0 || i > this.minefield.length-1 || j < 0 || j > this.minefield[i].length-1) { continue; }
        tiles.push(this.getUnclonedTile(i, j));
      }
    }
    return tiles;
  };
  this.getUnknownTiles = function() {
    return this.getTiles().filter(function(tile) { return tile.value == "?"; });
  };
  this.getUnclonedUnknownTiles = function() {
    return this.getUnclonedTiles().filter(function(tile) { return tile.value == "?"; });
  };
  this.getNumericTiles = function() {
    return this.getTiles().filter(function(tile) { return typeof tile.value == "number"; });
  };
  this.getUnclonedNumericTiles = function() {
    return this.getUnclonedTiles().filter(function(tile) { return typeof tile.value == "number"; });
  };
  this.set = function(tile) {
    this.minefield[tile.row][tile.col] = tile;
  };
  this.open = function(tile) {
    this.set(new Tile(tile.row, tile.col, parseInt(open(tile.row, tile.col))));
    this.getUnclonedTile(tile.row, tile.col).updateWorkingValue(this);
  };
  this.flag = function(tile) {
    this.set(new Tile(tile.row, tile.col, "x"));
  };
  
  this.findSafeTiles = function() {
    // For all unknown tiles, if any surrounding tile has a this.workingValue of 0, it's safe to open.
    var safeTiles = [];
    
    var unknownTiles = this.getUnknownTiles();
    unknownTiles.forEach(function(unknownTile) {
      var neighborsWithWorkingValueZero = this.getTilesSurrounding(unknownTile).filter(function(tile) { return tile.workingValue == 0; });
      if (neighborsWithWorkingValueZero.length > 0) {
        safeTiles.push(unknownTile);
      }
    }, this);
    
    // If any the board's mines have all been flagged, all leftover squares are open.
    if (this.getTiles().filter(function(tile) { return tile.value == "x"; }).length == this.n) {
      this.getUnclonedUnknownTiles().forEach(function(leftOverTile) { safeTiles.push(leftOverTile); });
    }
    
    return safeTiles;
  };
  this.findMines = function() {
    // For all numeric tiles with a this.workingValue > 0, if the number of unknown surrounding tiles equals this.workingValue, all surrounding tiles must be mines and should be flagged.
    var mines = [];
    
    var nonZeroNumericTiles = this.getUnclonedNumericTiles().filter(function(tile) { return tile.value > 0; });
    nonZeroNumericTiles.forEach(function(numericTile) {
      var surroundingUnknowns = this.getUnclonedTilesSurrounding(numericTile).filter(function(tile) { return tile.value == "?"; });
      if (surroundingUnknowns.length == numericTile.workingValue) {
        // All surrounding unknowns must be mines: flag them.
        surroundingUnknowns.forEach(function(mine) {
          mines.push(mine);
          this.getUnclonedTilesSurrounding(mine).filter(function(tile) { return typeof tile.value == "number"; }).forEach(function(tile) {
            tile.workingValue -= 1;
          }, this);
        }, this);
      }
    }, this);
    
    return mines;
  };
  this.iterateEasyLogic = function() {
    /***
      1) Logically open tiles.
      2) Logically flag mines.
    ***/
    var changedTiles = []; // For recording actions as they occur. It will also be helpful when deciding whether or not to try a contradiction search, because it will tell us if nothing happened.
    
    // 1)
    this.findSafeTiles().forEach(function(safeTile) {
      changedTiles.push(safeTile);
      this.open(safeTile);
    }, this);
    
    // 2)
    this.findMines().forEach(function(mine) {
      changedTiles.push(mine);
      this.flag(mine);
    }, this);
    
    return changedTiles;
  };
  
  this.contradictionSearch = function() {
    /***
      Until a safe square is found, every unknown tile bordered by a numeric tile, one by one, can be assumed to be a mine.
      From that assumption, a modified easyLogic* would be run until either
        A) the modified easy logic runs out moves to make. At this point, abort and try the next tile.
        B) the modified easy logic runs into an impossibility, such as a 2 tile with 3 surrounding mines.
           That tile cannot be a mine because it caused an impossibility as one, so it must be safe.
      
      * The modified easy logic would not open any tiles. As it's running off of an assumption, this would be dangerous.
        Rather, it would note how existing tiles would update if it was a mine, and flag more mines (still hypothetically)
        based off of this assumption, until either A or B occurs.
    ***/
    
    var unknownTilesBorderingNumericTiles = this.getUnknownTiles().filter(function(unknownTile) {
      return this.getTilesSurrounding(unknownTile).filter(function(tile) { return typeof tile.value == "number"; }).length > 0;
    }, this);
    
    var unknownTile, hypotheticalMinefield, hypotheticalMines, impossibilities, strandedTiles, minesLeftToFlag;
    for (var i in unknownTilesBorderingNumericTiles) {
      unknownTile = unknownTilesBorderingNumericTiles[i];
      
      minesLeftToFlag = this.n - this.getTiles().filter(function(tile) { return tile.value == "x"; }).length; // How many mines
      
      hypotheticalMinefield = this.clone();
      
      hypotheticalMinefield.getUnclonedNumericTiles()
        .filter(function(numericTile) { return numericTile.value > 0; })
        .forEach(function(numericTile) { numericTile.updateWorkingValue(hypotheticalMinefield); });
      
      var addPlaceholderNumbersAround = function(assumptionMine) {
       hypotheticalMinefield.getUnclonedTilesSurrounding(assumptionMine)
          .filter(function(tile) { return tile.workingValue == 0; })
          .forEach(function(numericTile) {
            hypotheticalMinefield.getUnclonedTilesSurrounding(numericTile)
            .filter(function(tile) { return tile.value == "?"; })
            .forEach(function(tile) {
              tile.value = "#"; tile.workingValue = "#";
            });
          });
      }
      
      // Update working values around the assumption mine.
      var hypotheticalAssumptionMine = hypotheticalMinefield.getUnclonedTile(unknownTile.row, unknownTile.col);
      hypotheticalAssumptionMine.value = "*"; hypotheticalAssumptionMine.workingValue = "*";
      hypotheticalMinefield.getUnclonedTilesSurrounding(unknownTile).filter(function(tile) { return typeof tile.value == "number"; }).forEach(function(numericTile) {
        numericTile.workingValue -= 1;
      });
      addPlaceholderNumbersAround(hypotheticalAssumptionMine);
      minesLeftToFlag -= 1;
      
      do {
        hypotheticalMines = hypotheticalMinefield.findMines(); // A
        hypotheticalMines.forEach(function(hypotheticalMine) {
          hypotheticalMine.value = "*"; hypotheticalMine.workingValue = "*";
          addPlaceholderNumbersAround(hypotheticalMine);
        });
        minesLeftToFlag -= hypotheticalMines.length;
        if (minesLeftToFlag == 0) {
          // All tiles are safe, for all mines have been flagged.
          hypotheticalMinefield.getUnclonedUnknownTiles().forEach(function(unknownTile) {
            unknownTile.value =  "#"; unknownTile.workingValue =  "#";
          });
        }
        // B part 1: Are there any tiles with too many mines around them?
        impossibilities = hypotheticalMinefield.getNumericTiles()
          .filter(function(numericTile) { return numericTile.workingValue < 0; });
        // B part 2: Are there any "stranded" tiles who need more mines than they have unknown tiles around them?
        strandedTiles = hypotheticalMinefield.getNumericTiles().filter(function(numericTile) {
          return numericTile.workingValue > hypotheticalMinefield.getTilesSurrounding(numericTile).filter(function(tile) {
            return tile.value == "?";
          }).length;
        });
        strandedTiles.forEach(function(strandedTile) {
          impossibilities.push(strandedTile);
        });
        // B part 3: Are there more mines on the board than there can be?
        if (minesLeftToFlag < 0) {
          impossibilities.push("impossible number of mines");
        }
      } while(hypotheticalMines.length > 0 && impossibilities.length == 0);
      
      if (impossibilities.length > 0) {
        // Impossibility found: the original assumption mine cannot be. It must be safe!
        this.open(unknownTile);
        return unknownTile;
      }
    }
    
    // No impossibilities found: the board must be ambiguous, impossible to solve!
    console.log(minefieldMatrixToString(minefieldTilesToMatrix(this.minefield)));
    return "?";
  };
}

function minefieldStringToMatrix(string) {
  var minefield = string.split("\n"), row;
  for (row = 0; row < minefield.length; row++) {
    minefield[row] = minefield[row].split(" ");
  }
  return minefield;
}
function minefieldMatrixToString(matrix) {
  var minefield = "", row, col;
  for (row = 0; row < matrix.length; row++) {
    for (col = 0; col < matrix[row].length; col++) {
      minefield += matrix[row][col];
      minefield += (col == matrix[row].length-1) ? (row == matrix.length-1 ? "" : "\n") : " ";
    }
  }
  return minefield;
}
function minefieldMatrixToTiles(matrix) {
  var minefield = [], row, col, value;
  for (row = 0; row < matrix.length; row++) {
    minefield.push([]);
    for (col = 0; col < matrix[row].length; col++) {
      value = matrix[row][col];
      if (typeof value == "number") {
        parseInt(value);
      }
      minefield[row].push(new Tile(row, col, value));
    }
  }
  return minefield;
}
function minefieldTilesToMatrix(tiles) {
  var minefield = [], row, col, value;
  for (row = 0; row < tiles.length; row++) {
    minefield.push([]);
    for (col = 0; col < tiles[row].length; col++) {
      value = tiles[row][col].value;
      if (typeof value == "number") {
        value.toString();
      }
      minefield[row].push(value);
    }
  }
  return minefield;
}

function solveMine(map,n) {
  var minefield = new Minefield(map, n), easyLogic, contradictionSearch;
  while (minefield.getUnknownTiles().length > 0) {
    easyLogic = minefield.iterateEasyLogic();
    if (easyLogic.length == 0) {
      // easyLogic did nothing, so try a contradiction search.
      contradictionSearch = minefield.contradictionSearch();
      if (contradictionSearch == "?") {
        // The board is ambiguous, impossible to solve.
        return "?";
      }
    }
  }
  
  return minefieldMatrixToString(minefieldTilesToMatrix(minefield.minefield));
}
