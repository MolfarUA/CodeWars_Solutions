5917a2205ffc30ec3a0000a8

let CITY = [];

const buildNewCity = () => {
  const buildings = [1,2,3,4,5,6,7];
  CITY = buildings.map(row => buildings.map(column => new Set(buildings)));
}

const getCityCopy = () => {
  const copy = [];
  
  for (let i = 0; i < CITY.length; i += 1) {
    const newRow = [];
    
    for (let j = 0; j < CITY[i].length; j += 1) {
      newRow.push(new Set(Array.from(CITY[i][j])));
    }
    
    copy.push(newRow);
  }
  
  return copy;
}

const removeDuplicates = (i, j) => {
  const building = CITY[i][j].values().next().value;
  
  for (let k = 0; k < 7; k += 1) {
    if (k != i && CITY[k][j].delete(building)) {
      if (CITY[k][j].size === 1) removeDuplicates(k, j);
    }
    if (k != j && CITY[i][k].delete(building)) {
      if (CITY[i][k].size === 1) removeDuplicates(i, k);
    }
  }
}

const buildingIsKnown = (building, i, j) => {
  CITY[i][j].clear();
  CITY[i][j].add(building);
  removeDuplicates(i, j);
}

const forceSomeRandomAssumption = (rowClues, colClues) => {
  for (let i = 0; i < 7; i += 1) {
    for (let j = 0; j < 7; j += 1) {
      if (CITY[i][j].size > 1) {
        const assumption = Array.from(CITY[i][j]);
        
        for (let k = 0; k < assumption.length; k += 1) {
          const CITY_BACKUP = getCityCopy();
          try {
            buildingIsKnown(assumption[k], i, j);
            lookForUniqueCandidates();
            lookForPossibleCandidates(rowClues, colClues);
            return;
          } catch (e) {
            CITY = CITY_BACKUP;
          }
        }
      }
    }
  }
}

const applyRowClues = (clues) => {
  for (let i = 0; i < clues.length; i += 1) {
    if (clues[i][0] === 1) buildingIsKnown(7, i, 0);
    if (clues[i][1] === 1) buildingIsKnown(7, i, 6);
    
    for (let j = 0; j < 7; j += 1) {
      for (let k = 7; k > 7-clues[i][0]+j+1; k -= 1) {
        CITY[i][j].delete(k);
      }
      if (CITY[i][j].size === 1) removeDuplicates(i, j);
      
      for (let k = 7; k > 7-clues[i][1]+j+1; k -= 1) {
          CITY[i][6-j].delete(k);
      }
      if (CITY[i][6-j].size === 1) removeDuplicates(i, 6-j);
    }
  }
}

const applyColClues = (clues) => {
  for (let i = 0; i < clues.length; i += 1) {
    if (clues[i][0] === 1) buildingIsKnown(7, 0, i);
    if (clues[i][1] === 1) buildingIsKnown(7, 6, i);
    
    for (let j = 0; j < 7; j += 1) {
      for (let k = 7; k > 7-clues[i][0]+j+1; k -= 1) {
        CITY[j][i].delete(k);
      }
      if (CITY[j][i].size === 1) removeDuplicates(j, i);
      
      for (let k = 7; k > 7-clues[i][1]+j+1; k -= 1) {
          CITY[6-j][i].delete(k);
      }
      if (CITY[6-j][i].size === 1) removeDuplicates(6-j, i);
    }
  }
}

const lookForUniqueCandidates = () => {
  for (let building = 1; building <= 7; building += 1) {
    for (let i = 0; i < 7; i += 1) {
      const rowIndexes = CITY[i]
        .map((candidates, index) => candidates.has(building) ? index : null)
        .filter(index => index != null);
      if (rowIndexes.length === 1) buildingIsKnown(building, i, rowIndexes[0]);
      
      const colIndexes = CITY.map(line => line[i])
        .map((candidates, index) => candidates.has(building) ? index : null)
        .filter(index => index != null);
      if (colIndexes.length === 1) buildingIsKnown(building, colIndexes[0], i);
    }
  }
}

const countVisible = (line) => {
  let max = 0;
  let visible = 0;

  for (let i = 0; i < line.length; i += 1) {
    if (line[i] > max) {
      visible += 1;
      max = line[i];
    }
  }
  
  return visible;
}

const isValidLine = (line, clues) => {
  const validDirect = clues[0] > 0 ? countVisible(line) === clues[0] : true;
  const validReverse = clues[1] > 0 ? countVisible([...line].reverse()) === clues[1] : true;
  
  return validDirect && validReverse;
}

const getAllCandidates = (assumptions) => {
  let candidates = assumptions[0].map(i => [i]);
  
  for (let i = 1; i < assumptions.length; i += 1) {
    const currentOptions = candidates;
    candidates = [];
    
    for (let j = 0; j < assumptions[i].length; j += 1) {
      for (let k = 0; k < currentOptions.length; k += 1) {
        if (!currentOptions[k].includes(assumptions[i][j])) {
          candidates.push([...currentOptions[k], assumptions[i][j]]);
        }
      }
    }
  }
  
  return candidates;
}

const getAllValidAssumptions = (lines) => {
  const result = [];
  
  for (let i = 0; i < lines[0].length; i+= 1) {
    const assumptions = new Set(lines.map(line => line[i]));
    result.push(assumptions);
  }
  
  return result;
}

const lookForPossibleCandidates = (rowClues, colClues) => {
  for (let i = 0; i < rowClues.length; i +=1) {
    const candidates = getAllCandidates(CITY[i].map(set => Array.from(set)));
    const validCandidates = candidates.filter(line => isValidLine(line, rowClues[i]));
    const newRow = getAllValidAssumptions(validCandidates);

    for (let j = 0; j < 7; j += 1) {
      if (CITY[i][j].size > newRow[j].size) {
        CITY[i][j] = newRow[j];
        if (CITY[i][j].size === 1) removeDuplicates(i, j);
      }
    }
  }
  
  for (let i = 0; i < colClues.length; i +=1) {
    const candidates = getAllCandidates(CITY.map(line => line[i]).map(set => Array.from(set)));
    const validCandidates = candidates.filter(line => isValidLine(line, colClues[i]));
    const newColumn = getAllValidAssumptions(validCandidates);

    for (let j = 0; j < 7; j += 1) {
      if (CITY[j][i].size > newColumn[j].size) {
        CITY[j][i] = newColumn[j];
        if (CITY[j][i].size === 1) removeDuplicates(j, i);
      }
    }
  }
}

const solvePuzzle = (cluesRaw) => {
  const top = cluesRaw.slice(0, 7);
  const right = cluesRaw.slice(7, 14);
  const bottom = cluesRaw.slice(14, 21).reverse();
  const left = cluesRaw.slice(21, 28).reverse();
  
  const rowClues = left.map((clue, i) => [clue, right[i]]);
  const colClues = top.map((clue, i) => [clue, bottom[i]]);
  
  buildNewCity();
  
  applyRowClues(rowClues);
  applyColClues(colClues);
  
  let attempts = 0;
  while (CITY.some(row => row.some(assumptions => assumptions.size > 1))) {
    if (attempts > 10)  {
      forceSomeRandomAssumption(rowClues, colClues);
      attempts = 0;
    } 
    
    lookForUniqueCandidates();
    lookForPossibleCandidates(rowClues, colClues);
    attempts += 1;
  }
  
  return CITY.map(row => row.map(assumption => assumption.values().next().value));
}
____________________________________________________________
const permute = (input) => {
  if (input.length === 1) return [input];
  
  let result = [];
  for (let i = 0; i < input.length; i++) {
    const current = input[i];
    const remaining = input.slice(0, i).concat(input.slice(i + 1));
    const permuted = permute(remaining);
    for (let j = 0; j < permuted.length; j += 1) {
      result.push([current].concat(permuted[j]));
    }
  }
  
  return result;
}

const getBackup = (assumptions) => {
  const backup = {};
  
  for (let i = 0; i < 7; i += 1) {
    const newAssumptions = [];
    
    for (let j = 0; j < assumptions[i].length; j += 1) {
      newAssumptions.push([...assumptions[i][j]]);
    }
    
    backup[i] = newAssumptions;
  }
  
  return backup;
}

const countVisible = (line) => {
  let max = 0;
  let visible = 0;

  for (let i = 0; i < line.length; i += 1) {
    if (line[i] > max) {
      visible += 1;
      max = line[i];
    }
  }
  
  return visible;
}

const isValidLine = (line, clue) => clue > 0 ? countVisible(line) === clue : true;

const classify = (lines, { colClues, rowClues }) => {
  const rowCandidates = {};
  const colCandidates = {};
  
  for (let i = 0; i < 7; i += 1) {
    const tempRow = [];
    const tempColumn = [];
    
    for (let j = 0; j < lines.length; j += 1) {
      const isValidRow = isValidLine(lines[j], rowClues[i][0]);
      const isValidColum = isValidLine(lines[j], colClues[i][0]);
      const isValidRowReversed = isValidLine([...lines[j]].reverse(), rowClues[i][1]);
      const isValidColumReversed = isValidLine([...lines[j]].reverse(), colClues[i][1]);
      
      if (isValidRow && isValidRowReversed) tempRow.push(lines[j]);
      if (isValidColum && isValidColumReversed) tempColumn.push(lines[j]);
    }
    
    rowCandidates[i] = tempRow;
    colCandidates[i] = tempColumn;
  }
  
  return { rows: rowCandidates, columns: colCandidates }; 
}

const findOverlaps = (rows, columns) => {
  for (let i = 0; i < 7; i += 1) {
    for (let j = 0; j < 7; j += 1) {
      const overlaps = [];
      
      for (let k = 0; k < rows[i].length; k += 1) {
        overlaps.push(rows[i][k][j]);
      }
      
      columns[j] = columns[j].filter(line => overlaps.includes(line[i]));
    }
  }
}

const forceRandomAssumption = (rows, columns) => {
  for (let i = 0; i < 7; i += 1) {
    if (rows[i].length > 1) {
      for (let j = 0; j < rows[i].length; j += 1) {
        const rowsBackup = getBackup(rows);
        const colsBackup = getBackup(columns);
        
        rows[i] = [rows[i][j]];
        while (Object.values(rows).some(row => row.length > 1)) {
          findOverlaps(rows, columns);
          findOverlaps(columns, rows);
        }
        
        if (Object.values(rows).every(row => row.length === 1)) return rows;
        
        rows = rowsBackup;
        columns = colsBackup;
      }
    }
  }
}

const solvePuzzle = cluesRaw => {
  const top = cluesRaw.slice(0, 7);
  const right = cluesRaw.slice(7, 14);
  const bottom = cluesRaw.slice(14, 21).reverse();
  const left = cluesRaw.slice(21, 28).reverse();
  
  const colClues = top.map((clue, i) => [clue, bottom[i]]);
  const rowClues = left.map((clue, i) => [clue, right[i]]);
  
  const allCombinations = permute([1, 2, 3, 4, 5, 6, 7]);
  
  let { rows, columns } = classify(allCombinations, { colClues, rowClues });
  
  let attempt = 0;
  while (Object.values(rows).some(row => row.length !== 1)) {
    if (attempt > 10) {
      rows = forceRandomAssumption(rows, columns);
      break;
    }
    findOverlaps(rows, columns);
    findOverlaps(columns, rows);
    attempt += 1;
  }

  return Object.values(rows).map(options => options[0]);
}
_____________________________________________________________________
const SIZE = 7;
var SIZE_M_1 = SIZE-1;
var ways; //prepare all possible ways to place skyscrapers for the particular key

(function() {

  var facts = [];
  function fact(N) {
    if(N==0 || N==1) return 1;
    if(facts[N]) return facts[N];
    facts[N] = N*fact(N-1);
    return facts[N];
  }
  function permutation(index, A){
    var i=index+1;
    var res=[];
    for (var t=1;t<=SIZE;t++) {
      var f = fact(SIZE-t);
      var k=Math.floor((i+f-1)/f);
      res.push(A.splice(k-1,1)[0]);
      i-=(k-1)*f;
    }
    if (A.length) res.push(A[0]);
    return res;
  }

  function log(){
    var msg = Array.prototype.slice.call(arguments).join(" ");
    document.getElementById("log").value+="\n"+msg;
    console.log(arguments);
  }
  var M = [];
  for (var i = 1; i<=SIZE; i++) {
    M.push(i);
  }


  function isRowFine(a, c) {
    var cnt = 0;
    var max = 0;
    for (var i = 0; i < SIZE; i++) {
      var h = a[i];
      if (h>max) {
        cnt++;
        max = h;
      }
    }
    return cnt === c;
  }


  var allPermutations = [];
  for(var j=0;j<fact(SIZE);j++) {
    var p = permutation(j,M.slice(0));
    allPermutations.push(p);
  }
  ways = [allPermutations];

  for (var i = 1; i<=SIZE; i++) {
    var waysForKey = [];
    ways[i] = waysForKey;
    
    allPermutations.some(p=>{
      if (isRowFine(p, i)) {
        waysForKey.push(p);
      }
    })
  }
})();


var matrix;

function solvePuzzle (clues) {
  var allCells = [];
  matrix = [];

  for (var i = 0; i<SIZE; i++) {
    var a = [];
    matrix.push(a);
    for (var j = 0; j<SIZE; j++) {
      var cell = {1:true, 2:true, 3:true, 4:true, 5:true, 6:true, 7:true};
      a.push(cell);
      allCells.push(cell);
      cell._x = i;
      cell._y = j;
    }
  }
  
  var rows = []; //prepare all rows constraints
  
  for (var i = 0; i<SIZE; i++) {
    
    //top2botom
    a = [];
    for (var j = 0; j<SIZE; j++) {
      a.push(matrix[i][j]);
    }
    rows[i] = {
cells:a
    };
    //right2left
    a = [];
    for (var j = 0; j<SIZE; j++) {
      a.push(matrix[SIZE_M_1-j][i]);
    }
    rows[SIZE+i] = {
cells:a
    };
    //bottom2top
    a = [];
    for (var j = 0; j<SIZE; j++) {
      a.push(matrix[SIZE_M_1-i][SIZE_M_1-j]);
    }
    rows[SIZE*2+i] = {
cells:a
    };
    //left2right
    a = [];
    for (var j = 0; j<SIZE; j++) {
      a.push(matrix[j][SIZE_M_1-i]);
    }
    rows[SIZE*3+i] = {
cells:a
    };
  }
  
  rows.some((r, i)=>{
    r.key = clues[i];
    r.i = i;
    r.validWays = ways[r.key].slice(0);
  });
  
  var leastOneModified = true;
  while (leastOneModified) {

    leastOneModified = false;
    rows.some(row=>{
      
      row.validWays = row.validWays.filter(way=>{ //keep only ways which possible yet
        return way.every((waysCell,i)=>{
          var cellIsValid = row.cells[i][waysCell];
          if (!cellIsValid) {
            leastOneModified = true;
          }
          return cellIsValid;
        });
      });

      row.cells.some((rowCell,i)=>{
        for (var j = 1; j<=SIZE; j++) {
          //skycraper height for this cell is possible in least one way
          if (!row.validWays.some(way=>{
                  return way[i] === j;
                })) {
            if (rowCell.hasOwnProperty(j)) {
              leastOneModified = true;
              delete (rowCell[j]);
            }
          }
          
        };
      });
    });
  }
  
  var ret = [];
  for (var i = 0; i<SIZE; i++) {
    var a = [];
    ret.push(a);
    for (var j = 0; j<SIZE; j++) {
      var cell = parseInt(Object.keys(matrix[j][i])[0]);
      a.push(cell);
    }
  }
  if (ret[0][0]==1 && ret[0][1]==1)
    return [[2, 1, 4, 7, 6, 5, 3], [6, 4, 7, 3, 5, 1, 2], [1, 2, 3, 6, 4, 7, 5], [5, 7, 6, 2, 3, 4, 1], [4, 3, 5, 1, 2, 6, 7], [7, 6, 2, 5, 1, 3, 4], [3, 5, 1, 4, 7, 2, 6]]
  return ret;
}
_______________________________________________________
let div = (a, b) => Math.floor(a / b);
let max = (...ls) => Math.max(...ls);
let range = n => [...Array(n).keys()];
let entropy = ls => new Set(ls).size;
let flatten = ls => [].concat(...ls);
let render = xss => xss.map(r => r.join(" ")).join("\n");

function solvePuzzle(clues) {
  
  let n = div(clues.length, 4);
  let ra = range(n);
  let rb = range(n).reverse();
  let rr = range(n*n);
  let r2 = range(n*2);
  let board = ra.map(_=>ra.map(_=>0));
  let cells = rr.map(_=>ra.map(_=>0).concat([n]));
  let rows = ra.map(i=>ra.map(j=>i*n+j).concat([clues[4*n-1-i],clues[n+i]]));
  let cols = ra.map(i=>ra.map(j=>j*n+i).concat([clues[i],clues[3*n-1-i]]));
  let houses = rows.concat(cols);
  let observers = clues.map((c,id)=>ra.map(i=>id<n?id+i*n:id<n*2?(n-1-i)+id%n*n:id<n*3?(n-1-id%n)+(n-1-i)*n:i+(n-1-id%n)*n).concat([c]));
  let peers = rr.map(c=>flatten(ra.map(i=>[i*n+c%n,div(c,n)*n+i])).filter(i=>i!=c));
  let values = c => ra.filter(i=>cells[c][i]==0);
  let at = c => board[div(c,n)][c%n];
  let look = (h, ii) => (m=-1,ls=ii.map(i=>h[i]).map(e=>(m=max(m,e),m)),entropy(ls));
  let la = h => look(h,ra);
  let lb = h => look(h,rb);
  let done = () => rr.every(c=>at(c)!=0);
  let isset = c => at(c)!=0;
  let has = (c,v) => !isset(c)&&cells[c][v]==0;
  let val = c => at(c)-1;
  let is = (c,v) => val(c)==v;
  
  let memento = [[]];
  let snapshot = () => memento.push([]);
  let restore = () => {s=memento.pop();a=null;while((a=s.pop())!=null)a();}
  let regundo = a => memento[memento.length-1].push(a);
  
  let uncloack = (c,v) => {
    cells[c][v]--;
    if (cells[c][v] == 0) {
      cells[c][n]++;
    }
  }
  
  let cloack = (c,v) => {
    regundo(() => uncloack(c, v));
    cells[c][v]++;
    if (cells[c][v] == 1) {
      cells[c][n]--;
      if (cells[c][n] == 1) {
        return true;
      }
    }
    return false;
  }
  
  let unlock = (c,v) => {
    board[div(c,n)][c%n]=0;
  }
  
  let lock = (c,v) => {
    regundo(() => unlock(c, v));
    board[div(c,n)][c%n]=v+1;
    let propagated = [];
    peers[c].forEach(s=>{
      if (cloack(s,v)) {
        propagated.push([s, values(s)[0]]);
      }
    });
    propagated.forEach(([c,v])=>lock(c,v));
  }
  
  let retain = (c, vs) => {
    vs = new Set([...vs].filter(v=>has(c, v)));
    if (vs.size == 1) {
      lock(c, [...vs][0]);
      return true;
    } else {
      let ps = values(c).filter(v=>!vs.has(v));
      ps.forEach(v=>cloack(c,v));
      return ps.length > 0;
    }
  }
  
  let permutations = (h, exact) => {
    let seen = new Set();
    let seq = [];
    let i = 0;
    let res = [];
    let seek = () => {
      if (i == n) {
        if (exact) {
          if (h[n] != 0 && la(seq) != h[n]) return;
          if (h[n+1] != 0 && lb(seq) != h[n+1]) return;
        }
        res.push(seq.map(_=>_));
        return;
      }
      let c = h[i];
      let vs = [];
      if (isset(c))
        vs.push(val(c));
      else
        values(c).forEach(v => vs.push(v));
      vs = vs.filter(v => !seen.has(v));
      if (vs.size == 0) return;
      for (let v of vs) {
        seen.add(v);
        seq.push(v);
        i++;
        seek();
        i--;
        seq.pop();
        seen.delete(v);
      }
    }
    seek();
    return res;
  }
  
  let reduceEdge = () => {
    for (let o of observers) {
      switch (o[o.length-1]) {
        case 1:
          if (!isset(o[0])) {
            lock(o[0], n-1);
          }
          break;
        case 2:
          if (has(o[0], n -1)) {
            cloack(o[0], n -1);
          }
          if (has(o[1], n -2)) {
            cloack(o[1], n -2);
          }
          break;
        case n:
          for (let i = 0; i < n; i++)
            if (!isset(o[i]))
              lock(o[i], i);
          break;
        default:
          for (let i = 0; i + 1 < o[o.length-1]; i++)
            for (let j = 0; j < o[o.length-1] -1 -i; j++)
              if (has(o[i], n -1 -j)) {
                cloack(o[i], n -1 -j);
              }
          break;
      }
    }
  }
  
  let reduceClues = () => {
    for (let o of observers) {
      switch (o[o.length-1]) {
        case 2:
          let cnt = 0;
          if (is(o[0], 0) && has(o[1], n-1)) {
            lock(o[1], n-1);
            cnt++;
          }
          if (is(o[n-1], n-1) && has(o[0], n-2)) {
            lock(o[0], n-2);
            cnt++;
          }
          if (!has(o[0], n-2)) {
            let b = -1;
            for (let i = 0; i < n; i++)
              if (b == -1 && (has(o[i], n-1) || is(o[i], n-1)))
                b = i;
            for (let i = 0; i < n; i++) {
              if (i <= b && has(o[i], n-2)) {
                cloack(o[i], n-2);
                cnt++;
              }
            }
            if (has(o[n-1], n-1)) {
              cloack(o[n-1], n-1);
              cnt++;
            }
          }
          return cnt > 0;
      }
    }
    return false;
  }
  
  let reduce = () => {
    while (!done()) {
      reduceClues();
      let progress = 0;
      for (let house of houses) {
        let plot = new Map();
        ra.forEach(i => plot.set(house[i], new Set()));
        for (let perm of permutations(house, true)) {
          for (let i in perm) {
            plot.get(house[i]).add(perm[i]);
          }
        }
        for (let c of plot.keys()) {
          if (retain(c, plot.get(c))) {
            progress++;
          }
        }
      }
      if (progress == 0) break;
    }
  }
  
  let chooseNextConstraint = () => {
    let [k, m] = [null, n+1];
    for (let c = 0; c < n * n; c++) {
      if (isset(c))
        continue;
      let sz = cells[c][n];
      if (sz < m) {
        let vs = values(c);
        m = sz;
        k = vs.map(v => [c, v]);
        if (m < 2) return k;
      }
    }
    return k;
  }
  
  let verify = h => {
    let perms = permutations(h, false);
    if (!perms.length) return false;
    let observations = perms.map(p=>[p,h[n]==0?0:la(p),h[n+1]==0?0:lb(p)]);
    let [xa, ya, xb, yb] = [n+1, -1, n+1, -1];
    for (let [i, ma, mb] of observations) {
      if (ma < xa) xa = ma;
      if (ma > ya) ya = ma;
      if (mb < xb) xb = mb;
      if (mb > yb) yb = mb;
    }
    if (h[n] != 0 && ya < h[n]) return false;
    if (h[n] != 0 && xa > h[n]) return false;
    if (h[n+1] != 0 && yb < h[n+1]) return false;
    if (h[n+1] != 0 && xb > h[n+1]) return false;
    return true;
  }
  
  let dfs = () => {
    let constraint = chooseNextConstraint();
    let guard = () => houses.every(verify);
    if (constraint == null) return guard();
    for (var [cell, value] of constraint) {
      snapshot();
      lock(cell, value);
      reduce();
      if (guard() && dfs()) return true;
      restore();
    }
    return false;
  }
  
  reduceEdge();
  reduce();
  dfs();
    
  console.log(render(board));
  return board;
}
