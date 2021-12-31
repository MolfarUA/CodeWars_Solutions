type Side = 0 | 1;
type PieceName = 'king' | 'queen' | 'bishop' | 'knight' | 'rook' | 'pawn';
type Cord = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
type Piece = {piece: PieceName, owner: Side, x: Cord, y: Cord, prevX?: Cord, prevY?: Cord};

function move(piece: Piece, pieces: Array<Piece>, xd: number, yd: number, result: Array<Array<Piece>>): boolean {
  const x = piece.x + xd;
  const y = piece.y + yd;
  if (x < 0 || x > 7 || y < 0 || y > 7) return false;
  const capture = pieces.find(p => p.x === x && p.y === y);
  if (!capture || piece.owner !== capture.owner) {
    result.push([...pieces
                 .filter(p => (p.x !== x || p.y !== y) && (p.x !== piece.x || p.y !== piece.y))
                 .map(({prevX, prevY, ...p}) => p),
               {
                 ...piece,
                 x: x as Cord,
                 y: y as Cord,
                 prevX: piece.x,
                 prevY: piece.y
               } ]);
  }
  return !!capture;
}

function moveLine(piece: Piece, pieces: Array<Piece>, xd: number, yd: number, result: Array<Array<Piece>>): void {
  for (let i = 1; i < 8; i++) {
    if (move(piece, pieces, xd * i, yd * i, result)) return;
  }
}

function moves(pieces: Array<Piece>, player: Side): Array<Array<Piece>> {
  const result: Array<Array<Piece>> = [];
  pieces.filter(piece => piece.owner === player).forEach(piece => {
    switch (piece.piece) {
        case 'king':
          move(piece, pieces, -1, -1, result);
          move(piece, pieces, -1, 0, result);
          move(piece, pieces, -1, 1, result);
          move(piece, pieces, 0, -1, result);
          move(piece, pieces, 0, 1, result);
          move(piece, pieces, 1, -1, result);
          move(piece, pieces, 1, 0, result);
          move(piece, pieces, 1, 1, result);
          break;
        case 'queen':
          moveLine(piece, pieces, -1, -1, result);
          moveLine(piece, pieces, -1, 0, result);
          moveLine(piece, pieces, -1, 1, result);
          moveLine(piece, pieces, 0, -1, result);
          moveLine(piece, pieces, 0, 1, result);
          moveLine(piece, pieces, 1, -1, result);
          moveLine(piece, pieces, 1, 0, result);
          moveLine(piece, pieces, 1, 1, result);
          break;
        case 'bishop':
          moveLine(piece, pieces, -1, -1, result);
          moveLine(piece, pieces, -1, 1, result);
          moveLine(piece, pieces, 1, -1, result);
          moveLine(piece, pieces, 1, 1, result);
          break;
        case 'knight':
          move(piece, pieces, -1, -2, result);
          move(piece, pieces, -1, 2, result);
          move(piece, pieces, -2, -1, result);
          move(piece, pieces, -2, 1, result);
          move(piece, pieces, 1, -2, result);
          move(piece, pieces, 1, 2, result);
          move(piece, pieces, 2, -1, result);
          move(piece, pieces, 2, 1, result);
          break;
        case 'rook':
          moveLine(piece, pieces, -1, 0, result);
          moveLine(piece, pieces, 0, -1, result);
          moveLine(piece, pieces, 0, 1, result);
          moveLine(piece, pieces, 1, 0, result);
          break;
        case 'pawn':
          const direction = 2 * piece.owner - 1;
          const blocker = pieces.find(p => p.x === piece.x && p.y === piece.y + direction);
          if (!blocker) {
            move(piece, pieces, 0, direction, result);
            const homeRow = piece.owner === 1 ? 1 : 6;
            const secondBlocker = pieces.find(p => p.x === piece.x && p.y === piece.y + 2 * direction);
            if (piece.y === homeRow && !secondBlocker) {
              move(piece, pieces, 0, 2 * direction, result);
            }
          }
          const captures = pieces.filter(p => Math.abs(p.x - piece.x) === 1 && p.y === piece.y + direction);
          captures.forEach(capture => {
            move(piece, pieces, capture.x - piece.x, direction, result);
          });
          const enPassant = pieces.find(p => p.piece === 'pawn' && Math.abs(p.x - piece.x) === 1 && p.y === piece.y && p.prevY === piece.y + 2 * direction);
          if (enPassant) {
            result.push([...pieces
                         .filter(p => (p.x !== enPassant.x || p.y !== enPassant.y) && (p.x !== piece.x || p.y !== piece.y))
                         .map(({prevX, prevY, ...p}) => p),
               {
                 ...piece,
                 x: enPassant.x,
                 y: piece.y + direction as Cord,
                 prevX: piece.x,
                 prevY: piece.y
               } ]);
          }
          break;
    }
  });
  return result;
}

// Returns an array of threats if the arrangement of 
// the pieces is a check, otherwise false
export function isCheck(pieces: Array<Piece>, player: Side): Array<Piece> | false
{
  const king = pieces.find(piece => piece.piece === 'king' && piece.owner === player);
  if (!king) return false;
  const checks = moves(pieces, 1 - player as Side)
    .map(state => state.find(piece => piece.x === king.x && piece.y === king.y))
    .filter(piece => piece && piece.owner !== player)
    .map(piece => pieces.find(p => p.x === piece?.prevX && p.y === piece?.prevY));
  return checks.length > 0 ? checks as Piece[] : false;
}

// Returns true if the arrangement of the
// pieces is a check mate, otherwise false
export function isMate(pieces: Array<Piece>, player: Side): boolean
{
  const checking = isCheck(pieces, player);
  if (checking === false) return false;
  return moves(pieces, player).filter(state => isCheck(state, player) === false).length === 0;
}
  
___________________________________________________
type Side = 0 | 1;
type PieceName = 'king' | 'queen' | 'bishop' | 'knight' | 'rook' | 'pawn';
type Cord = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
type Piece = { piece: PieceName, owner: Side, x: Cord, y: Cord, prevX?: Cord, prevY?: Cord };
type Cell = { x: number, y: number };

function isFree(king: Piece, value: Piece, pieces: Array<Piece>) {
    if (king.x == value.x) return !pieces.filter(value1 => value1.x == king.x && ((value1.y - king.y) * (value1.y - value.y) < 0)).length;
    if (king.y == value.y) return !pieces.filter(value1 => value1.y == king.y && ((value1.x - king.x) * (value1.x - value.x) < 0)).length;
    if (Math.abs(king.x - value.x) == Math.abs(king.y - value.y)) return !(pieces.filter(value1 => (value1.x - king.x) / (value.x - king.x) == (value1.y - king.y) / (value.y - king.y)).length > 2);
    return true;
}

function getAttackPieces(value: Piece, king: Piece, pieces: Array<Piece>, player: Side, out: Piece[], isSim = false) {
    switch (value.piece) {
        case "king":
            if (Math.abs(king.x - value.x) <= 1 && Math.abs(king.y - value.y) <= 1) out.push(value);
            break;
        case "queen":
            if (((Math.abs(king.x - value.x) == Math.abs(king.y - value.y)) || ((king.x - value.x == 0) || (king.y - value.y == 0))) && isFree(king, value, pieces)) out.push(value);
            break;
        case "bishop":
            if ((Math.abs(king.x - value.x) == Math.abs(king.y - value.y)) && isFree(king, value, pieces)) out.push(value);
            break;
        case "knight":
            if (JSON.stringify([Math.abs(king.x - value.x), Math.abs(king.y - value.y)].sort()) == JSON.stringify([1, 2])) out.push(value);
            break;
        case "rook":
            if (((king.x - value.x == 0) || (king.y - value.y == 0)) && isFree(king, value, pieces)) out.push(value);
            break;
        case "pawn":
            if (isSim) {
                let sign = player == 0 ? 1 : -1;
                let available: number[] = [sign];
                if ((player == 1 && value.y == 6) || (player == 0 && value.y == 1)) available.push(2 * sign);
                if (king.x == value.x && (available.indexOf(king.y - value.y) > -1)) out.push(value);
            } else {
                if (Math.abs(king.x - value.x) == 1 && (king.y - value.y == (player == 0 ? 1 : -1) || (king.piece == "pawn" && king.y == value.y)))
                    out.push(value);
            }
            break;
    }
}

export function isCheck(pieces: Array<Piece>, player: Side): Array<Piece> | false {
    let out: Piece[] = [];
    let opPieces = pieces.filter(value => value.owner == (player == 0 ? 1 : 0));
    let king: Piece = pieces.filter(value => value.owner == player && value.piece == "king")[0];
    opPieces.forEach(value => getAttackPieces(value, king, pieces, player, out));
    return out.length ? out : false;
}

function getAttackPositions(pieces: Array<Piece>, last: Piece, player: Side, isSim = false) {
    let out: Piece[] = [];
    let opPieces = pieces.filter(value => value.owner != player);
    opPieces.forEach(value => getAttackPieces(value, last, pieces, player, out, isSim));
    return out.map(value => {
        let filter = pieces.filter(value1 => value1 != last && value1 != value);
        filter.push({piece: value.piece, owner: value.owner, x: last.x, y: last.y});
        return filter;
    });
}

function getCells(last: Piece, king: Piece) {
    let out: Piece[] = [];
    if (last.piece == "knight") return out;

    let xDiff = king.x - last.x;
    let yDiff = king.y - last.y;
    let xStep = xDiff ? (xDiff > 0 ? 1 : -1) : 0;
    let yStep = yDiff ? (yDiff > 0 ? 1 : -1) : 0;

    for (let i = 1; i < (Math.max(xDiff, yDiff)); i++) {
        out.push({ piece: "queen", owner: king.owner == 0 ? 1 : 0, x: convertPosition(last.x + i * xStep), y: convertPosition(last.y + i * yStep)});
    }
    return out;
}

export function isMate(pieces: Array<Piece>, player: Side): boolean {
    let check = isCheck(pieces, player);
    let next = nextPieces(pieces, player);
    if (!next.length) {
        if (check) {
            let last = pieces.filter(value => value.owner != player && value.prevX)[0];
            let pos: Piece[][] = getAttackPositions(pieces, last, player == 0 ? 1 : 0);
            for (const po of pos) {
                if (isCheck(po, player) == false)
                    return false;
            }
            let king = pieces.filter(value => value.owner == player && value.piece == "king")[0];
            let cells: Piece[] = getCells(last, king);
            let newPos: Piece[][] = cells.map(value => [...pieces, value]);

            for (const newPo of newPos) {
                let attackPos = getAttackPositions(newPo, newPo[newPo.length - 1], player == 0 ? 1 : 0, true);
                for (const attackPo of attackPos) {
                    if (isCheck(attackPo, player) == false)
                        return false;
                }
            }
        }
        return check != false;
    }
    for (const nextElement of next) {
        if (isCheck(nextElement, player) == false) return false;
    }
    return true;
}

function nextPieces(pieces: Array<Piece>, player: Side) {
    let king: Piece = pieces.filter(value => value.owner == player && value.piece == "king")[0];
    let notKing: Piece[] = pieces.filter(value => !(value.owner == player && value.piece == "king"));
    let coords: Cell[] = notKing.filter(value => value.owner == player).map(value => ({x: value.x, y: value.y}));
    let nextPositions: (Array<Piece>)[] = [];
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j < 1; j++) {
            if (i == 0 && j == 0) continue;
            let item: Cell = {x: king.x + i, y: king.y + j};
            if ([item.x, item.y].every(value => value >= 0 && value < 8) && !coords.find(value => value.x == item.x && value.y == item.y)) {
                let newPos = notKing.filter(value => value.x != item.x || value.y != item.y);
                newPos.push({piece: "king", owner: player, x: convertPosition(item.x), y: convertPosition(item.y)});
                if (!isCheck(newPos, player))
                    nextPositions.push(newPos);
            }
        }
    }
    return nextPositions;
}

function convertPosition(n: number): Cord {
    let cord: Cord;
    switch (n) {
        case 0: cord = 0; break;
        case 1: cord = 1; break;
        case 2: cord = 2; break;
        case 3: cord = 3; break;
        case 4: cord = 4; break;
        case 5: cord = 5; break;
        case 6: cord = 6; break;
        case 7: cord = 7; break;
        default: cord = 0;
    }
    return cord;
}
  
___________________________________________________
type Side = 0 | 1;
type PieceName = 'king' | 'queen' | 'bishop' | 'knight' | 'rook' | 'pawn';
type Cord = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
type Piece = {piece: PieceName, owner: Side, x: Cord, y: Cord, prevX?: Cord, prevY?: Cord};

type Direction = {x: -1 | 0 | 1, y: - 1 | 0 | 1};

/**
 * Where can a piece move?
 * Which pieces can a piece eat?
 * Which pieces can a piece threat (I think they are the same)
 * A first piece on one of it's way, is a piece threatened.
 * 
 * How to check if it's a check?
 * If some piece threatens the king, then it's a check.
 */
function dist1(a: Cord, b: Cord): number {
  return a > b ? a - b : b - a;
}

function sign(source: Cord, dist: Cord): (-1 | 0 | 1) {
  if (source > dist) {
    return -1;
  } else if (source < dist) {
    return 1;
  } else {
    return 0;
  }
}

type Cord2 = {x: Cord, y: Cord};

// Returns an array of threats if the arrangement of 
// the pieces is a check, otherwise false

function checkNoBetween(board: Map<string, Piece>, source: Cord2, dist: Cord2, direction: Direction): boolean {
  const init = Object.assign({}, source);
  
  init.x += direction.x;
  init.y += direction.y;
  while (init.x !== dist.x || init.y !== dist.y) {
    if (board.has(JSON.stringify({
      x: init.x,
      y: init.y
    }))) return false;
    init.x += direction.x;
    init.y += direction.y;
  }
  return true;
}

function getCordsBetweenIfReachable(board: Map<string, Piece>, attacker: Piece, attackee: Cord2): Array<Cord2> {
  const dist1x = dist1(attacker.x, attackee.x);
  const dist1y = dist1(attacker.y, attackee.y);
  const direcx = sign(attacker.x, attackee.x);
  const direcy = sign(attacker.y, attackee.y);
  const direction = {x: direcx, y: direcy};
  return getCordsBetweenIfReachableRaw(board, attacker, attackee, direction);
}

function getCordsBetweenIfReachableRaw(board: Map<string, Piece>, source: Cord2, dist: Cord2, direction: Direction): Array<Cord2> {
  const init = Object.assign({}, source);
  
  init.x += direction.x;
  init.y += direction.y;
  const res = [];
  while (init.x !== dist.x || init.y !== dist.y) {
    res.push(Object.assign({}, init));
    init.x += direction.x;
    init.y += direction.y;
  }
  return res;
}

function canThreat(board: Map<string, Piece>, attacker: Piece, attackee: Cord2): boolean {
  const dist1x = dist1(attacker.x, attackee.x);
  const dist1y = dist1(attacker.y, attackee.y);
  const direcx = sign(attacker.x, attackee.x);
  const direcy = sign(attacker.y, attackee.y);
  const direction = {x: direcx, y: direcy};
  switch (attacker.piece) {
    case 'king':
      if (dist1x <= 1 && dist1y <= 1) {
        return true
      } else {
        return false
      }
    case 'queen':
      if (dist1x === 0 || dist1y === 0 || dist1x === dist1y) { /** x is the column, so they are in the same column */
        /** check if there are pieces between them on this column */
        return checkNoBetween(board, attacker, attackee, direction);
      } else {
        return false;
      }
    case 'bishop':
      if (dist1x === dist1y) {
        return checkNoBetween(board, attacker, attackee, direction);
      } else {
        return false;
      }
    case 'rook':
      if (dist1x === 0 || dist1y === 0) {
        return checkNoBetween(board, attacker, attackee, direction);
      } else {
        return false;
      }
    case 'knight':
      if (dist1x === 1 && dist1y === 2) {
        return true;
      } else if (dist1x === 2 && dist1y === 1) {
        return true;
      } else {
        return false;
      }
    case 'pawn':
      /** ordinary eat, which moves to the position of the eaten piece. */
      /** en passant would be handled elsewhere. */
      if (dist1x === 1 && dist1y === 1) {
        if (attacker.owner === 0) {
          if (direcy === -1) {
            return true;
          } else {
            return false;
          }
        } else {
          if (direcy === 1) {
            return true;
          } else {
            return false;
          }
        }
      } else {
        return false;
      }
  }
}

function canMoveTo(board: Map<string, Piece>, attacker: Piece, attackee: Cord2): boolean {
  const dist1x = dist1(attacker.x, attackee.x);
  const dist1y = dist1(attacker.y, attackee.y);
  const direcx = sign(attacker.x, attackee.x);
  const direcy = sign(attacker.y, attackee.y);
  const direction = {x: direcx, y: direcy};
  if (board.has(JSON.stringify({x: attackee.x, y: attackee.y}))) return false; /** probably won't be needed, since we will not check the route if it's not feasible. */
  if (attacker.piece !== 'pawn') {
    return canThreat(board, attacker, attackee);
  } else {
    /** specially handle the pawn. */
    /** check if not moved. */
    let notMoved = false;
    if (attacker.owner === 0) /** is white */ {
      if (attacker.y === 6) notMoved = true;
    } else {
      if (attacker.y === 1) notMoved = true;
    }
    if (dist1x !== 0) return false;
    if (dist1y === 1) {
      if (attacker.owner === 0) /** is white */ {
        /** white can decrease the y cord by 1. */
        if (direcy === -1) {
          return true;
        }
      } else { /** black can increase the y cord. */
        if (direcy === 1) {
          return true;
        } 
      }
    }
    /** if not moved, also check for double move. */
    if (notMoved) {
      if (dist1y === 2) {
        if (attacker.owner === 0) /** is white */ {
          /** white can decrease the y cord by 1. */
          if (direcy === -1) {
            return true;
          }
        } else { /** black can increase the y cord. */
          if (direcy === 1) {
            return true;
          } 
        }
      }
    }
  }
  return false; 
}

function buildBoard(pieces: Array<Piece>): Map<string, Piece> {
  const res = new Map<string, Piece>();
  for (const piece of pieces) {
    res.set(JSON.stringify({
      x: piece.x,
      y: piece.y
    }), piece);
  }
  return res;
}

/**
 * 
 * @param {*} pieces 
 * @param {*} player 
 */
export function isCheck(pieces: Array<Piece>, player: Side)
{
  const board = buildBoard(pieces);
  const king = pieces.filter(e => e.owner === player && e.piece === 'king')[0];
  const res = [];
  for (const piece of pieces) {
    if (piece.owner !== player) {
      if (canThreat(board, piece, king)) {
        res.push(piece);
      }
    }
  }
  return res.length === 0 ? false : res;
}

function isValid(cord: Cord2) {
  return cord.x >=0 && cord.x < 8 && cord.y >= 0 && cord.y < 8;
}

// Returns true if the arrangement of the
// pieces is a check mate, otherwise false
export function isMate(pieces: Array<Piece>, player: Side)
{
  pieces = pieces.map(e => Object.assign({}, e));
  /** avoid modifying the original array. */
  const checks = isCheck(pieces, player);
  if (!checks) return false;
  const king = pieces.filter(e => e.owner === player && e.piece === 'king')[0];
  const kingIndex = pieces.filter(e => e.owner === player && e.piece === 'king')[0];
  const piecesToMove = pieces.filter(e => e.owner === player && e.piece !== 'king');
  const board = buildBoard(pieces);

  
  /** check all possible moves of the king */
  // for all 9 directions. check if valid. check if is a check.
  const moves: Array<Direction> = [
    {x: 1, y: 1},
    {x: 1, y: 0},
    {x: 1, y: -1},
    {x: -1, y: 1},
    {x: -1, y: 0},
    {x: -1, y: -1},
    {x: 0, y: 1},
    {x: 0, y: -1},
  ]
  for (const move of moves) {
    king.x += move.x;
    king.y += move.y;
    if (isValid(king)) {
      const empty = !board.has(JSON.stringify({
        x: king.x,
        y: king.y
      }));
      const canCapture = !empty && board.get(JSON.stringify({
        x: king.x,
        y: king.y
      }))!.owner !== player;
      if (empty && !isCheck(pieces, player)) {
        return false;
      } else if (canCapture && !isCheck(pieces.filter(e => e.x !== king.x || e.y !== king.y || e.owner === king.owner), player)) { /** This does not change pieces, so no need to restore. */
        return false;
      }
    }
    /** remember to restore the state of the king. */
    king.x -= move.x;
    king.y -= move.y;
  }

  /** check all the attackers, and see if they can be hampered. */
  for (const attacker of checks) {
    /** check if can intercept */
    let spacesInBetween: Cord2[];
    if (attacker.piece === 'queen' || attacker.piece === 'bishop' || attacker.piece === 'rook') {
      spacesInBetween = getCordsBetweenIfReachable(board, attacker, king);
    } else {
      spacesInBetween = [];
    }
    const originalAttacker = Object.assign({}, attacker);
    
    const attackerRemovedPieces = pieces.filter(e => e.x !== attacker.x || e.y !== attacker.y || e.piece !== attacker.piece || e.owner !== attacker.owner);
    for (const pieceCanMove of piecesToMove) {
      const originalPieceCanMove = Object.assign({}, pieceCanMove);
      /** if it can threaten the space in between, try capturing it */
      if (canThreat(board, pieceCanMove, attacker)) {
        pieceCanMove.x = attacker.x;
        pieceCanMove.y = attacker.y;
        if (!isCheck(attackerRemovedPieces, player)) return false;
        pieceCanMove.x = originalPieceCanMove.x;
        pieceCanMove.y = originalPieceCanMove.y;
      }
      /** check for en passant */
      if (attacker.piece === 'pawn' && pieceCanMove.piece === 'pawn') {
        /** only possible with a previous move and the move is by 2 */
        if (attacker.prevX && Math.abs(attacker!.prevY! - attacker!.y!) === 2) {
          /** only if they are right next to each other */
          if (attacker.y === pieceCanMove.y && Math.abs(attacker.x - pieceCanMove.x) === 1) {
            let oldCord = {x: attacker.x, y: attacker.y};
            if (attacker.owner === 0) { /** white move by decreasing, so old should be retrieved by increasing. */
              oldCord.y += 1;
            } else {
              oldCord.y -= 1;
            }
            /** only possible when not captured. */
            (<any>pieceCanMove.x) = oldCord.x;
            (<any>pieceCanMove.y) = oldCord.y;
            if (!board.has(JSON.stringify(oldCord))) {
              if (!isCheck(attackerRemovedPieces, player)) return false;
            }
            pieceCanMove.x = originalPieceCanMove.x;
            pieceCanMove.y = originalPieceCanMove.y;
          }
        }
      }
      /** if it can threaten the piece, try taking it. */
      /**
       * King is unstoppable.
       * Queen can be intercepted.
       * Bishop can be intercepted.
       * Knight cannot be intercepted.
       * Rook can be intercepted.
       * Pawn cannot be intercepted.
       */
      for (const spaceInBetween of spacesInBetween) {
        if (canMoveTo(board, pieceCanMove, spaceInBetween)) {
          /** check if it's a check */
        pieceCanMove.x = spaceInBetween.x;
        pieceCanMove.y = spaceInBetween.y;
        if (!isCheck(pieces, player)) return false;
        pieceCanMove.x = originalPieceCanMove.x;
        pieceCanMove.y = originalPieceCanMove.y;
        } /** else cannot do anything. */
      }
    }
  }

  return true; // no effective move.
}
