class Go {
  static get turns(){
    return [`black`, `white`]
  }
  
  static get stones(){
    return [`x`, `o`]
  }
  
  static get errors(){
    return {
      ibs: (h, w) => `Illegal Board Size ${h} by ${w}. Max is 25 by 25.`,
      im: (c) => `Illegal Move ${c}.`,
      ic: (c) => `Invalid Coordinates ${c}.`,
      ihspr: () => `Illegal Handicap Stones Placement Request.`,
      irr: () => `Illegal Rollback Request.`
    }
  }
  
  static parseCoordinates(c, board){
    const yx = c.split(/(?<=\d)(?=[A-HJ-Z])/)
    if(yx.length !== 2 || yx[1].length > 1) Go.throw(Go.errors.ic(c))
    const y = board.length - Number(yx[0])
    const x = yx[1].charCodeAt(0) - 65 - (yx[1].charCodeAt(0) < 73 ? 0 : 1)
    if(!board[y][x]) Go.throw(Go.errors.ic(c))
    return {y, x}
  }
  
  static copyBoardState(board){
    return JSON.parse(JSON.stringify(board))
  }
  
  static throw(m){
    throw new Error(m)
  }
  
  constructor(h, w){
    this.newGame(h, w)
  }
  
  get turn(){
    return Go.turns[Number(this.turnVal)]
  }
  
  get size(){
    return {height: this.h, width: this.w}
  }
  
  get stone(){
    return Go.stones[Number(this.turnVal)]
  }
  
  newGame(h, w = h){
    if(h > 25 || w > 25) Go.throw(Go.errors.ibs(h, w))
    this.h = h
    this.w = w
    this.board = new Array(h).fill(`.`).map(r => new Array(w).fill(`.`))
    this.turnVal = false
    this.moves = [Go.copyBoardState(this.board)]
    this.wereHcapsPlaced = false
  }
  
  move(...moves){
    moves.forEach(c => {
      const {y, x} = Go.parseCoordinates(c, this.board)
      if(this.board[y][x] !== `.`) Go.throw(Go.errors.im(c))
      this.board[y][x] = this.stone
      if(this.capture()){
        this.turnVal = !this.turnVal
        this.moves.push(Go.copyBoardState(this.board))
      }else{
        this.board = Go.copyBoardState(this.moves[this.moves.length - 1])
        Go.throw(Go.errors.im(c))
      }
    })
  }
  
  capture(){
    const groups = this.getAllGroupsOnBoard()
    groups.sort((a, b) => {
      const as = a.stone === this.stone ? 1 : 0
      const bs = b.stone === this.stone ? 1 : 0
      return as - bs
    })
    for(const g of groups){
      if(!this.calcLibs(g)){
        if(g.stone === this.stone) return false
        for(const p of g.points){
          const [y, x] = p.split(`,`).map(c => parseInt(c))
          this.board[y][x] = `.`
        }
      }
    }
    if(JSON.stringify(this.board) ===
        JSON.stringify(this.moves[this.moves.length - 2])) return false
    return true
  }
  
  getAllGroupsOnBoard(){
    const groups = []
    for(let y = 0; y < this.h; y++){
      rowLoop:
      for(let x = 0; x < this.w; x++){
        const stone = this.board[y][x]
        if(stone === `.`) continue rowLoop
        const point = `${y},${x}`
        for(const g of groups){
          if(g.points.has(point)) continue rowLoop
        }
        groups.push(this.getGroup(point, stone))
      }
    }
    return groups
  }
  
  getGroup(point, stone){
    const points = new Set([point])
    const ptsToChk = [point]
    while(ptsToChk.length){
      const [y, x] = ptsToChk[0].split(`,`).map(c => parseInt(c))
      const cp = this.getConnectedPoints(y, x)
      for(const p of cp){
        if(!this.board[p[0]]) continue
        const pt = `${p[0]},${p[1]}`
        if(this.board[p[0]][p[1]] === stone && !points.has(pt)){
          points.add(pt)
          ptsToChk.push(pt)
        }
      }
      ptsToChk.shift()
    }
    return {points, stone}
  }
  
  calcLibs(group){
    const libs = new Set([])
    for(const p of group.points){
      const cp = this.getConnectedPoints(...p.split(`,`).map(c => parseInt(c)))
      for(const pt of cp){
        if(!this.board[pt[0]]) continue
        if(this.board[pt[0]][pt[1]] === `.`){
          libs.add(`${pt[0]},${pt[1]}`)
        }
      }
    }
    return libs.size
  }
  
  handicapStones(n){
    const hcap = {
      '9': [[2, 6], [6, 2], [6, 6], [2, 2], [4, 4]],
      '13': [[3, 9], [9, 3], [9, 9], [3, 3], [6, 6], [6, 3], [6, 9], [3, 6], [9, 6]],
      '19': [[3, 15], [15, 3], [15, 15], [3, 3], [9, 9], [9, 3], [9, 15], [3, 9], [15, 9]]
    }
    if(this.h !== this.w
      || !hcap[`${this.h}`]
      || n > hcap[`${this.h}`].length
      || this.moves.length !== 1
      || this.wereHcapsPlaced) Go.throw(Go.errors.ihspr())
    for(let i = 0; i < n; i++){
      const p = hcap[`${this.h}`][i]
      this.board[p[0]][p[1]] = this.stone
    }
    this.wereHcapsPlaced = true
  }
  
  getConnectedPoints(y, x){
    return [[y - 1, x], [y + 1, x], [y, x - 1], [y, x + 1]]
  }
  
  getPosition(c){
    const {y, x} = Go.parseCoordinates(c, this.board)
    return this.board[y][x]
  }
  
  rollback(nt){
    if(nt < 1 || nt >= this.moves.length) Go.throw(Go.errors.irr())
    this.moves = this.moves.slice(0, this.moves.length - nt)
    this.board = Go.copyBoardState(this.moves[this.moves.length - 1])
    this.turnVal = this.moves.length % 2 === 0
  }
  
  pass(){
    this.turnVal = !this.turnVal
    this.moves.push(Go.copyBoardState(this.board))
  }
  
  reset(){
    this.newGame(this.h, this.w)
  }
}

____________________________________________________________
const WHITE = 'o';
const BLACK = 'x';

const VALID_HANDICAP_BOARDS = [
  { width: 9, height: 9 },
  { width: 13, height: 13 },
  { width: 19, height: 19 }
]

const HANDICAP_STONES_9X9 = [
  { x: 6, y: 2 },
  { x: 2, y: 6 },
  { x: 6, y: 6 },
  { x: 2, y: 2 },
  { x: 4, y: 4 }
]

const HANDICAP_STONES_13X13 = [
  { x: 9, y: 3 },
  { x: 3, y: 9 },
  { x: 9, y: 9 },
  { x: 3, y: 3 },
  { x: 6, y: 6 },
  { x: 3, y: 6 },
  { x: 9, y: 6 },
  { x: 6, y: 3 },
  { x: 6, y: 9 }
];

const HANDICAP_STONES_19X19 = [
  { x: 15, y: 3 },
  { x: 3, y: 15 },
  { x: 15, y: 15 },
  { x: 3, y: 3 },
  { x: 9, y: 9 },
  { x: 3, y: 9 },
  { x: 15, y: 9 },
  { x: 9, y: 3 },
  { x: 9, y: 15 }
];

class Go {
    
    constructor(size1, size2){
      if (size2){
        this._width = size2;
        this._height = size1;
      }
      else this._height = this._width = size1;
      this._ensureCorrectSizes();
      this._initGame();
    }
    
    move(...moves){
      for (const move of moves) this._executeMove(move);
    }
    
    getPosition(goCoordinates){
      const xyCoordinates = this._convertGoCoordinates(goCoordinates);
      const stone = this._getStone(xyCoordinates);
      return stone ? stone.color : '.';
    }
    
    handicapStones(numberOfStones){
      this._ensureHandicapStonesCanBePlaced();
      const handicapBoard = this._getHandicapBoard();
      if (numberOfStones > handicapBoard.length) throw new Error('Too many handicap stones');
      for (let i = 0; i < numberOfStones; i++){
        const position = handicapBoard[i];
        this._putStone(this._turnOfColor, position);
      }
    }
    
    rollback(numberOfTurns){
      this._rollbackTurns(numberOfTurns);
    }
    
    pass(){
      this._currentTurn ++;
      this._toggleTurnOfColor();
      this._saveTurn();
    }
    
    reset(){
      this._initGame();
    }
    
    get board(){
      return [...Array(this._height)]
        .map((_, y) => [...Array(this._width)]
          .map((_, x) => {
            const stone = this._getStone({x, y});
            return stone ? stone.color : '.';
          })
        );
    }
    
    get size(){
      return {
        width: this._width,
        height: this._height
      }
    }
    
    get turn(){
      return this._turnOfColor === BLACK ? 'black' : 'white'
    }
    
    _ensureCorrectSizes(){
      if (this._width > 25 || this._height > 25) throw new Error('Board too large');
    }
    
    _initGame(){
      this._turns = [];
      this._stones = [];
      this._turnOfColor = BLACK;
      this._currentTurn = 0;
      this._saveTurn();
    }
    
    _executeMove(goCoordinates){
      const xyCoordinates = this._convertGoCoordinates(goCoordinates);
      try {
        this._putStone(this._turnOfColor, xyCoordinates);
        this._removeOpponentGroupsWithoutLiberties();
        this._ensureNotSuicideMove();
        this._ensureNotKOMove();
        this._currentTurn ++;
        this._toggleTurnOfColor();
        this._saveTurn();
      }
      catch (e){
        this._rollbackTurn();
        throw e;
      }
    }

    _getStone({x, y}){
      return this._stones.find(s => s.x === x && s.y === y) || null;
    }
    
    _putStone(color, {x, y}){
      this._ensureSpaceWithoutStone({x, y});
      this._ensureCoordinatesInBounds({x, y});
      this._stones.push({color, x, y});
    }

    _removeStone(stone){
      const stoneIndex = this._stones.findIndex(s => s.x === stone.x && s.y === stone.y);
      if (stoneIndex === -1) throw new Error(`Attempting to remove not existing stone ${id}`);
      this._stones.splice(stoneIndex, 1);
    }

    _getAdjacentStones({x, y}){
      const adjacentCoordinates = this._getAdjacentCoordinates({x, y});
      const stones = [];
      for (const coordinates of adjacentCoordinates){
        const stone = this._getStone(coordinates);
        if (stone) stones.push(stone);
      }
      return stones;
    }

    _ensureSpaceWithoutStone({x, y}){
      if (this._getStone({x, y})) throw new Error('Stone already present');
    }

    _getStoneGroups(color){
      const stones = this._stones.filter(s => s.color === color);
      const groups = [];
      const isAlreadySeen = stone => groups.some(g => !!g.find(s => s.x === stone.x && s.y === stone.y));
      for (const stone of stones){
        if (isAlreadySeen(stone)) continue;
        groups.push(this._getStoneGroup(stone));
      }
      return groups;
    }

    _getStoneGroup(stone, alreadySeen){
      if (!alreadySeen) alreadySeen = [stone];
      const isAlreadySeen = stone => !!alreadySeen.find(s => s.x === stone.x && s.y === stone.y);
      const adjacentStones = this._getAdjacentStones({x: stone.x, y: stone.y})
        .filter(s => s.color === stone.color)
        .filter(s => !isAlreadySeen(s));
      alreadySeen.push(...adjacentStones);
      for (const adjacentStone of adjacentStones) this._getStoneGroup(adjacentStone, alreadySeen);
      return alreadySeen;  
    }

    _isStoneGroupWithoutLiberties(stones){
      return stones.every(s => 
        this._getAdjacentCoordinates({x: s.x, y: s.y}).every(c => this._getStone(c))
      );
    }
    
    _removeOpponentGroupsWithoutLiberties(){
      const opponentColor = this._turnOfColor === BLACK ? WHITE : BLACK;
      const opponentGroups = this._getStoneGroups(opponentColor);
      for (const group of opponentGroups){
        if (this._isStoneGroupWithoutLiberties(group)) group.forEach(s => this._removeStone(s))
      }
    }
    
    _ensureNotSuicideMove(){
      const alliesGroups = this._getStoneGroups(this._turnOfColor);
      for (const group of alliesGroups){
        if (this._isStoneGroupWithoutLiberties(group)) throw new Error('Suicide move')
      }
    }
    
    _ensureNotKOMove(){
      const previousTurnPlayer = this._turns.slice(-2)[0];
      if (previousTurnPlayer){
        const currentStones = JSON.stringify(this._stones);
        const previousStones = JSON.stringify(previousTurnPlayer.stones);
        if (currentStones === previousStones) throw new Error('KO');
      }
    }
    
    _saveTurn(){
      this._turns.push({
        number: this._currentTurn,
        stones: this._stones.slice(),
        turnOfColor: this._turnOfColor
      });
    }
    
    _rollbackTurn(){
      const { number, stones, turnOfColor } = this._turns[this._turns.length - 1];
      this._currentTurn = number;
      this._stones = stones.slice(0);
      this._turnOfColor = turnOfColor;
    }
    
    _rollbackTurns(numberOfTurns){
      const { number, stones, turnOfColor } = this._turns[this._turns.length - numberOfTurns - 1];
      this._turns.splice(this._turns.length - numberOfTurns, 300000);
      this._currentTurn = number;
      this._stones = stones.slice(0);
      this._turnOfColor = turnOfColor;
    }
    
    _toggleTurnOfColor(){
      this._turnOfColor = this._turnOfColor === BLACK ? WHITE : BLACK;
    }
    
    _getHandicapBoard(){
      const board = VALID_HANDICAP_BOARDS
        .find(x => x.width === this._width && x.height === this._height);
      if (!board) throw new Error('Board not valid for handicap');
      if (board.width === 9 && board.height === 9) return HANDICAP_STONES_9X9;
      if (board.width === 13 && board.height === 13) return HANDICAP_STONES_13X13;
      if (board.width === 19 && board.height === 19) return HANDICAP_STONES_19X19;
      throw new Error('Handicap board not configured');
    }
    
    _ensureHandicapStonesCanBePlaced(){
      if (this._stones.length > 0 || this._currentTurn > 0) {
        throw new Error('Can\'t place handicap stones, game already started');
      }
    }
    
    _convertGoCoordinates(coordinates){
      const numberChar = coordinates.match(/\d+/)[0];
      const letterChar = coordinates.match(/[A-Z]/)[0];
      const y = Math.abs(+numberChar - this._height);
      const x = this._getGoCoordinateLetters().indexOf(letterChar);
      return { x, y };
    }
    
    _getGoCoordinateLetters(){
      return 'ABCDEFGHJKLMNOPQRSTUVWXYZ'.split('');
    }
    
    _getAdjacentCoordinates({x, y}){
      const coordinates = [];
      if (x > 0) coordinates.push({ x: x - 1, y });
      if (x < this._width - 1) coordinates.push({ x: x + 1, y });
      if (y > 0) coordinates.push({ x, y: y - 1 });
      if (y < this._height - 1) coordinates.push({ x, y: y + 1 });
      return coordinates;
    }

    _ensureCoordinatesInBounds({x, y}){
      if (x < 0 || x > this._width) throw new Error('x coordinate out of bound');
      if (y < 0 || y > this._height) throw new Error('y coordinate out of bound');
    }

}

____________________________________________________________
class Go {
constructor(height, width = height) {
    if (height > 25) throw new Error("too big size");
    this.height = height;
    this.size = { height, width };
    this.board = [];
    this.initBoard(this.board);
    this.turn = "black";
    this.history = [JSON.parse(JSON.stringify(this.board))];
    this.hasBeenMoved = false;
    this.hIndices = {};
    this.alphabets = "ABCDEFGHJKLMNOPQRSTUVWXYZ";
    for (let i = 0; i < 25; i++) {
      this.hIndices[this.alphabets[i]] = i;
    }
  }

  initBoard(board, value = ".") {
    for (let row = 0; row < this.size.height; row++) {
      board.push([]);
      for (let col = 0; col < this.size.width; col++) {
        board[row].push(value);
      }
    }
  }

  getV(position) {
    return this.height - position.substring(0, position.length - 1);
  }

  getH(position) {
    return this.hIndices[position.substring(position.length - 1)];
  }

  getPosition(position) {
    return this.board[this.getV(position)][this.getH(position)];
  }

  pass() {
    this.turn = this.turn === "black" ? "white" : "black";
    this.addToHistory();
    this.hasBeenMoved = true;
  }

  capture(row, col) {
    this.board[row][col] = ".";
  }

  checkOpponent(row, col) {
    let result = false;
    const opponent = this.turn === "black" ? "o" : "x";
    if (this.board[row - 1] && this.board[row - 1][col] === opponent) {
      const res = this.checkLiberties(row - 1, col, opponent);
      if (res) result = true;
    }
    if (this.board[row] && this.board[row][col - 1] === opponent) {
      const res = this.checkLiberties(row, col - 1, opponent);
      if (res) result = true;
    }
    if (this.board[row + 1] && this.board[row + 1][col] === opponent) {
      const res = this.checkLiberties(row + 1, col, opponent);
      if (res) result = true;
    }
    if (this.board[row] && this.board[row][col + 1] === opponent) {
      const res = this.checkLiberties(row, col + 1, opponent);
      if (res) result = true;
    }
    return result;
  }

  checkLiberties(row, col, color) {
    const queue = [{ row, col }];
    const capturingStones = [{ row, col }];
    const visitBoard = [];
    this.initBoard(visitBoard, false);
    visitBoard[row][col] = true;

    const visit = (r, c) => {
      if (r < 0 || c < 0 || r >= this.height || c >= this.size.width) return;
      if (this.board[r][c] === ".") return true;
      if (this.board[r][c] === color && !visitBoard[r][c]) {
        visitBoard[r][c] = true;
        capturingStones.push({ row: r, col: c });
        queue.push({ row: r, col: c });
      }
      return;
    };

    while (queue.length > 0) {
      const current = queue.shift();
      if (visit(current.row + 1, current.col)) return;
      if (visit(current.row, current.col + 1)) return;
      if (visit(current.row - 1, current.col)) return;
      if (visit(current.row, current.col - 1)) return;
    }

    const opponent = this.turn === "black" ? "o" : "x";
    if (color === opponent) {
      for (let stone of capturingStones) {
        this.capture(stone.row, stone.col);
      }
    }
    return true;
  }

  place(position) {
    const myColor = this.turn === "black" ? "x" : "o";
    this.board[this.getV(position)][this.getH(position)] = myColor;
  }

  addToHistory() {
    this.history.push(JSON.parse(JSON.stringify(this.board)));
  }

  move(...positions) {
    for (let position of positions) {
      if (this.getPosition(position) !== ".") throw new Error("already placed");

      this.place(position);

      const result = this.checkOpponent(
        this.getV(position),
        this.getH(position)
      );
      if (!result) {
        const myColor = this.turn === "black" ? "x" : "o";
        const res = this.checkLiberties(
          this.getV(position),
          this.getH(position),
          myColor
        );
        if (res) {
          this.board[this.getV(position)][this.getH(position)] = ".";
          throw new Error("self capturing");
        }
      }
      if (this.history.length > 5) {
        const pastBoard = JSON.stringify(this.history[this.history.length - 2]);
        if (JSON.stringify(this.board) === pastBoard) {
          this.board = JSON.parse(
            JSON.stringify(this.history[this.history.length - 1])
          );
          throw new Error("KO rule");
        }
      }
      this.addToHistory();
      this.turn = this.turn === "black" ? "white" : "black";
      this.hasBeenMoved = true;
    }
  }

  rollback(num) {
    if (this.history.length < num + 1) throw new Error("too many rollbacks");
    for (let i = 0; i < num; i++) {
      this.history.pop();
      this.turn = this.turn === "black" ? "white" : "black";
    }
    this.board = JSON.parse(
      JSON.stringify(this.history[this.history.length - 1])
    );
  }

  reset() {
    this.board = [];
    this.initBoard(this.board);
    this.history = [JSON.parse(JSON.stringify(this.board))];
    this.turn = "black";
    this.hasBeenMoved = false;
  }

  handicapStones(num) {
    if (this.hasBeenMoved) throw new Error("already moved");
    const stones = {
      9: {
        1: "7G",
        2: "3C",
        3: "3G",
        4: "7C",
        5: "5E",
      },
      13: {
        1: "10K",
        2: "4D",
        3: "4K",
        4: "10D",
        5: "7G",
        6: "7D",
        7: "7K",
        8: "10G",
        9: "4G",
      },
      19: {
        1: "16Q",
        2: "4D",
        3: "4Q",
        4: "16D",
        5: "10K",
        6: "10D",
        7: "10Q",
        8: "16K",
        9: "4K",
      },
    };
    if (
      !stones[this.height] ||
      !stones[this.size.width] ||
      this.height !== this.size.width
    ) {
      throw new Error("invalid size for handicapStones");
    }
    for (let i = 1; i <= num; i++) {
      const position = stones[this.height][i];
      if (!position) throw new Error("no such handicap position");
      this.place(position);
    }
    this.addToHistory();
    this.hasBeenMoved = true;
  }
}

____________________________________________________________
const VERBOSE = 0, FULL = 0

function Go(height, width = height) {
    if(height > 25 || width > 25) throw new Error("Board cannot be larger than 25 by 25.")
    
    if(VERBOSE) console.log(`Creating board with height ${height} and ${width} width...`)
    const ALPHA = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
    const INFO = [{color: 'black', stone: 'x'}, {color: 'white', stone: 'o'}]
    const HANDICAP = {
        9: {indices: [[2,6],[6,2],[6,6],[2,2],[4,4]], count: 0, maxCount: 5},
        13: {indices: [[3,9],[9,3],[9,9],[3,3],[6,6],[6,3],[6,9],[3,6],[9,6]], count: 0, maxCount: 9},
        19: {indices: [[3,15],[15,3],[15,15],[3,3],[9,9],[9,3],[9,15],[3,9],[15,9]], count: 0, maxCount: 9}
    }
    const decode = enc => [height - enc.replace(/\D+/g, ''), ALPHA.indexOf(enc.replace(/\d/g, ''))]
    const inBounds = (x, y) => 0 <= x && x < height && 0 <= y && y < width

    let grid = Array.from({length: height}, () => Array(width).fill('.'))
    let player = 1
    const history = []
    const peers = Array.from({length: height}, (_, x) => Array.from({length: width}, (_, y) =>
        [[-1,0], [0,-1], [0,1], [1,0]].map(([i, j]) => inBounds(i += x, j += y) && [i, j]).filter(p => p)))
    
    const snap = () => history.push({snapshot: JSON.stringify(grid), player})

    function doTurn(enc) {
        snap()
        player ^= 1

        if(!enc) return

        let [x, y] = decode(enc)
        if(!inBounds(x, y)) throw new Error("Placing stone outside of bounds.")
        if(grid[x][y] != '.') throw new Error("Placing stone on stone.")

        let {stone} = INFO[player]
        let opponent = INFO[player ^ 1].stone

        grid[x][y] = stone

        const isClosed = (x, y, stone, opponent, closed) => {
            const group = new Set

            const recf = (x, y) => {
                if(closed) closed.add(x + ' ' + y)
                group.add(x + ' ' + y)
                return peers[x][y].some(([i, j]) => !group.has(i + ' ' + j) && (grid[i][j] == stone ? recf(i, j) : grid[i][j] != opponent))
            }
            
            return !recf(x, y) && group
        }

        const closed = new Set
        let capture = false

        grid.forEach((row, x) => row.forEach((cell, y) => {
            if(cell != opponent || closed.has(x + ' ' + y)) return
            let res = isClosed(x, y, opponent, stone, closed)
            if(!res) return
            capture = true
            res.forEach(s => {
                let [x, y] = s.split(' ')
                grid[x][y] = '.'
            })
        }))

        if(VERBOSE && FULL) console.log( `Moving ${stone} to ${enc}(${x}, ${y})\n${grid.map(row => row.join('')).join('\n')}` )

        if(!capture && isClosed(x, y, stone, opponent)) throw new Error("Self-capturing move.")
        
        if(JSON.stringify(grid) == (history[history.length - 2] || {}).snapshot) throw new Error("KO rule violation.")
    }

    return {
        get size() {
            return {height, width}
        },
        get board() {
            return grid
        },
        getPosition(enc) {
            if(VERBOSE) console.log(`Getting at position ${enc}...`)
            let [x, y] = decode(enc)
            return grid[x][y]
        },
        move(...encs) {
            if(VERBOSE) console.log(`Moving ${encs}...`)
            try {
                encs.forEach(doTurn)
            } catch(err) {
                this.rollback(1)
                throw err
            }
        },
        handicapStones(n) {
            if(VERBOSE) console.log(`Placing ${n} handicap stones...`)
            if(height != width || !HANDICAP[width]) throw new Error("Invalid board size for handicap stones.")
            if(HANDICAP[width].count + n > HANDICAP[width].maxCount) throw new Error("Too many handicap stones to place.")
            if(history.length) throw new Error("Placing handicap stones after first turn.")
            const {stone} = INFO[0]
            while(n--) {
                let i = HANDICAP[width].count++
                let [x, y] = HANDICAP[width].indices[i]
                grid[x][y] = stone
            }
        },
        rollback(n) {
            if(VERBOSE) console.log(`Rolling back ${n} times...`)
            if(!n) return
            if(n > history.length) throw new Error("Rollback too high.")
            while(--n) history.pop()
            let entry = history.pop()
            player = entry.player
            grid = JSON.parse(entry.snapshot)
        },
        get turn() {
            return INFO[player ^ 1].color
        },
        reset() {
            if(VERBOSE) console.log('Reseting...')
            for(let k in HANDICAP) HANDICAP[k].count = 0
            grid.forEach(row => row.forEach((_, y) => row[y] = '.'))
            history.length = 0
            player = 1
        },
        pass() {
            if(VERBOSE) console.log('Passing...')
            doTurn()
        }
    }
}
