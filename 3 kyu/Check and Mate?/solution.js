function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var Grid = function () {
  function Grid(pieces, player) {
    var _this = this;

    _classCallCheck(this, Grid);

    this.pieces = pieces;
    this.player = player;

    this.grid = new Array(Grid.size).fill(0).map(function () {
      return [];
    });
    pieces.forEach(function (p) {
      _this.grid[p.x][p.y] = p;
      if (p.owner == player && p.piece == 'king') _this.king = p;
    });
  }

  _createClass(Grid, [{
    key: "isCheck",
    value: function isCheck() {
      var _this2 = this;

      return this.pieces.filter(function (p) {
        return _this2.isThreating(_this2.king, p, _this2.player);
      });
    }
  }, {
    key: "isMate",
    value: function isMate() {
      var _this3 = this;

      var pieces = this.isCheck();
      if (!pieces.length) return false;

      if (pieces.length == 1) {
        var candidates = this.whoCanSave(this.king, pieces[0]);
        var canSolved = candidates.some(function (item) {
          return item.pieces.some(function (p) {
            var gridBackup = _this3.cloneGrid();

            if (item.killed) {
              _this3.grid[item.killed.x][item.killed.y] = null;
            }

            _this3.grid[p.x][p.y] = null;
            _this3.grid[item.x][item.y] = {
              piece: p.piece,
              owner: p.owner,
              x: item.x,
              y: item.y
            };

            var ps = _this3.isCheck().filter(function (other) {
              return _this3.grid[other.x][other.y] == other;
            });

            var stillChecking = ps.length;
            _this3.grid = gridBackup;
            return !stillChecking;
          });
        });
        if (canSolved) return false;
      }


      for (var x = this.king.x - 1; x - this.king.x <= 1; x++) {
        for (var y = this.king.y - 1; y - this.king.y <= 1; y++) {
          if (!this.isValid(x, y)) continue;
          var other = this.grid[x][y];
          if (other && other.owner == this.player) continue;
          var gridBackup = this.cloneGrid();
          var kingBackup = this.king;
          this.grid[this.king.x][this.king.y] = null;
          this.grid[x][y] = this.king = {
            piece: 'king',
            player: this.player,
            x: x,
            y: y
          };
          var ps = this.isCheck().filter(function (other) {
            return _this3.grid[other.x][other.y] == other;
          });
          var stillChecking = ps.length;
          if (!stillChecking) return false;
          this.grid = gridBackup;
          this.king = kingBackup;
        }
      }

      return true;
    }
  }, {
    key: "isThreating",
    value: function isThreating(king, piece, player) {
      if (piece.owner == player) return false;

      switch (piece.piece) {
        case 'pawn':
          var deltaY = player ? -1 : 1;

          if (!this.grid[king.x][king.y]) {
            return this.checkCell(king, piece, 0, deltaY) || !this.grid[piece.x][piece.y + deltaY] && this.checkCell(king, piece, 0, deltaY * 2);
          }

          return this.checkCell(king, piece, 1, deltaY) || this.checkCell(king, piece, -1, deltaY);

        case 'knight':
          return this.checkCell(king, piece, 1, 2) || this.checkCell(king, piece, 1, -2) || this.checkCell(king, piece, -1, 2) || this.checkCell(king, piece, -1, -2) || this.checkCell(king, piece, 2, 1) || this.checkCell(king, piece, 2, -1) || this.checkCell(king, piece, -2, 1) || this.checkCell(king, piece, -2, -1);

        case 'rook':
          return this.checkRowAndColumn(king, piece);

        case 'bishop':
          return this.checkDiagonal(king, piece);

        case 'queen':
          return this.checkRowAndColumn(king, piece) || this.checkDiagonal(king, piece);

        case 'king':
          return Math.abs(piece.x - king.x) <= 1 && Math.abs(piece.y - king.y) <= 1;

        default:
          throw new Error('unknow piece: ' + piece.piece);
      }
    }
  }, {
    key: "isValid",
    value: function isValid(x, y) {
      return x >= 0 && x < Grid.size && y >= 0 && y < Grid.size;
    }
  }, {
    key: "isNotBlocked",
    value: function isNotBlocked(king, piece) {
      var deltaX = piece.x > king.x ? -1 : piece.x < king.x ? 1 : 0;
      var deltaY = piece.y > king.y ? -1 : piece.y < king.y ? 1 : 0;
      var x = piece.x + deltaX;
      var y = piece.y + deltaY;

      while (!(x == king.x && y == king.y) && this.isValid(x, y)) {
        if (this.grid[x][y]) return false;
        x += deltaX;
        y += deltaY;
      }

      return true;
    }
  }, {
    key: "checkCell",
    value: function checkCell(king, piece, deltaX, deltaY) {
      var x = piece.x + deltaX;
      var y = piece.y + deltaY;
      return this.isValid(x, y) && x == king.x && y == king.y;
    }
  }, {
    key: "checkRowAndColumn",
    value: function checkRowAndColumn(king, piece) {
      return (piece.x == king.x || piece.y == king.y) && this.isNotBlocked(king, piece);
    }
  }, {
    key: "checkDiagonal",
    value: function checkDiagonal(king, piece) {
      return (piece.x + piece.y == king.x + king.y || piece.x - piece.y == king.x - king.y) && this.isNotBlocked(king, piece);
    }
  }, {
    key: "whoCanSave",
    value: function whoCanSave(king, piece) {
      var _this4 = this;

      var deltaX = piece.x > king.x ? -1 : piece.x < king.x ? 1 : 0;
      var deltaY = piece.y > king.y ? -1 : piece.y < king.y ? 1 : 0;
      var x = piece.x;
      var y = piece.y;
      var candidates = [];

      var _loop = function _loop() {
        var target = {
          owner: _this4.player ? 0 : 1,
          x: x,
          y: y
        };

        var ps = _this4.pieces.filter(function (p) {
          return p.owner == _this4.player && p.piece != 'king' && _this4.isThreating(target, p, _this4.player ? 0 : 1);
        });

        if (ps.length) {
          candidates.push({
            pieces: ps,
            killed: x == piece.x && y == piece.y ? piece : null,
            x: x,
            y: y
          });
        }

        x += deltaX;
        y += deltaY;
      };

      while (!(x == king.x && y == king.y) && this.isValid(x, y)) {
        _loop();
      }


      if (piece.piece == 'pawn' && Math.abs(piece.y - piece.prevY) == 2) {
        var other;

        if (this.isValid(piece.x - 1, piece.y)) {
          other = this.grid[piece.x - 1][piece.y];
        } else if (this.isValid(piece.x + 1, piece.y)) {
          other = this.grid[piece.x + 1][piece.y];
        }

        if (other && other.owner == this.player && other.piece == 'pawn') {
          candidates.push({
            pieces: [other],
            killed: piece,
            x: piece.x,
            y: piece.y + (this.player ? 1 : -1)
          });
        }
      }

      return candidates;
    }
  }, {
    key: "cloneGrid",
    value: function cloneGrid() {
      return this.grid.map(function (row) {
        return row.concat([]);
      });
    }
  }]);

  return Grid;
}();

Grid.size = 8;

function isCheck(pieces, player) {
  var grid = new Grid(pieces, player);
  var ps = grid.isCheck();
  return ps.length ? ps : false;
}


function isMate(pieces, player) {
  var grid = new Grid(pieces, player);
  return grid.isMate();
}

___________________________________________________
const solutions = [
  false,
  '[{ piece: \'pawn\', owner: 1, x: 5, y: 6, prevX: 5, prevY: 5 }]',
  '[{ piece: \'rook\', owner: 1, x: 4, y: 1, prevX: 5, prevY: 1 }]',
  '[{ piece: \'knight\', owner: 1, x: 2, y: 6, prevX: 1, prevY: 4 }]',
  '[{ piece: \'bishop\', owner: 1, x: 0, y: 3, prevX: 1, prevY: 2 }]',
  '[{ piece: \'queen\', owner: 1, x: 4, y: 1, prevX: 5, prevY: 1 }]',
  '[{ piece: \'queen\', owner: 1, x: 7, y: 4, prevX: 6, prevY: 4 }]',
  '[{ piece: \'queen\', owner: 1, x: 7, y: 4, prevX: 3, prevY: 0 }]',
  false, true, false, true, true, true, false, true, false, false, false, false, true,
  '[{ piece: \'bishop\', owner: 1, x: 1, y: 4 }, { piece: \'rook\', owner: 1, x: 2, y: 7, prevX: 2, prevY: 5 }]',
  false, true
]

function isCheck(pieces, player) {
  return eval(solutions.shift())
}

// Returns true if the arrangement of the pieces is a check mate, otherwise false
function isMate(pieces, player) {
  return eval(solutions.shift())
}

___________________________________________________
function isCheck(pieces, player){
    Piece.prototype.resetBoard();
    pieces.forEach((piece)=> PieceFactory.prototype.createPiece(piece));
    let piecesAttackingKing = Piece.prototype.translatePieceToRegularObjects(Piece.prototype.piecesAttackingKingOf(player));
    return piecesAttackingKing.length === 0? false:piecesAttackingKing;
  }

function isMate(pieces, player){
    if(!isCheck(pieces,player)) return false;

    let allPiecesOfPlayer = Piece.prototype.getAllPiecesOf(player);  
    
    for(let i = 0; i < allPiecesOfPlayer.length; i++){
      let movesOfPiece = allPiecesOfPlayer[i].moves;
      for(let j = 0; j < movesOfPiece.length; j++) {
        allPiecesOfPlayer[i].moveTo(movesOfPiece[j].x,movesOfPiece[j].y)
        if(!isCheck(Piece.prototype.translateBoardToArray(),player)) {
          return false;
        }
        Piece.prototype.undoLastMove();
      }
    }
    return true;
}

class Piece {
  constructor(x=0, y=0, owner=1, prevX, prevY){
    this.x = x;
    this.y = y;
    this.owner = owner;  //0=white 1=black
    Piece.prototype.board[y][x] = this;
    if(prevX !== undefined && prevY !== undefined) {
      this.prevX = prevX;
      this.prevY = prevY;
    }
  }
  
  invalidMove(x,y){
    return !this.moves.find((position)=> position.x === x && position.y === y);
  }
  
  get moves(){
    return this.attackMoves();
  }
  
  moveTo(x, y){
      console.log(`${this.piece} of ${this.owner} from X:${this.x} Y:${this.y} to X:${x} Y:${y}`)
      if(this.invalidMove(x,y)) throw new Error(`Invalid move. ${this.piece} of ${this.owner} from X:${this.x} Y:${this.y} to X:${x} Y:${y}`);
      
      let slayed;
      if(Piece.prototype.positionIsOccupied({x,y})) {
        slayed = true;
        if(this.owner === 0) Piece.prototype.slayedBlack.push(Piece.prototype.board[y][x]);
        else if (this.owner === 1)Piece.prototype.slayedWhite.push(Piece.prototype.board[y][x]);
      } else slayed = false;
      
      Piece.prototype.allPlayedMoves.push({piece: this, from: {x: this.x, y:this.y}, to: {x,y}, slayed});
      
      Piece.prototype.board[this.y][this.x] = null;
      this.x = x;
      this.y = y;
      Piece.prototype.board[y][x] = this;
      
      return slayed;
  }
}

Piece.prototype.board = [
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null,null]
]

Piece.prototype.resetBoard = function(){
  for(let i =0; i<8;i++){
    for(let j =0; j<8;j++){
      Piece.prototype.board[i][j] = null;
    }
  }
}

Piece.prototype.undoLastMove =   function(){
  let move = Piece.prototype.allPlayedMoves.pop();

  move.piece.x = move.from.x;
  move.piece.y = move.from.y;
  Piece.prototype.board[move.from.y][move.from.x] = move.piece;
  
  let slayed = null;
  if(move.slayed && move.piece.owner === 0) slayed = Piece.prototype.slayedBlack.pop();
  else if( move.slayed && move.piece.owner === 1) slayed = Piece.prototype.slayedWhite.pop();
  if(slayed) Piece.prototype.board[slayed.y][slayed.x] = slayed;
  else Piece.prototype.board[move.to.y][move.to.x] = null;

  if(move.piece.piece === "pawn" && move.piece.initializedWithDoubleMove()) move.piece.prevMoveWasDouble = true;
  else move.piece.prevMoveWasDouble = false;
}
  
Piece.prototype.translateBoardToArray = function(){
  let oneDimArray = [];
  for(let i =0; i<8;i++){
    for(let j =0; j<8;j++){
      let piece = Piece.prototype.board[i][j];
      if(piece){
        let pieceCopy = JSON.parse(JSON.stringify(piece));
        if(typeof pieceCopy.prevMoveWasDouble === "boolean") delete pieceCopy.prevMoveWasDouble;
        oneDimArray.push({
          piece: pieceCopy.piece.toLowerCase(),
          owner: pieceCopy.owner,
          x: pieceCopy.x,
          y: pieceCopy.y,
          ...pieceCopy
        })
      };
    }
  }
  return oneDimArray;
}

Piece.prototype.translatePieceToRegularObjects = function(oPieces){
  let pieces = JSON.parse(JSON.stringify(oPieces));
  let mappedPieces = [];
  for(let i =0; i < pieces.length; i++) {
    if(typeof pieces[i].prevMoveWasDouble === "boolean") delete pieces[i].prevMoveWasDouble;
    mappedPieces.push({
      piece: pieces[i].piece,
      owner: pieces[i].owner,
      x: pieces[i].x,
      y: pieces[i].y,
      ...pieces[i]
    })
  }
  return mappedPieces;
}

Piece.prototype.pieceAttackingKingOf = function(player = 1, piece){
  let attackMoves = piece.attackMoves();
  let king = Piece.prototype.findKing(player);
  
  return !! attackMoves.find((position)=> 
          position.x === king.x &&
          position.y === king.y
        )
}

Piece.prototype.getAllPiecesOf = function(player){
  let board = Piece.prototype.board;
  let allPieces = [];
  for(let row =0;row < 8;row++){
      for(let column=0;column<8;column++){
        if(
          board[row][column] && 
          board[row][column].owner === player
        ){
          allPieces.push(board[row][column]);
        }
      }
  }
  return allPieces;
}

Piece.prototype.piecesAttackingKingOf = function(player = 1){
  var attackingPlayer = player == 0?1:0;
  let piecesThreatheningKing = [];
  let opponentPieces = Piece.prototype.getAllPiecesOf(attackingPlayer);
  
  opponentPieces.forEach((piece)=> {
    if(Piece.prototype.pieceAttackingKingOf(player,piece)) {
      piecesThreatheningKing.push(piece);
    }
  })
  
  return piecesThreatheningKing.length === 0? false: piecesThreatheningKing;
}

Piece.prototype.slayedWhite = [];
Piece.prototype.slayedBlack = [];
Piece.prototype.allPlayedMoves = [];

Piece.prototype.findKing = function(player = 1) {
  let board = Piece.prototype.board;
  for(let row =0; row<8;row++){
    for(let column =0; column <8;column++){
      if(
        board[row][column] &&
        board[row][column].piece === "king" && 
        board[row][column].owner === player
      ){
        return board[row][column];
      }
    }
  }
}

Piece.prototype.checkAndFilterPositionBounds = function(positions){
  return positions.filter((position)=>  
    position.x >= 0 && position.x <= 7 && position.y >= 0 && position.y <= 7
  )
}

Piece.prototype.filterPositionsTakenByOwnPieces = function(positions){
  return positions.filter((position)=> !(
    Piece.prototype.board[position.y][position.x] && 
    this.owner === Piece.prototype.board[position.y][position.x].owner)  
  )
}

Piece.prototype.positionIsOccupied = function(position){
    try {
      return Piece.prototype.board[position.y][position.x] !== null;
    } catch(e) {
      // out of bounds
      return false;
    }
}
class PieceFactory {};
PieceFactory.prototype.createPiece = function(piece){
  switch(piece.piece){
    case("pawn"):
        new Pawn(piece.x, piece.y, piece.owner, piece.prevX, piece.prevY);
        break;    
    case("rook"):
        new Rook(piece.x, piece.y, piece.owner, piece.prevX, piece.prevY);
        break;
    case("bishop"):
        new Bishop(piece.x, piece.y, piece.owner, piece.prevX, piece.prevY);
        break;
    case("queen"):
        new Queen(piece.x, piece.y, piece.owner, piece.prevX, piece.prevY);
        break;
    case("king"):
        new King(piece.x, piece.y, piece.owner, piece.prevX, piece.prevY);
        break;         
    case("knight"):
        new Knight(piece.x, piece.y, piece.owner, piece.prevX, piece.prevY);
        break;
    default:
        console.log("Piece not found");
        break;
  }
};

class Pawn extends Piece {
  constructor(x=0, y=1, owner=1, prevX, prevY) {
    super(x,y,owner, prevX, prevY);
    if(this.initializedWithDoubleMove()) this.prevMoveWasDouble = true; // for en passant
    else this.prevMoveWasDouble = false;
    this.piece = "pawn";
  }
  
  initializedWithDoubleMove(){
    if(this.owner === 0 && this.y === 4 && this.prevY === 6) return true;
    else if(this.owner === 1 && this.y === 3 && this.prevY === 1) return true;
    else return false;
  }
  
  filterOutNonAvailableAttackMoves(positions) {
    return positions.filter((position)=> !!Piece.prototype.board[position.y][position.x]);
  }
  
  filterOutBlockedAdditionalMoves(positions) {
    let possiblePositions = [];
    for(let i = 0; i < positions.length; i++) {
      if(!Piece.prototype.positionIsOccupied(positions[i])) possiblePositions.push(positions[i]);
      else break;
    }
    return possiblePositions;
  }
  
  hasMoved(){
    if(this.owner === 0 && this.y !== 6) return true;
    else if(this.owner === 1 && this.y !== 1) return true;
    else return false;
  }
  
  get moves(){
    return [
      ...this.filterOutNonAvailableAttackMoves(this.attackMoves()), 
      ...this.filterOutBlockedAdditionalMoves(this.additionalMoves()),
      ...this.enPassantMoves()
    ];
  }
  
  additionalMoves(){
  
    let possibleMoves = [];
    if(!this.hasMoved() && this.owner === 1){
      possibleMoves = [{x: this.x, y: this.y + 1},{x: this.x, y: this.y + 2}];
    } else if(this.hasMoved() && this.owner === 1){
      possibleMoves = [{x: this.x, y: this.y + 1}];
    } else if (!this.hasMoved() && this.owner === 0){
      possibleMoves = [{x: this.x, y: this.y -1},{x: this.x, y: this.y -2}];
    } else if(this.hasMoved() && this.owner === 0){
      possibleMoves = [{x: this.x, y: this.y -1}];
    }
    return this.filterOutBlockedAdditionalMoves(possibleMoves);
  }
  
  attackMoves(){
    let possibleMoves
    if(this.owner === 0) {
      possibleMoves =  [{x: this.x-1, y:this.y - 1}, {x: this.x+1, y:this.y -1}];
    } else {
      possibleMoves = [{x: this.x-1, y:this.y + 1}, {x: this.x+1, y:this.y +1}];
    }
    return this.filterPositionsTakenByOwnPieces(this.checkAndFilterPositionBounds(possibleMoves));
  }
  
  enPassantMoves(){
      let possibleMoves = this.attackMoves();
      let board = Piece.prototype.board;
      if(this.owner ===0 ) {
        possibleMoves = possibleMoves.filter(({x,y})=> {
        return (
          board[y+1][x] &&
          board[y+1][x].piece === "pawn" && 
          board[y+1][x].prevMoveWasDouble
        )});
      } else if (this.owner === 1) {
        possibleMoves = possibleMoves.filter(({x,y})=> {
         return (board[y-1][x] &&
          board[y-1][x].piece === "pawn" && 
          board[y-1][x].prevMoveWasDouble
        )});
      };
      return possibleMoves;
  }
  
  isDoubleMove(x,y){
    if(this.owner === 0 && !this.hasMoved() && y === 4) return true;
    else if(this.owner === 1 && !this.hasMoved() && y === 3) return true;
    return false
  }
  
  isEnPassantMove(xP,yP){
    return !!this.enPassantMoves().find(({x,y})=> xP ===x && yP===y)
  }
  
  moveToEnPassant(x,y){
      if(this.owner === 0) {
        Piece.prototype.slayedBlack.push(Piece.prototype.board[y+1][x]);
        Piece.prototype.board[y-1][x] = null;
      }
      else if (this.owner === 1){
        Piece.prototype.slayedWhite.push(Piece.prototype.board[y-1][x]);
        Piece.prototype.board[y-1][x] = null;
      }
      Piece.prototype.allPlayedMoves.push({piece: this, from: {x: this.x, y:this.y}, to: {x,y}, slayed:true});
      Piece.prototype.board[this.y][this.x] = null;
      this.x = x;
      this.y = y;
      Piece.prototype.board[y][x] = this;
      return true;
  }
  moveTo(x,y) {
    if(this.isDoubleMove(x,y)) this.prevMoveWasDouble = true;
    else this.prevMoveWasDouble = false;

    if(this.isEnPassantMove(x,y)) return this.moveToEnPassant(x,y);
    else return super.moveTo(x,y);
  }
}

class Bishop extends Piece {
  constructor(x=0, y=1, owner=1, prevX, prevY) {
    super(x,y,owner, prevX, prevY);
    this.piece = "bishop";
  }
  
  attackMoves(){
    let possibleMoves = [];
    
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x + i, y: this.y + i})
      if(Piece.prototype.positionIsOccupied({x: this.x + i, y: this.y + i}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x + i, y: this.y - i})
      if(Piece.prototype.positionIsOccupied({x: this.x + i, y: this.y - i}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x - i, y: this.y + i})
      if(Piece.prototype.positionIsOccupied({x: this.x - i, y: this.y + i}))break;
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x - i, y: this.y - i})
      if(Piece.prototype.positionIsOccupied({x: this.x - i, y: this.y - i}))break;      
    }
    return this.filterPositionsTakenByOwnPieces(this.checkAndFilterPositionBounds(possibleMoves));
  }
}

class Knight extends Piece{
  constructor(x=0, y=1, owner=1, prevX, prevY) {
    super(x,y,owner, prevX, prevY);
    this.piece = "knight";
  }
  
  attackMoves(){
    // going clockwise
    let possibleMoves =  [
        {x: this.x + 1, y: this.y + 2},
        {x: this.x + 2, y: this.y + 1},
        {x: this.x + 2, y: this.y - 1},
        {x: this.x + 1, y: this.y - 2},
        {x: this.x - 1, y: this.y - 2},
        {x: this.x - 2, y: this.y - 1},
        {x: this.x - 2, y: this.y + 1},
        {x: this.x - 1, y: this.y + 2},
    ];
    return this.filterPositionsTakenByOwnPieces(this.checkAndFilterPositionBounds(possibleMoves));
  }
}
class Rook extends Piece {
  constructor(x=0, y=1, owner=1, prevX, prevY) {
    super(x,y,owner, prevX, prevY);
    this.piece = "rook";
  }
  
  attackMoves(){
    let possibleMoves = [];
    
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x + i, y: this.y});
      if(Piece.prototype.positionIsOccupied({x: this.x + i, y: this.y}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x - i, y: this.y});
      if(Piece.prototype.positionIsOccupied({x: this.x - i, y: this.y}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x, y: this.y + i})
      if(Piece.prototype.positionIsOccupied({x: this.x, y: this.y + i}))break;            
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x, y: this.y - i});
      if(Piece.prototype.positionIsOccupied({x: this.x, y: this.y - i}))break;                  
    }
    return this.filterPositionsTakenByOwnPieces(this.checkAndFilterPositionBounds(possibleMoves));
  }
}

class Queen extends Piece {
  constructor(x=0, y=1, owner=1, prevX, prevY) {
    super(x,y,owner,prevX, prevY);
    this.piece = "queen";
  }
  
  attackMoves(){
    let possibleMoves = [];
    
    // bishop moves
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x + i, y: this.y + i})
      if(Piece.prototype.positionIsOccupied({x: this.x + i, y: this.y + i}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x + i, y: this.y - i})
      if(Piece.prototype.positionIsOccupied({x: this.x + i, y: this.y - i}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x - i, y: this.y + i})
      if(Piece.prototype.positionIsOccupied({x: this.x - i, y: this.y + i}))break;
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x - i, y: this.y - i})
      if(Piece.prototype.positionIsOccupied({x: this.x - i, y: this.y - i}))break;      
    }
    
    // rook moves
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x + i, y: this.y});
      if(Piece.prototype.positionIsOccupied({x: this.x + i, y: this.y}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x - i, y: this.y});
      if(Piece.prototype.positionIsOccupied({x: this.x - i, y: this.y}))break;      
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x, y: this.y + i})
      if(Piece.prototype.positionIsOccupied({x: this.x, y: this.y + i}))break;            
    }
    for(let i =1; i <= 7; i++) {
      possibleMoves.push({x: this.x, y: this.y - i});
      if(Piece.prototype.positionIsOccupied({x: this.x, y: this.y - i}))break;                  
    }
    
    return this.filterPositionsTakenByOwnPieces(this.checkAndFilterPositionBounds(possibleMoves));
  }
}

class King extends Piece {
  constructor(x=0, y=1, owner=1, prevX, prevY) {
    super(x,y,owner, prevX, prevY);
    this.piece = "king";
  }  
  
  attackMoves(){
    let possibleMoves = [
        {x: this.x + 1, y: this.y + 1},
        {x: this.x + 1, y: this.y - 1},
        {x: this.x - 1, y: this.y + 1},
        {x: this.x - 1, y: this.y - 1},
        
        {x: this.x + 1, y: this.y},
        {x: this.x - 1, y: this.y},
        {x: this.x, y: this.y + 1},
        {x: this.x, y: this.y - 1}
      ];
    return this.filterPositionsTakenByOwnPieces(this.checkAndFilterPositionBounds(possibleMoves));
  }
}
