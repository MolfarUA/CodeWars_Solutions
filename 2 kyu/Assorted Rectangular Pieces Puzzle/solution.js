function Point(x, y, rotated) {
    this.x = x;
    this.y = y;
    this.rotated = rotated;
    this.Adjacent = function (point) {
        if (this.y === point.y) {
            if (this.x === point.x - 1)
                return true;
            if (this.x === point.x + 1)
                return true;
        }

        if (this.x === point.x) {
            if (this.y === point.y - 1)
                return true;
            if (this.y === point.y + 1)
                return true;
        }

        return false;
    };
}

var setBits = [];
var widthSetBits = [];
var piecesIndex = [];

for (let i = 0; i < 24; i++) {
    setBits[i] = 1 << (23 - i);
    let bits = 0;
    for (let j = 0; j <= i; j++) {
        bits = bits << 1;
        bits |= 1;
    }
    widthSetBits[i + 1] = bits;
}

function GetBoardBits(board) {
    let boardBits = [];
    for (let i = 0; i < board.length; i++) {
        let bits = 0b111111111111111111111111;
        let bitsString = board[i];
        for (let j = 0; j < bitsString.length; j++) {
            if (bitsString[j] === '0')
                bits ^= 1 << (23 - j);
        }
        boardBits.push(bits);
        console.log(bits);
    }
    return boardBits;
}

var _boardBits, _width, _height, _pieceChosen, _pieceDirections, _piecePoint, _leftPieces, _pieces;

let pieceIndexByValue = [];

function solve_puzzle(board, pieces) {
    let maxTime;
    let res;

    maxTime = new Date().getTime() + 20000;
    res = _solve_puzzle(board, pieces, maxTime, 1);    
    return res;
}

function get1x1Positions(boardBits) {
    let empty = (x, y) => {
        if (x < 0)
            return false;
        if (y < 0)
            return false;
        if (x > _width - 1)
            return false;
        if (y > _height - 1)
            return false;

        return (boardBits[y] & setBits[x]) === 0;
    };

    let positions = [];

    for (let y = 0; y < _width; y++) {
        for (let x = 0; x < _width; x++) {
            if (empty(x, y) && !empty(x + 1, y) && !empty(x - 1, y) && !empty(x, y + 1) && !empty(x, y - 1))
                positions.push(new Point(x, y));
        }
    }
    return positions;
}

let count1x1 = 0;
let usedArea = 0;
let totalArea = 0;
let usedBoardIndexes = [];
let leftPiecesUniqueDimensions = [];
let leftPiecesDimensions = [];
let leftPiecesByDimensions = [];

function _solve_puzzle(board, pieces, maxTime, sort) {
    console.log(`board=${JSON.stringify(board)}`);
    console.log(`pieces=${JSON.stringify(pieces)}`);


    count1x1 = 0;
    usedArea = 0;
    totalArea = 0;
    usedBoardIndexes = [];

    usedBoardIndexes[500] = undefined;

    leftPiecesUniqueDimensions = [];

    let boardBits = GetBoardBits(board);


    let pieceChosen = [];
    let pieceDirections = [];
    let piecePoint = [];
    pieceIndexByValue = [];

    if (board.length < 4)
        return null;

    const width = board[0].length;
    const height = board.length;

    let startPoint = findNextEmptyPoint(new Point(0, 0), boardBits, width, height);

    let leftPieces = pieces.map((x, index) => index);

    leftPieces.sort((a, b) => {
        let area1 = pieces[a][0] * pieces[a][1];
        let area2 = pieces[b][0] * pieces[b][1];        

        let dim1 = area1 * 1000 + pieces[a][0] * 100 + pieces[a][1];
        let dim2 = area2 * 1000 + pieces[b][0] * 100 + pieces[b][1];        
        return (dim1 - dim2);
    });

    leftPiecesDimensions = [];
    leftPiecesByDimensions = [];
    leftPiecesUniqueDimensions = [];

    leftPieces.forEach((val, idx4) => {
        pieceIndexByValue[val] = idx4;
        totalArea += pieces[val][0] * pieces[val][1];
        leftPiecesUniqueDimensions[idx4] = pieces[val][0] * 100 + pieces[val][1];
    });

    _leftPieces = leftPieces;

    _width = width;
    _height = height;

    let start = new Date().getTime();
    generatePieceIndex(boardBits, pieces, width, height, sort);
    let stop = new Date().getTime();
    console.log(`index took:${stop - start}ms`);

    let pos1x1 = get1x1Positions(boardBits);
    console.log(`1x1 positions:${pos1x1.length}`);

    for (let pos1 of pos1x1) {
        let index = _leftPieces.findIndex((value, idx) => {
            return (pieces[value][0] === 1 && pieces[value][1] === 1);
        });
        let pieceIndex = _leftPieces[index];
        _leftPieces.splice(index, 1);
        leftPiecesUniqueDimensions.splice(index, 1);
        boardBits[pos1.y] |= setBits[pos1.x];
        console.log(`index:` + index);
        usedArea++;

        pieceChosen.push([pieceIndex, false, pos1]);
    }

    console.log(`totalArea:${totalArea} usedArea:${usedArea}`);

    count1x1 = _leftPieces.filter(x => pieces[x][0] === 1 && pieces[x][1] === 1).length;
    console.log(`left 1x1:${count1x1}`);

    let prevDimension = -1;
    let leftArea = 0;

    for (let i = 0; i < leftPieces.length; i++) {
        let dim = leftPiecesUniqueDimensions[i];
        if (prevDimension !== dim) {
            leftPiecesDimensions.push(leftPieces[i]);
            leftPiecesByDimensions.push([leftPieces[i]]);
        } else {
            leftPiecesByDimensions[leftPiecesByDimensions.length - 1].push(leftPieces[i]);
        }
        prevDimension = dim;
        leftArea += pieces[leftPieces[i]][0] * pieces[leftPieces[i]][1];
    }

    console.log(`left area:${leftArea}`);

    _boardBits = boardBits;

    _pieceChosen = pieceChosen;
    _pieceDirections = pieceDirections;
    _piecePoint = piecePoint;

    _pieces = pieces;

    let count = 0;
    for (let i = 0; i < pieces.length; i++) {
        count += piecesPoints[i].length;
    }
    console.log(`total positions:${count}`);
        
    bitsByDepth = pieces.map(x => _boardBits.map(y => y));
    let solution = findSolution(undefined, undefined, 0, maxTime, 0);
    stop = new Date().getTime();
    console.log(`solve took:${stop - start}ms`);

    if (solution === "timeout")
        return null;

    return transformSolution(solution, startPoint, GetBoardBits(board), width, height, pieces);
}

let piecesPoints = [];
let piecesBoardPoints = [];
let pieceMatrix = [];

let intersectingPieces = [];

function generatePieceIndex(boardBits, pieces, width, height, sort) {
    piecesIndex = [];
    piecesPoints = [];
    piecesBoardPoints = [];
    pieceMatrix = [];
    intersectingPieces = [];

    for (let y = 0; y < height; y++) {
        pieceMatrix[y] = [];
        for (let x = 0; x < width; x++) {
            let index = y * width + x;
            piecesIndex[index] = [];
            let pointNotRotated = new Point(x, y, false);
            let pointRotated = new Point(x, y, true);
            pieceMatrix[y][x] = [pointNotRotated, pointRotated];
            for (let i = 0; i < pieces.length; i++) {
                let piece = pieces[i];                

                if (!piecesPoints[i]) {
                    piecesPoints[i] = [];
                    piecesBoardPoints[i] = new Map();
                }

                let boardIndex = y * _width + x + 1;
                let boardIndexNotRotated = boardIndex * -1;
                let boardIndexRotated = boardIndex;

                let rotated = false;
                let p;
                let fitsNotRotated = pieceFitsWithChecks(p = new Point(x, y, rotated), boardBits, width, height, piece, rotated);

                if (fitsNotRotated) {                    
                    piecesPoints[i].push(p); 
                    piecesBoardPoints[i].set(boardIndexNotRotated, p); 
                }

                rotated = true;
                let fitsRotated = pieceFitsWithChecks(p = new Point(x, y, rotated), boardBits, width, height, piece, rotated);
                if (fitsRotated) {                    
                    piecesPoints[i].push(p);                     
                    piecesBoardPoints[i].set(boardIndexRotated, p);
                }
                piecesIndex[index][i] = [fitsNotRotated, fitsRotated];
            }
        }
    }

    indexedPieces = []; 
    indexByPiece = [];

    let center = (_height / 2 >> 0) * _width + (_width / 2 >> 0) + 1;

    for (let i = 0; i < pieces.length; i++) {
        if (sort === 4)
            piecesPoints[i].sort((a, b) => {
                return (intersectingPieces[i][b.boardIndex] || []).length - (intersectingPieces[i][a.boardIndex] || []).length;
            });
        else if (sort === 3)
            piecesPoints[i].sort((a, b) => (center - a.absBoardIndex) - (center - b.absBoardIndex));
        else if (sort === 2)
            piecesPoints[i].sort((a, b) => (intersectingPieces[i][a.boardIndex] || []).length - (intersectingPieces[i][b.boardIndex] || []).length);
        else if (sort)
            piecesPoints[i].sort((a, b) => Math.abs(a.boardIndex) - Math.abs(b.boardIndex));
        else
            piecesPoints[i].sort((a, b) => Math.abs(b.boardIndex) - Math.abs(a.boardIndex));
    }

    indexByPieceAndPrevBoardIndex = [];
    indexByPieceAnd2PrevBoardIndex = [];    
}

function transformSolution(solution, startPoint, boardBits, width, height, pieces) {
    let result = [];    
    for (let i = 0; i < _pieceChosen.length; i++) {
        let index = _pieceChosen[i][0];
        let rotated = _pieceChosen[i][1];
        let point = _pieceChosen[i][2];
        result[index] = [point.y, point.x, rotated ? 1 : 0];
        point = findNextEmptyPoint(point, boardBits, width, height);
    }
    console.log(`${JSON.stringify(result)}`);
    return result;
}


function findNextEmptyPoint(startPoint, boardBits, width, height) {
    for (let x = startPoint.x; x < width; x++) {
        let bit = setBits[x]; //1 << (23 - x);
        if ((boardBits[startPoint.y] & bit) === 0)
            return new Point(x, startPoint.y);
    }
    for (let y = startPoint.y + 1; y < height; y++) {
        for (let x = 0; x < width; x++) {
            //let bit = 1 << (23 - x);
            let bit = setBits[x];
            if ((boardBits[y] & bit) === 0)
                return new Point(x, y);
        }
    }
}

function findSolution(prevPoint, prevPrevPoint, depth, maxTime, startIndex) {
    if (_leftPieces.length % 10 === 0 && new Date().getTime() >= maxTime)
        return "timeout";

    let dim = leftPiecesDimensions[leftPiecesDimensions.length - 1];
    let equalPieces = leftPiecesByDimensions[leftPiecesByDimensions.length - 1];
    let possiblePlacementPositions = piecesPoints[dim];

    let usedPieceIndex = equalPieces[equalPieces.length - 1];
    let piece = _pieces[usedPieceIndex];
    _leftPieces.length--;
    equalPieces.length--;

    for (let i = startIndex; i < possiblePlacementPositions.length; i++) {
        let point = possiblePlacementPositions[i];
        let bits = point.bits;
        let rotated = point.rotated;
        if (pieceFits(point, _boardBits, _width, _height, piece, rotated, bits)) {
            possiblePlacementPositions.splice(i, 1);
            _pieceChosen.push([usedPieceIndex, rotated, point]);

            if (_leftPieces.length === 0) {
                console.log(`0`);
                return {};
            }

            for (let y = point.y; y < point.maxY; y++)
                _boardBits[y] ^= bits;

            usedArea += point.area;
            let nextStartIndex = i;
            if (equalPieces.length === 0) {
                leftPiecesDimensions.length--;
                leftPiecesByDimensions.length--;
                nextStartIndex = 0;
            }

            solution = findSolution(point, prevPoint, depth + 1, maxTime, nextStartIndex);
            if (solution)
                return solution;

            for (let y = point.y; y < point.maxY; y++)
                _boardBits[y] ^= bits;

            _pieceChosen.pop();

            usedArea -= point.area;
            possiblePlacementPositions.splice(i, 0, point);

            if (equalPieces.length === 0) {
                leftPiecesDimensions.push(dim);
                leftPiecesByDimensions.push(equalPieces);
            }

        }
    }

    equalPieces.push(usedPieceIndex);
    _leftPieces.push(usedPieceIndex);
}

function pieceFitsWithChecks(startPoint, boardBits, width, height, piece, rotated, bits) {
    let pieceWidth = !rotated ? piece[1] : piece[0];
    let pieceHeight = !rotated ? piece[0] : piece[1];

    if (startPoint.x + pieceWidth - 1 >= width) {
        return false;
    }

    if (bits === undefined)
        bits = widthSetBits[pieceWidth] << (24 - startPoint.x - pieceWidth);

    if (startPoint.y + pieceHeight > height)
        return false;

    for (let y = startPoint.y; y < startPoint.y + pieceHeight && y < height; y++) {
        let test = (boardBits[y] & bits);
        if (test !== 0)
            return false;
    }

    startPoint.bits = bits;
    startPoint.pieceWidth = pieceWidth;
    startPoint.pieceHeight = pieceHeight;
    startPoint.maxY = startPoint.y + pieceHeight;
    startPoint.area = pieceWidth * pieceHeight;

    let boardIndex = startPoint.y * _width + startPoint.x + 1;
    if (!rotated)
        boardIndex * -1;
    startPoint.boardIndex = boardIndex;
    startPoint.absBoardIndex = Math.abs(boardIndex);

    return true;
}


function pieceFits(startPoint, boardBits, width, height, piece, rotated, bits) {
    if ((boardBits[startPoint.y] & bits))
        return false;
    for (let y = startPoint.y + 1; y < startPoint.maxY; y++) {
        let test = boardBits[y] & bits;
        if (test !== 0)
            return false;
    }
    return true;
}

_____________________________________________________________
function solve_puzzle(board, pieces) {

  function compareNumeric(a, b) { //comparison by seniority
    for (let i = 0; i < 2; i++) {
      if (a[i] > b[i]) return 1
      if (a[i] == b[i]) {
        if (i == 1) return 0
        else continue
      }
      if (a[i] < b[i]) return -1
    }
  }

  let squareCompare = (a, b) => a[0] * a[1] - b[0] * b[1] //area comparison

  let pieces_ = pieces.slice(0).sort(compareNumeric),
    board_ = [], coords = [], vars = [], cloneCount = [], solution = []
  for (let i = 0; i < pieces_.length; i++) { //formation of arrays and removal of duplicates
    coords.push([])
    vars.push([])
    pieces_[i].push(1)
    while ((pieces_[i + 1] != undefined) &&
      (pieces_[i][0] == pieces_[i + 1][0]) &&
      (pieces_[i][1] == pieces_[i + 1][1])
    ) {
      pieces_.splice(i + 1, 1)
      pieces_[i][2]++
    }
  }
  pieces_.sort(squareCompare).reverse() //unique elements
  cloneCount = pieces_.map((e) => e.pop()) //number of copies

  board.forEach(e1 => { //formatted board copy
    board_.push([]); e1.split('').forEach(e2 => {
      board_[board_.length - 1].push(e2 == '0' ? e2 : '#')
    })
  })

  function check(e, m_pos, n_pos) { //checking an element for a coordinate
    let c0 = 0, c1 = 1
    do {
      if (!((m_pos + e[c0]) > board_.length || (n_pos + e[c1]) > board_[0].length)) {
        let c_err = 0
        outer: for (let i = m_pos; i < (m_pos + e[c0]); i++) {
          for (let j = n_pos; j < (n_pos + e[c1]); j++) {
            if (board_[i][j] !== '0') {
              c_err = 1
              break outer
            }
          }
        }
        if (c_err == 0)
          coords[pieces_.indexOf(e)].push([m_pos, n_pos, c0])
      }
      if (e[0] == e[1] || c0 == 1) return
      [c0, c1] = [c1, c0]
    }
    while (true)
  }

  for (let e of pieces_) { //bypassing a list of elements to obtain possible coordinates
    for (let i = 0; i < board_.length; i++) {
      for (let j = 0; j < board_[0].length; j++) {
        if (board_[i][j] === '0') {
          check(e, i, j)
        }
      }
    }
  }

  function squad(c) { //checking, inserting and retrieving an item on the board
    let crd = coords[i1][i2],
      p1 = crd[0] + pieces_[i1][0 ^ crd[2]],
      p2 = crd[1] + pieces_[i1][1 ^ crd[2]],
      j1 = crd[0], j2, v = ['0', ' '][c % 2]
    do {
      j2 = crd[1]
      do {
        if (c == 0) {
          if (board_[j1][j2] != v) {
            return
          }
        } else board_[j1][j2] = v
        j2++
      } while (j2 < p2)
      j1++
    } while (j1 < p1);
    if (c == 0) {
      vars[i1].push(i2)
      squad(1)
    } else if (c == 2) {
      return vars[i1].pop()
    }
    return
  }

  let i1 = 0, i2 = 0
  cond_1 = () =>
  (i2 + 2 > coords[i1].length && vars[i1].length < cloneCount[i1]) ||
    (coords[i1].length - i2 - 1 < cloneCount[i1] - vars[i1].length)
  cond_2 = () => (vars[i1][0] == undefined)
  cond_3 = () => (i2 < coords[i1].length && vars[i1].length < cloneCount[i1])
  cond_4 = () => (i1 < pieces_.length)
  do { //iteration over coordinates for all elements
    i2 = 0
    do {
      squad(0)
      while (cond_1()) {
        if (cond_2()) {
          i1--
        }
        i2 = vars[i1][vars[i1].length - 1]
        i2 = squad(2)
      }
      i2++
    } while (cond_3())
    i1++
  } while (cond_4())

  for (let e of pieces) { //collecting verified coordinates into a solution
    iy = pieces_.findIndex(a =>
      a.join() == e
    )
    ix = vars[iy].pop()
    solution.push(coords[iy][ix])
  }

  return solution
}
  
_____________________________________________________________
function solve_puzzle(board, pieces){
  let field = board.map(s => [...s]);
  let parts = [];
  let check = (i,j,h,w) => {
    for (let di=0; di<h; ++di) for(let dj=0; dj<w; ++dj) if ((field[i+di]||[])[j+dj] != '0') return false;
    return true;
  }
  let fill = (i,j,h,w,c) => {
    for (let di=0; di<h; ++di) for(let dj=0; dj<w; ++dj) field[i+di][j+dj] = c; 
  }
  for (const piece of pieces){
    let part;
    if (part = parts.find(p => p.h == piece[0] && p.w == piece[1])) part.count++;
    else {
      parts.push(part = {h:piece[0], w:piece[1], count:1, places:[], used: 0});
      for(let i=0;i<field.length;++i) for(let j=0;j<field[i].length;++j) if (field[i][j] == '0'){
        if (check(i,j,part.h,part.w)) part.places.push([i,j,0,part.h,part.w]);
        if(part.h != part.w && check(i,j,part.w,part.h)) part.places.push([i,j,1,part.w,part.h]);
      }
    }
  }
  parts.sort((p2,p1) => p1.h+p1.w+.01*p1.h*p1.w-p2.h-p2.w-.01*p2.h*p2.w);
  let result = [];
  let bruteforce = (k, prevP) => {
    if (k == parts.length) return true;
    parts[k].used++;
    for (let p=prevP+1; p<parts[k].places.length; ++p){ 
      let place = parts[k].places[p];
      if (check(place[0], place[1], place[3], place[4])){
        fill(place[0], place[1], place[3], place[4], k+1);
        result.push([k,p]);
        if (bruteforce(k+(parts[k].used == parts[k].count), (parts[k].used == parts[k].count ? -1: p))) return true;
        fill(place[0], place[1], place[3], place[4], '0');
        result.pop();
      }
    }
    parts[k].used--;
    return false;
  }
  bruteforce(0,-1);
  return pieces.map(([h,w]) => {
    let k = parts.findIndex(p => p.h == h && p.w == w);
    let resP = result.find(([resK,_]) => resK == k);
    resP[0] = -1;
    return parts[k].places[resP[1]].slice(0,3);
  });
}
  
_____________________________________________________________
function solve_puzzle(board, pieces) {
    var brd = board.map(r => r.split('').map(e => e === ' ' ? 1 : 0));
    var length = brd.length;
    var pcs = pieces.map((e, i) => [...e, i]).sort((a, b) => {
        if (b[0] * b[1] !== a[0] * a[1])
            return b[0] * b[1] - a[0] * a[1];
        let x1 = Math.max(a[0], a[1]),
            x2 = Math.max(b[0], b[1]);
        if (x1 !== x2)
            return x2 - x1;
        x1 = Math.min(a[0], a[1]);
        x2 = Math.min(b[0], b[1]);
        return x2 - x1;
    });
    var m = pcs.length;
    var H = [];
    for (var r = 0; r < length; r++)
        for (var c = 0; c < length; c++)
            if (brd[r][c] === 0) H.push([r, c]);
    var arr = [],
        res = [],
        tt = false;
    rec();
    res.sort((x, y) => x[3] - y[3]);
    return res.map(e => {
        e.pop();
        return e;
    });

    function rec(i = 0) {
        if (tt) return;
        if (i === m) {
            res = [...arr];
            tt = true;
            return;
        }
        if (!simpTestCount()) return;
        var [h, w, pos] = pcs[i];
        var PP = [];
        for (; i < m; i++) {
            if (pcs[i][0] === h && pcs[i][1] === w) PP.push([...pcs[i], 0]);
            else if (pcs[i][1] === h && pcs[i][0] === w) PP.push([...pcs[i], 1]);
            else break;
        }
        var HH = [];
        for (var [r, c] of H) {
            if (brd[r][c] === 1) {
                continue;
            }
            if (sett(r, c, h, w)) {
                HH.push([r, c, 0, ...count_neighb(r, c, h, w)]);
            }
            if (w !== h && sett(r, c, w, h)) {
                HH.push([r, c, 1, ...count_neighb(r, c, w, h)]);
            }
        }
        HH.sort((a, b) => {
            if (b[3] !== a[3]) return b[3] - a[3];
            else return b[4] - a[4];
        });
        if (PP.length > HH.length) return;
        var CC = [];
        if (h !== 1 || w !== 1) comb(PP.length, HH.length, CC);
        else CC = [Array.from(Array(PP.length).keys())];
        for (var com of CC) {
            let changed = [],
                test = false,
                tmp_res = [];
            for (var j = 0; j < PP.length; j++) {
                let [h, w, pos, oo] = PP[j]
                let [r, c, o, _, __] = HH[com[j]]
                if (o ^ oo === 0) {
                    if (!fill(r, c, h, w, changed)) {
                        test = true;
                        break;
                    } else {
                        tmp_res.push([r, c, 0, pos]);
                    }
                } else {
                    if (!fill(r, c, w, h, changed)) {
                        test = true;
                        break;
                    } else {
                        tmp_res.push([r, c, 1, pos]);
                    }
                }
            }
            if (test) {
                clear(changed);
                test = false, tmp_res = [];
                continue;
            }
            arr.push(...tmp_res);
            rec(i);
            clear(changed);
            arr = arr.slice(0, -tmp_res.length);
        }
    }

    function count_neighb(r, c, h, w) {
        var count_u = 0,
            count_r = 0,
            count_d = 0,
            count_l = 0;
        if (r === 0) {
            count_u += w > 1 ? w - 1 : 1;
        } else {
            for (var i = c; i < c + w; i++)
                if (brd[r - 1][i] === 1) count_u++;
        }
        if (r + h === length) {
            count_d += w > 1 ? w - 1 : 1;
        } else {
            for (var i = c; i < c + w; i++)
                if (brd[r + h][i] === 1) count_d++;
        }
        if (c === 0) {
            count_l += h > 1 ? h - 1 : 1;
        } else {
            for (var i = r; i < r + h; i++)
                if (brd[i][c - 1] === 1) count_l++;
        }
        if (c + w === length) {
            count_r += h > 1 ? h - 1 : 1;
        } else {
            for (var i = r; i < r + h; i++)
                if (brd[i][c + w] === 1) count_r++;
        }
        let mx_h = Math.max(count_l, count_r);
        let mx_w = Math.max(count_u, count_d);
        let mn_h = Math.min(count_l, count_r);
        let mn_w = Math.min(count_u, count_d);
        if (h > w) {
            return [mx_h + mx_w + mn_w, mn_h];
        }
        if (h < w) {
            return [mx_w + mx_h + mn_h, mn_w];
        }
        return [mx_h + mx_w, mn_h + mn_w];
    }

    function simpTestCount() {
        let sg_in_P = 0,
            sg_co = 0;
        for (var j = 0; j < m; j++)
            if (1 === pcs[j][0] && 1 === pcs[j][1]) sg_in_P++;
        for (var [r, c] of H) {
            if (brd[r][c] === 1) {
                continue;
            }
            if (isOnly(r, c)) sg_co++;
            if (sg_co > sg_in_P) {
                return false;
            }
        }
        return true;
    }

    function comb(l, n, c, j = 0, ar = []) {
        if ((ar.length > 0 && ar[0] > 1) || c.length > 1000) return;
        if (ar.length === l) {
            c.push([...ar]);
            return;
        }
        for (var i = j; i < n; i++) {
            ar.push(i);
            comb(l, n, c, i + 1, ar);
            ar.pop();
        }
    }

    function isOnly(r, c) {
        if (r - 1 >= 0 && brd[r - 1][c] === 0) return false;
        if (c - 1 >= 0 && brd[r][c - 1] === 0) return false;
        if (r + 1 < length && brd[r + 1][c] === 0) return false;
        if (c + 1 < length && brd[r][c + 1] === 0) return false;
        return true;
    }

    function sett(r, c, h, w) {
        if (r + h > length || c + w > length) return false;
        for (var i = r; i < r + h; i++)
            for (var j = c; j < c + w; j++)
                if (brd[i][j] === 1) {
                    return false;
                }
        return true;
    }

    function fill(r, c, h, w, ch) {
        for (var i = r; i < r + h; i++)
            for (var j = c; j < c + w; j++) {
                if (brd[i][j] === 1) return false;
                brd[i][j] = 1;
                ch.push([i, j]);
            }
        return true;
    }

    function clear(changed) {
        for (var [i, j] of changed) {
            brd[i][j] = 0;
        }
    }
}
