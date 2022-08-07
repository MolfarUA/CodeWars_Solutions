5a20eeccee1aae3cbc000090


function slidePuzzle(arr,o=0){
  const find=n=>{
    var y=arr.findIndex(r=>r.includes(n));
    return [arr[y].indexOf(n),y];
  }
  var p=[], s=arr.length, [x,y]=find(0);
  const mov=d=>{
    if(d==='u') {[arr[y][x],arr[y-1][x]]=[arr[y-1][x],arr[y][x]]; p.push(arr[y--][x]);}
    else if(d==='l') {[arr[y][x],arr[y][x-1]]=[arr[y][x-1],arr[y][x]]; p.push(arr[y][x--]);}
    else if(d==='r') {[arr[y][x],arr[y][x+1]]=[arr[y][x+1],arr[y][x]]; p.push(arr[y][x++]);}
    else if(d==='d') {[arr[y][x],arr[y+1][x]]=[arr[y+1][x],arr[y][x]]; p.push(arr[y++][x]);}
    else throw new Error(d);
  }
  const rL=_=>{while(y+1<s) mov('d'); while(x+1<s) mov('r');}, rG=_=>{while(x+1<s) mov('r'); while(y+1<s) mov('d');};
  const rc=(w,h)=>[...'l'.repeat(w)+'u'.repeat(h)+'r'.repeat(w)+'d'.repeat(h)].forEach(mov),
        rcc=(w,h)=>[...'u'.repeat(h)+'l'.repeat(w)+'d'.repeat(h)+'r'.repeat(w)].forEach(mov);
  var u=arr[0].map((_,i)=>o*(s+o+1)+i+1), l=arr.map((_,j)=>o*(s+o+1)+j*(s+o)+1);
  
  if(arr.length===2) {
    rL();
    while(arr[0][0]!==u[0]) rc(1,1);
    return arr[0][1]!==u[1]?null:p;
  }
  
  // top row
  for(let i=0; i<u.length-1; i++) {
    let [tx,ty]=find(u[i]);
    if(ty===0&&tx===i) continue;
    rL();
    [tx,ty]=find(u[i]);
    while(arr[s-1][s-2]!==u[i]) rc(s-1-tx||1,s-1-ty||1);
    while(arr[0][i]!==u[i]) rc(s-1-i,s-1);
  }
  rL();
  var c=u[u.length-1], [tx,ty]=find(c);
  if(ty!==0||tx!==s-1) {
    while(arr[s-2][s-1]!==c) rc(s-1-tx||1,s-1-ty||1);
    rcc(1,s-1);
    while(arr[1][s-1]!==c) rcc(1,s-2);
    rc(1,s-1);
  }
  
  // left col
  for(let j=0; j<l.length-1; j++) {
    let [tx,ty]=find(l[j]);
    if(tx===0&&ty===j) continue;
    rG();
    [tx,ty]=find(l[j]);
    while(arr[s-2][s-1]!==l[j]) rc(s-1-tx||1,s-1-ty||1);
    while(arr[j][0]!==l[j]) rc(s-1,s-1-j);
  }
  rG();
  var c=l[l.length-1], [tx,ty]=find(c);
  if(tx!==0||ty!==s-1) {
    while(arr[s-1][s-2]!==c) rc(s-1-tx||1,s-1-ty||1);
    rc(s-1,1);
    while(arr[s-1][1]!==c) rcc(s-2,1);
    rcc(s-1,1);
  }
  
  var n=slidePuzzle(arr.slice(1).map((r,j)=>r.slice(1)),o+1);
  return n?p.concat(n):n;
}
_________________________________________
const slidePuzzle = arr => {   // average time for this solution makes up ~1250ms

  const {PI, sin, cos, round, abs, sign} = Math;
  const flatArr = arr => arr.reduce((acc, item) => [...acc, ...item]); // Array.prototype.flat() still not working in CodeWars...
  
  // This checks if the puzzle is solvable
  const isSolvable = arr => flatArr(arr).reduce((acc, num1, idx, arrFlat) => 
                              acc + (num1 ? arrFlat.slice(idx+1).filter(num2 => num2 < num1 && num2).length
                                          : ~(idx / arr.length) * (arr.length + 1) % 2), 0) % 2 === 0;
  
  // This generates square path that will lead you around the point
  const manhattannRoundPath = ([offsetX, offsetY]) => {
    const circle = Array.from({length: 16}, (_, idx) => [round(cos(PI / 4 * idx)), round(sin(-PI / 4 * idx))]);
    const startIndex = circle.findIndex(([x, y]) => x === offsetX && y === offsetY);
    return(circle.slice(startIndex, startIndex + 9));
  } 
  
  const manhattannDistance = ([x1, y1], [x2, y2]) => abs(x2 - x1) + abs(y2 - y1); 
  
  // This is the universal strategy I used in childhood to solve the puzzle
  // It defines which piece with which number should be put to which place, step by step
  // It did work here as well
  const adoptStrategy = n => {  
    const mainBlock = Array.from({length: n - 2}, (_, rowIdx) => Array.from({length: n}, (_, colIdx) => 
                                 ({piece: rowIdx * n + colIdx + 1, x: colIdx, y: rowIdx})))
                           .map((block, idx) => (block.splice(-2, 0, 
                                 {piece: (idx + 1) * n    ,     x: n - 1,   y: idx + 2},
                                 {piece: (idx + 1) * n - 1,     x: n - 1,   y: idx},
                                 {piece: (idx + 1) * n    ,     x: n - 1,   y: idx + 1}), block));
    const lowerTwoLines = Array.from({length: n - 2}, (_, idx) => [
                                 {piece: n * (n - 1) + 1 + idx, x: idx + 2, y: n - 1},
                                 {piece: n * (n - 2) + 1 + idx, x: idx,     y: n - 1},
                                 {piece: n * (n - 1) + 1 + idx, x: idx + 1, y: n - 1}, 
                                 {piece: n * (n - 2) + 1 + idx, x: idx,     y: n - 2},
                                 {piece: n * (n - 1) + 1 + idx, x: idx,     y: n - 1}]);
    const lastThreePieces = [    {piece: n * (n - 1) - 1,       x: n - 2,   y: n - 2},
                                 {piece: n * (n - 1),           x: n - 1,   y: n - 2},
                                 {piece: n * n - 1,             x: n - 2,   y: n - 1}];
    
    return flatArr([...mainBlock, ...lowerTwoLines, lastThreePieces]);
  };
  
  // some functions to help the Deed
  const findPiece     = num => arr.reduce((acc, row, idx) => row.includes(num) ? [row.indexOf(num), idx] : acc, [0, 0]);
  const blockPiece    = piece => blockedPieces.push(piece);
  const isCellBlocked = ([x, y]) => x < 0 || y < 0 || x >= N || y >= N || blockedPieces.includes(arr[y][x]);
  
  // this makes one exact puzzle move - just moves exact piece to the empty place
  const movePiece = ([x, y]) => {
    if (x === zeroX && y === zeroY) return;
    
    solution.push(arr[y][x]);
    [ arr[y][x], arr[zeroY][zeroX] ] = [ 0, arr[y][x] ];
    [ zeroY, zeroX ] = [ y, x ];
  }
  
  // this brings empty cell next to the target cell
  const moveEmptyNextToPiece = ([x, y]) => {  
    const [dx, dy] = [x - zeroX, y - zeroY];
    if (dx ** 2 + dy ** 2 <= 2) return;
    
    const [offsetX, offsetY] = abs(dx) > 1 && !isCellBlocked([zeroX + sign(dx), zeroY]) ? [sign(dx), 0] : [0, sign(dy)]; 
    
    // when near border, sometimes we need to help computer; these extra lines allow to make general algorithm simpler
    if (!offsetX && offsetY === -1 && x === N - 1 && isCellBlocked([zeroX, zeroY - 1])) {
       movePiece([zeroX - 1, zeroY]); movePiece([zeroX, zeroY - 1]);
    }
    if (!offsetX && !offsetY) {
       movePiece([zeroX, zeroY - 1]); movePiece([zeroX - 1, zeroY]);
    } 
    
    movePiece([zeroX + offsetX, zeroY + offsetY])
    moveEmptyNextToPiece([x, y]);  //recursion until we reach the goal step by step
  }
  
  // this moves the empty cell to the position between the piece being moved 
  // and its target position and recursively moves it step by step until it occupies the target place
  const movePieceToTarget = ([x, y], [targetX, targetY]) => {
    const currDiplacement = manhattannDistance([x, y], [targetX, targetY]);
    if (!currDiplacement) return;
    
    const targetPiece = arr[y][x];
     
    const circle = manhattannRoundPath([zeroX - x, zeroY - y])
                     .map(([offsetX, offsetY]) => [x + offsetX, y + offsetY])
                     .map(cell => isCellBlocked(cell) ? null : cell);
    const circlePath        = circle          .slice(1, circle.indexOf(null));
    const circleCounterPath = circle.reverse().slice(1, circle.indexOf(null));  
    const finalPointInPath        = circlePath       .findIndex(([x1, y1]) => manhattannDistance([x1, y1], [targetX, targetY]) === currDiplacement - 1);
    const finalPointInCounterPath = circleCounterPath.findIndex(([x1, y1]) => manhattannDistance([x1, y1], [targetX, targetY]) === currDiplacement - 1);

    const goodPath = finalPointInPath !== -1 ? circlePath       .slice(0, finalPointInPath + 1) 
                                             : circleCounterPath.slice(0, finalPointInCounterPath + 1);
    [...goodPath, [x, y]].forEach(movePiece);
    
    return movePieceToTarget(findPiece(targetPiece), [targetX, targetY]); //recursion until we reach the goal step by step
  }
  
  // this invokes the necessary functions to move each exact piece to its target location
  const putPieceToTargetLocation = ({piece, x, y}) => {
    const targetPiece = findPiece(piece);
    moveEmptyNextToPiece(targetPiece);
    movePieceToTarget(targetPiece, [x, y]);  
    (abs(x - (piece - 1) % N) <= 1 && abs(y - ~~((piece - 1) / N)) <= 1) && blockPiece(piece);
  }
   
//   prettyPrint(arr);  // try this stuff :)
  if (!isSolvable(arr)) return null;
  
  const N = arr.length;
  let [zeroX, zeroY] = findPiece(0);

  const blockedPieces = [];
  const solution = [];
  
  adoptStrategy(N).forEach(putPieceToTargetLocation); // successively moves each piece to its target location according to the universal strategy
  
  return solution;
}
_________________________________________
function slidePuzzle(p){
    const N = p.length, result = [], ɸ = {'U':[-1,0],'D':[1,0],'L':[0,-1],'R':[0,1]},
    R=[...Array(N).keys()],set=new Set(),j=(r,c)=>[r,c].join(','),
    
    // utility functions
    manh =(r,c,R,C,a=Math.abs)=>a(R-r)+a(C-c),
    xpos =x=> { for(let r of R)for(let c of R)if(p[r][c] === x)return[r,c] },
    safe =(r,c)=> r >= 0 && r < N && c >= 0 && c < N && !set.has(j(r,c)),
    move =(d,[r,c]=xpos(0))=>{const D=ɸ[d],R=D[0]+r,C=D[1]+c,t=p[r][c];p[r][c]=p[R][C],p[R][C]=t;result.push(p[r][c])},
    mov0 =(r,c,p0hb={})=> {
      while(p[r][c] !== 0){
        const [R,C]=xpos(0),x=j(R,C),l=[]
        if (x in p0hb) p0hb[x]++; else p0hb[x] = 1
        for (let d in ɸ) {
          const D=ɸ[d],Y=R+D[0],X=C+D[1],y=p0hb[j(Y,X)] 
          if (safe(Y,X)) l.push([y|0,manh(r,c,Y,X),d])
        }
        l.sort()
        move(l[0][2])
      }
    },
    movx =(x,r,c,pxhb=new Set())=> {
      while (p[r][c] !== x) {
        const [R,C] = xpos(x), t = j(R,C), l = []
        pxhb.add(t); set.add(t)
        for (let d in ɸ) {
          const D=ɸ[d],Y=R+D[0],X=C+D[1]
          if (safe(Y,X)) l.push([manh(r,c,Y,X),Y,X])
        }
        l.sort()
        let y = 0, L = l.length
        while (y < L && pxhb.has(j(l[y][1],l[y][2]))) y++
        if (L > y) {
          mov0(l[y][1],l[y][2])
          set.delete(t)
          mov0(R,C)
        }
      }
    },
    xflip =()=> [...'LURRDLULDRRULLDRULDR'].forEach(d=> move(d)),
    yflip =()=> [...'DDLURULDDRUULDRULD'].forEach(d=> move(d))
    // end utility functions
    
    
    // solve the top N-2 rows
    let x = 0, Z = N-2
    for (let r = 0; r < Z; r++) {
      for (let c = 0; c < Z; c++) {
        let J = j(r,c)
        x++ // x belonds in p[r][c]
        if (p[r][c] === x) { set.add(J); continue }
        if (!set.has(J)) { movx(x,r,c); set.add(J);}
      }
      x += 2
      movx(x,r,Z)
      
      movx(x-1,r+1,Z)
      set.add(j(r+1,Z))
      set.add(j(r,Z))
      mov0(r,N-1)
      
      set.delete(j(r,Z));     set.delete(j(r+1,Z))
      move('L');              move('D')
      set.add(j(r,N-1));      set.add(j(r,Z))
      
      if (p[r][Z] === x-1 && p[r+1][Z] === 0 && p[r+1][N-1] === x) {
          move('R')             
          move('U')
          yflip()
      }
    }
//     finish the last 2 rows starting from the left
    for (let c = 0; c < Z; c++) {
      let t = N*Z+c+1, b = N*(N-1)+c+1
      if (p[Z][c] === t && p[N-1][c] === b) {
        set.add(j(Z,c)); set.add(j(N-1,c))
        continue
      }
      movx(t,N-1,c)
      // case 1
      if (p[Z][c] === 0 && p[Z][c+1] === b) {
        move('R');  move('D')
        xflip()
        set.add(j(Z,c));  set.add(j(N-1,c))
      }
      // case 2
      else if (p[Z][c] === b) {
        mov0(N-1,c+1)
        xflip()
        set.add(j(Z,c)); set.add(j(N-1,c));
      }
      else {
        set.add(j(N-1,c));
        movx(b,N-1,c+1)
        set.add(j(N-1,c+1))
        mov0(Z,c)
        set.delete(j(N-1,c))
        set.delete(j(N-1,c+1))
        move('D'); move('R')
        set.add(j(Z,c))
        set.add(j(N-1,c))
      }
    }
    mov0(N-1,N-1)
    while (p[N-1][Z] !== N*N-1)
      [...'LURD'].forEach(d=>move(d))
    
    return p[Z][Z] > p[Z][N-1] ? null : result
}
