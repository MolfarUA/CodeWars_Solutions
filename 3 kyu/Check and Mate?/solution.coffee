# Returns an array of threats if the arrangement of 
# the pieces is a check, otherwise false
isCheck = (pieces, player, board, king, enemies) ->
  # reduces filtering and parsing if invoked by isMate
  if !board
    board = convertToBoard pieces
    king = findKing pieces, player
    enemies = findEnemies pieces, player
  
  # check to see if any of enemies threatens the king
  threats = []
  for enemy in enemies
    if threatens enemy, king.x, king.y, board
      threats.push enemy
  
  return if threats.length != 0 then threats else false

# Returns true if the arrangement of the
# pieces is a check mate, otherwise false
isMate = (pieces, player) ->
  board = convertToBoard pieces
  king = findKing pieces, player
  enemies = findEnemies pieces, player
  
  # can't be mate if it's not check
  threats = isCheck pieces, player, board, king, enemies
  if threats == false
    return false
  
  # check to see if there are any free tiles where the king can move
  x = king.x
  y = king.y
  if(isAvailableNonCheck(x-1, y-1, board, enemies, player) ||
     isAvailableNonCheck(x  , y-1, board, enemies, player) ||
     isAvailableNonCheck(x+1, y-1, board, enemies, player) ||
     isAvailableNonCheck(x-1, y  , board, enemies, player) ||
     isAvailableNonCheck(x+1, y  , board, enemies, player) ||
     isAvailableNonCheck(x-1, y+1, board, enemies, player) ||
     isAvailableNonCheck(x  , y+1, board, enemies, player) ||
     isAvailableNonCheck(x+1, y+1, board, enemies, player))
    return false
  
  p = 0
  if player == 0 then p = 1
  ownPieces = findEnemies pieces, p
  
  # check to see if there are any pieces that can capture
  # or intercept the threatening piece(s)
  for threat in threats
    path = getPathIndices threat, king.x, king.y
    
    for i in ownPieces
      for j in [0...path.length]
        # king can't block path to itself, only capture
        if j != path.length-1 && i == king
          continue
        # en passant is only available to pawns next to an enemy
        # pawn that just double-moved
        enPassant = threat.piece == "pawn" && i.piece == "pawn" && 
          threat.prevY && Math.abs(threat.prevY-threat.y) == 2
        
        # if j is the last point of the path, allow capturing, else allow moving
        # (only applies to pawns)
        moveOnly = j != path.length-1
        
        t = threatens i, path[j].x, path[j].y, board, moveOnly, enPassant
        if t
          # check to see if moving this piece would cause another check
          x = path[j].x
          y = path[j].y
          p = pieces
          
          # if en passant, remove the pawn and set the move coordinates correctly
          if t != true
            x = t.x
            y = t.y
            p = p.filter (o) -> o != threat
          
          return false unless moveCausesCheck p, i, x, y
  
  return true

# Returns isCheck() for pieces where mover has moved to x, y for mover's
# player, if x, y is occupied, the piece is captured in the process
moveCausesCheck = (pieces, mover, x, y) ->
  # eliminate piece at x, y from the list if exists
  t = pieces.filter (o) -> !(o.x == x && o.y == y)
  # replace the moving piece with a copy of it in the new
  # coordinates, we can use splice because filter copied
  # the array.
  t.splice t.indexOf(mover), 1, {piece: mover.piece, owner: mover.owner, x: x, y: y}
  
  return isCheck t, mover.owner

# Returns the coordinates of the tiles piece will take to arrive at x, y, including it's
# currenct position and the end position. This function assumes the piece moves in a way
# that allows it to reach point x, y.
getPathIndices = (piece, x, y) ->
  # knights move directly to the position
  if piece.piece == "knight"
    return [{x: piece.x, y: piece.y}]
  
  path = []
  
  dx = sign(piece.x-x);
  dy = sign(piece.y-y);
  while x != piece.x && y != piece.y
    x += dx
    y += dy
    path.push {x: x, y: y}
  
  return path

# Returns -1 for negative numbers, +1 for positive
# and 0 for 0
sign = (x) ->
  return if !x then x else if x < 0 then -1 else 1

# Returns true if point x, y is unoccupied or occupied by an opponent's piece and moving
# king to that position would not be a check, else false.
# Sanity-checks x and y for out of bounds coordinates.
isAvailableNonCheck = (x, y, board, enemies, player) ->
  # sanity check boundaries
  if x < 0 || x > 7 || y < 0 || y > 7 then return false
  # if tile is occupied by own piece
  if board[y][x] && board[y][x].owner == player then return false
  
  # iterate through enemies to see if any of them threaten x, y
  for enemy in enemies
    if threatens enemy, x, y, board
      return false
  return true

# Returns true if piece threatens point x, y, or new coordinates for a pawn if en passant move.
# A piece does NOT threaten the tile it is on. When moveOnly is set true, returns true for
# a pawn if it can move to the position mentioned, instead of attacking to it.
threatens = (piece, x, y, board, moveOnly, enPassant) ->
  if x == piece.x && y == piece.y then return false
  switch piece.piece
    when "rook"
      # can only move straight lines along columns or rows
      if piece.y == y
        a = 1 + Math.min piece.x, x
        b = Math.max piece.x, x
        return areClear board[y].slice(a, b)
      if piece.x == x
        a = 1 + Math.min piece.y, y
        b = Math.max piece.y, y
        tiles = []
        for i in [a...b]
          tiles.push board[i][x]
        return areClear tiles
      return false
    when "bishop"
      # can only move diagonal lines
      if Math.abs(piece.x-x) == Math.abs(piece.y-y)
        dx = sign piece.x-x
        dy = sign piece.y-y
        l = Math.abs(piece.x-x) - 1
        tiles = []
        for i in [0...l]
          x += dx
          y += dy
          tiles.push board[y][x]
        return areClear tiles
      return false
    when "queen"
      # moves like a rook and bishop combined
      return threatens({piece: "rook", x: piece.x, y: piece.y}, x, y, board) || 
             threatens({piece: "bishop", x: piece.x, y: piece.y}, x, y, board)
    when "king"
      # moves one tile to any direction
      return Math.abs(piece.x-x) < 2 && Math.abs(piece.y-y) < 2
    when "pawn"
      # attacks one tile diagonally towards enemy, moves 1
      # (or 2 from starting position) tiles towards enemy
      da = 1;
      if piece.owner == 0 then da = -1
      a = piece.y+da
      
      if moveOnly
        # pawns can move two tiles from their starting position
        if (piece.y == 6 && piece.owner == 0) || (piece.y == 1 && piece.owner == 1)
          return (y == a || y == a+da) && piece.x == x
        
        # non-starting position, only can move one tile
        return y == a && piece.x == x
      
      # en passant?
      if enPassant && y == a-da && Math.abs(piece.x-x) == 1
        return {x: x, y: a}
      return y == a && Math.abs(piece.x-x) == 1
    when "knight"
      # moves to any of the closest squares that are not on the same rank, 
      # file, or diagonal (= in an L shape), ignores pieces in between
             # two to left or right and one up or down
      return (Math.abs(piece.x-x) == 2 && Math.abs(piece.y-y) == 1) ||
             # one to left or right and two up or down
             (Math.abs(piece.x-x) == 1 && Math.abs(piece.y-y) == 2)

# Returns true if all members of array are null
areClear = (array) ->
  return array.every (o) -> o == null

# Filters pieces so that only pieces that are not owned by player are returned.
findEnemies = (pieces, player) ->
  return pieces.filter (o) -> o.owner != player

# Returns the piece representing the king of player.
findKing = (pieces, player) ->
  return pieces.filter(
    (o) -> o.piece == "king" && o.owner == player
  )[0]

# Returns an array representation of the board with all pieces in place.
# Empty tiles are null.
convertToBoard = (pieces) ->
  b = [
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null]
  ]
  for p in pieces
    b[p.y][p.x] = p;
  return b
