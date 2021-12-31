const BLACK_PIECE = 1; // start on top
const WHITE_PIECE = 0; // start on bottom
function findPieceFunc(callable $func, array $pieces)
{
    foreach ($pieces as $piece) {
        if (call_user_func($func, $piece)) {
            return $piece;
        }
    }
    return false;
}
function findPieceAttr(array $pieceAttributes, array $pieces)
{
    foreach ($pieces as $piece) {
        $valid = true;
        foreach ($pieceAttributes as $attr => $value) {
            if ($piece[$attr] !== $value) {
                $valid = false;
                break;
            }
        }
        if ($valid) {
            return $piece;
        }
    }
    return false;
}


function removePieces(array $pieces, array $piecesToRemove): array
{
    $result = [];
    foreach ($pieces as $piece) {
        if (!in_array($piece, $piecesToRemove)) {
            $result[] = $piece;
        }
    }
    return $result;
}function canAttack(array $pieceAttack, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
  if ($pieceAttack['owner'] === $pieceDefence['owner']) {
  return false;
    }
  switch ($pieceAttack['piece']) {
   case 'pawn':
  return pawnCanAttack($pieceAttack, $pieceDefence, $otherPieces, $newPieces);
  case 'rook':
            return rookCanAttack($pieceAttack, $pieceDefence, $otherPieces, $newPieces);
        case 'knight':
            return knightCanAttack($pieceAttack, $pieceDefence, $otherPieces, $newPieces);
        case 'bishop':
            return bishopCanAttack($pieceAttack, $pieceDefence, $otherPieces, $newPieces);
        case 'queen':
            return queenCanAttack($pieceAttack, $pieceDefence, $otherPieces, $newPieces);
        case 'king':
            return kingCanAttack($pieceAttack, $pieceDefence, $otherPieces, $newPieces);
    }
    throw new Exception(sprintf('Invalid piece: %s', $pieceAttack['piece']));
}

/**
 * @param array $piece
 * @param array $position
 * @return array
 */
function at(array $piece, array $position)
{
    $newPiece = $piece;
    $newPiece['x'] = $position['x'];
    $newPiece['y'] = $position['y'];
    return $newPiece;
}
function pawnCanAttack(array $pawn, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
    $attackDirection = $pawn['owner'] === BLACK_PIECE ? +1 : -1;

    if ($pieceDefence['piece'] === 'pawn' && isset($pieceDefence['prevY']) &&
        abs($pieceDefence['y'] - $pieceDefence['prevY']) === 2) {
        $passantDirection = $pieceDefence['owner'] === BLACK_PIECE ? +1 : -1;
        $passantY = $pieceDefence['prevY'] + $passantDirection;
        $passantX = $pieceDefence['prevX'];
        $canAttack = ($passantY === $pawn['y'] + $attackDirection) &&
            abs($passantX - $pawn['x']) === 1;
        if ($canAttack) {
            $newPieces = array_merge($otherPieces, [at($pawn, ['x' => $passantX, 'y' => $passantY])]);
            return true;
        }
    }

    $canAttack = ($pieceDefence['y'] === $pawn['y'] + $attackDirection) &&
        abs($pieceDefence['x'] - $pawn['x']) === 1;

    if ($canAttack) {
        $newPieces = array_merge($otherPieces, [at($pawn, $pieceDefence)]);
    }
    return $canAttack;
}


function kingCanAttack(array $king, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
    $canAttack = abs($pieceDefence['x'] - $king['x']) <= 1
        && abs($pieceDefence['y'] - $king['y']) <= 1;
    if ($canAttack) {
        $newPieces = array_merge($otherPieces, [at($king, $pieceDefence)]);
    }
    return $canAttack;
}


function rookCanAttack(array $rook, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
    $sameColumnBetweenLines = function (array $p) use ($rook, $pieceDefence): bool {
        $minY = min($rook['y'], $pieceDefence['y']);
        $maxY = max($rook['y'], $pieceDefence['y']);
        return $p['x'] === $rook['x'] && $p['y'] > $minY && $p['y'] < $maxY;
    };
    $sameLineBetweenColumns = function (array $p) use ($rook, $pieceDefence): bool {
        $minX = min($rook['x'], $pieceDefence['x']);
        $maxX = max($rook['x'], $pieceDefence['x']);
        return $p['y'] === $rook['y'] && $p['x'] > $minX && $p['x'] < $maxX;
    };

    $canAttack = ($rook['x'] === $pieceDefence['x'] && !findPieceFunc($sameColumnBetweenLines, $otherPieces))
        || ($rook['y'] === $pieceDefence['y'] && !findPieceFunc($sameLineBetweenColumns, $otherPieces));
    if ($canAttack) {
        $newPieces = array_merge($otherPieces, [at($rook, $pieceDefence)]);
    }
    return $canAttack;
}


function knightCanAttack(array $knight, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
    $xDist = abs($knight['x'] - $pieceDefence['x']);
    $yDist = abs($knight['y'] - $pieceDefence['y']);
    $canAttack = min($xDist, $yDist) === 1 && max($xDist, $yDist) === 2;
    if ($canAttack) {
        $newPieces = array_merge($otherPieces, [at($knight, $pieceDefence)]);
    }
    return $canAttack;
}
function inDiagonal(array $piece1, array $piece2): bool
{
    return abs($piece1['x'] - $piece2['x']) === abs($piece1['y'] - $piece2['y']);
}

function bishopCanAttack(array $bishop, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
    $betweenPieces = function (array $p) use ($bishop, $pieceDefence): bool {
        $minX = min($bishop['x'], $pieceDefence['x']);
        $maxX = max($bishop['x'], $pieceDefence['x']);
        $minY = min($bishop['y'], $pieceDefence['y']);
        $maxY = max($bishop['y'], $pieceDefence['y']);
        return inDiagonal($p, $bishop)
            && inDiagonal($p, $pieceDefence)
            && $p['x'] > $minX && $p['x'] < $maxX
            && $p['y'] > $minY && $p['y'] < $maxY;
    };
    $canAttack = inDiagonal($bishop, $pieceDefence) && !findPieceFunc($betweenPieces, $otherPieces);
    if ($canAttack) {
        $newPieces = array_merge($otherPieces, [at($bishop, $pieceDefence)]);
    }
    return $canAttack;
}


function queenCanAttack(array $queen, array $pieceDefence, array $otherPieces, array &$newPieces): bool
{
    return rookCanAttack($queen, $pieceDefence, $otherPieces, $newPieces)
        || bishopCanAttack($queen, $pieceDefence, $otherPieces, $newPieces);
}


function canMove(array $piece, array $position, array $otherPieces): bool
{
    if ($piece['piece'] === 'pawn') {
        if (findPieceAttr($position, $otherPieces)) {
            return false;
        }
        $attackDirection = $pawn['owner'] === BLACK_PIECE ? +1 : -1;
        if ($piece['x'] === $position['x']) {
            return $piece['y'] + $attackDirection === $position['y']
                || ($piece['y'] + 2 * $attackDiraction === $position['y'] &&
                    !findPieceAttr(['x' => $position['x'], 'y' => $piece['y'] + $attackDirection], $otherPieces));
        }
    }

    $fakeOponent = array_merge(
        $position,
        ['owner' => 1 - $piece['owner']]
    );

    $newPieces = [];
    return canAttack($piece, $fakeOponent, $otherPieces, $newPieces);
}


function isCheck(array $pieces, int $player)
{
    $king = findPieceAttr(['piece' => 'king', 'owner' => $player], $pieces);

    $result = [];
    foreach ($pieces as $piece) {
        $otherPieces = removePieces($pieces, [$king, $piece]);
        $newPieces = [];
        if (canAttack($piece, $king, $otherPieces, $newPieces)) {
            $result[] = $piece;
        }
    }

    return empty($result) ? false: $result;
}


function validPosition(array $piece): bool
{
    return $piece['x'] >= 0 && $piece['x'] <= 7 && $piece['y'] >= 0 && $piece['y'] <= 7;
}

function kingCanMove(array $king, array $pieces): bool
{
    for ($x = -1; $x <= 1; $x++) {
        for ($y = -1; $y <= 1; $y++) {
            if ($x === 0 && $y === 0) {
                continue;
            }

            $newKing = $king;
            $newKing['x'] += $x;
            $newKing['y'] += $y;

            if (!validPosition($newKing)) {
                continue;
            }

            $newPieces = removePieces($pieces, [$king]);

            $samePosition = [
                'x' => $newKing['x'],
                'y' => $newKing['y'],
            ];
            $pieceSamePosition = findPieceAttr($samePosition, $newPieces);

            if ($pieceSamePosition) {
                if ($pieceSamePosition['owner'] == $newKing['owner']) {
                    continue;
                } else {
                    $newPieces = removePieces($newPieces, [$pieceSamePosition]);
                    $newPieces[] = $newKing;
                }
            } else {
                $newPieces[] = $newKing;
            }

            if (!isCheck($newPieces, $newKing['owner'])) {
                return true;
            }
        }
    }
    return false;
}


function positionsBetweenPieces(array $piece1, array $piece2): array
{
    if ($piece1['y'] === $piece2['y']) {
        $result = [];
        $minX = min($piece1['x'], $piece2['x']);
        $maxX = max($piece1['x'], $piece2['x']);
        for ($x = $minX + 1; $x < $maxX; $x++) {
            $result[] = ['x' => $x, 'y' => $piece1['y']];
        }
        return $result;
    }

    if ($piece1['x'] === $piece2['x']) {
        $result = [];
        $minY = min($piece1['y'], $piece2['y']);
        $maxY = max($piece1['y'], $piece2['y']);
        for ($y = $minY + 1; $y < $maxY; $y++) {
            $result[] = ['x' => $piece1['x'], 'y' => $y];
        }
        return $result;
    }

    if (inDiagonal($piece1, $piece2)) {
        $result = [];
        $minX = min($piece1['x'], $piece2['x']);
        $maxX = max($piece1['x'], $piece2['x']);
        $minY = min($piece1['y'], $piece2['y']);
        $maxY = max($piece1['y'], $piece2['y']);

        for ($x = $minX + 1, $y = $minY + 1; $x < $maxX; $x++, $y++) {
            $result[] = ['x' => $x, 'y' => $y];
        }
        return $result;
    }

    return [];
}


function isMate(array $pieces, int $player): bool
{
    $piecesAttack = isCheck($pieces, $player);
    if (!$piecesAttack) {
        return false;
    }

    $king = findPieceAttr(['piece' => 'king', 'owner' => $player], $pieces);
    if (kingCanMove($king, $pieces)) {
        return false;
    }

    if (count($piecesAttack) === 1) {
        $pieceAttack = $piecesAttack[0];
        $teammateFunc = function ($p) use ($player) {
            return $p['owner'] === $player;
        };
        $playerPieces = array_filter($pieces, $teammateFunc);

        foreach ($playerPieces as $playerPiece) {
            $newPieces = [];
            if (canAttack(
                $playerPiece,
                $pieceAttack,
                removePieces(
                    $pieces,
                    [$playerPiece, $pieceAttack]
                ),
                $newPieces
            )) {
                if (!isCheck($newPieces, $player)) {
                    return false;
                }
            }
        }

        if (in_array($pieceAttack['piece'], ['queen', 'bishop', 'rook'])) {
            $safePositions = positionsBetweenPieces($king, $pieceAttack);
            foreach ($playerPieces as $playerPiece) {
                $otherPieces = removePieces($pieces, [$playerPiece]);
                foreach ($safePositions as $safePosition) {
                    if (canMove($playerPiece, $safePosition, $otherPieces)) {
                        $newPlayerPiece = at($playerPiece, $safePosition);

                        $newPieces = $otherPieces;
                        $newPieces[] = $newPlayerPiece;

                        if (!isCheck($newPieces, $player)) {
                            return false;
                        }
                    }
                }
            }
        }
    }

    return true;
}
          
___________________________________________________
class Chess {

  /**
   * The pieces.
   *
   * @var array
   */
  protected $pieces;

  /**
   * The current player.
   *
   * @var integer
   */
  protected $player;

  /**
   * The current player's king.
   *
   * @var array
   */
  protected $king;

  /**
   * Chess constructor.
   *
   * @param array $pieces
   *   The pieces.
   * @param integer $player
   *   The current player.
   */
  public function __construct(array $pieces, $player) {
    $this->pieces = $pieces;
    $this->player = $player;
    $this->king = $this->getCurrentPlayerKing();
  }

  /**
   * Check if the player's king is threatened.
   *
   * @param array $pieces
   *   An array of pieces, if empty we use $this->pieces.
   *
   * @return array|bool
   *   A list of pieces that threaten the king if any.
   */
  public function isCheck(array $pieces = []) {
    if (!$pieces) {
      $pieces = $this->pieces;
    }
    $result = [];
    foreach ($pieces as $piece) {
      // Check if it's the opponents piece.
      if ($piece['owner'] != $this->player) {
        if (
          !($piece['y'] == $this->king['y'] && $piece['x'] == $this->king['x']) &&
          $this->pieceDoesThreatenKing($piece)
        ) {
          $result[] = $piece;
        }
      }
    }

    if (!count($result)) {
      return FALSE;
    }
    return $result;
  }

  /**
   * Check if the player is mate.
   *
   * @return bool
   *   Whether or not the player is checkmate.
   */
  public function isMate() {
    $fields = [
      // Center - Center.
      $this->king,
      // Top - Center.
      ['y' => $this->king['y'] - 1, 'x' => $this->king['x']],
      // Top - Right.
      ['y' => $this->king['y'] - 1, 'x' => $this->king['x'] + 1],
      // Center - Right.
      ['y' => $this->king['y'], 'x' => $this->king['x'] + 1],
      // Bottom - Right.
      ['y' => $this->king['y'] + 1, 'x' => $this->king['x'] + 1],
      // Bottom - Center.
      ['y' => $this->king['y'] + 1, 'x' => $this->king['x']],
      // Bottom - Left.
      ['y' => $this->king['y'] + 1, 'x' => $this->king['x'] - 1],
      // Center - Left.
      ['y' => $this->king['y'], 'x' => $this->king['x'] - 1],
      // Top - Left.
      ['y' => $this->king['y'] + 1, 'x' => $this->king['x'] - 1],
    ];

    $threateningPieces = [];
    $piecesCapturableByKing = [];
    $king = $this->king;
    $mate = TRUE;

    foreach ($fields as $field) {
      if ($field['y'] < 0 || $field['x'] < 0 || $field['y'] > 7 || $field['x'] > 7) {
        continue;
      }
      foreach ($this->pieces as $pos) {
        if ($pos['y'] == $field['y'] && $pos['x'] == $field['x']) {
          if ($pos['owner'] !== $this->player) {
            $piecesCapturableByKing[$pos['piece'] . $pos['x'] . $pos['y']] = $pos;
          }
          else {
            continue 2;
          }
        }
      }
      $this->king = $field;
      if (!$this->isCheck()) {
        $mate = FALSE;
      }
    }
    foreach ($this->pieces as $piece) {
      if ($piece['owner'] == $this->player) {
        continue;
      }
      $this->king = $king;
      if ($this->pieceDoesThreatenKing($piece)) {
        $threateningPieces[$piece['piece'] . $piece['x'] . $piece['y']] = $piece;
      }
    }

    if ($mate && count($threateningPieces) == 1) {
      // Check if the king can capture one of the capturable pieces without being in check.
      foreach ($piecesCapturableByKing as $pieceCapturableByKing) {
        $this->king = $pieceCapturableByKing;
        if (!$this->isCheck()) {
          $mate = FALSE;
        }
      }
      $this->king = $king;
      // Check if the threatening piece can be captured.
      if (
        $this->pieceCanBeCaptured(reset($threateningPieces)) ||
        $this->pieceCanBeBlocked(reset($threateningPieces))
      ) {
        $mate = FALSE;
      }
    }

    return $mate;
  }

  /**
   * Check if a given piece can be captured.
   *
   * @param array $pieceToCapture
   *   The piece to capture.
   *
   * @return bool
   *   Whether or not the piece can be captured.
   */
  private function pieceCanBeCaptured($pieceToCapture) {
    $pieces = $this->pieces;
    foreach ($this->pieces as &$piece) {
      if ($piece['owner'] == $this->player) {
        $capturableFields = $this->getCapturableFields($piece);
        foreach ($capturableFields as $capturableField) {
          if ($capturableField['y'] == $pieceToCapture['y'] && $capturableField['x'] == $pieceToCapture['x']) {
            if ($piece['piece'] == 'king') {
              $this->king = $pieceToCapture;
            }
            $piece['y'] = $capturableField['y'];
            $piece['x'] = $capturableField['x'];

            foreach ($pieces as $key => $pos) {
              if ($pos['y'] == $pieceToCapture['y'] && $pos['x'] == $pieceToCapture['x']) {
                unset($pieces[$key]);
              }
            }

            if ($this->isCheck($pieces)) {
              return FALSE;
            }
            return TRUE;
          }
          // Special case for en passant.
          if (
            $piece['piece'] == 'pawn' &&
            $pieceToCapture['piece'] == 'pawn' &&
            isset($pieceToCapture['prevY']) &&
            isset($pieceToCapture['prevX']) &&
            ($pieceToCapture['x'] - $piece['x'] == 1 || $pieceToCapture['x'] - $piece['x'] == -1) &&
            $pieceToCapture['y'] == $piece['y']
          ) {
            if ($pieceToCapture['owner'] == 0 && $pieceToCapture['owner'] !== $this->player) {
              if (
                $pieceToCapture['prevY'] == 6 &&
                $pieceToCapture['y'] == 4
              ) {
                $piece['x'] = $pieceToCapture['x'];
                $piece['y'] = $pieceToCapture['y'] + 1;
                foreach ($this->pieces as $key => $piece) {
                  if ($piece['y'] == $pieceToCapture['y'] && $piece['x'] == $pieceToCapture['x']) {
                    unset($this->pieces[$key]);
                  }
                }
                if ($this->isCheck()) {
                  return FALSE;
                }
                return TRUE;
              }
            }
            elseif ($pieceToCapture['owner'] == 1 && $pieceToCapture['owner'] !== $this->player) {
              if (
                $pieceToCapture['prevY'] == 1 &&
                $pieceToCapture['y'] == 3
              ) {
                $piece['x'] = $pieceToCapture['x'];
                $piece['y'] = $pieceToCapture['y'] + 1;
                if ($this->isCheck()) {
                  return FALSE;
                }
                return TRUE;
              }
            }
          }
        }
      }
    }
    return FALSE;
  }

  /**
   * Check if a given piece can be blocked.
   *
   * @param array $pieceToBlock
   *   The piece to block.
   *
   * @return bool
   *   Whether or not the piece can be blocked.
   */
  public function pieceCanBeBlocked($pieceToBlock) {
    foreach ($this->pieces as &$piece) {
      if ($piece['owner'] == $this->player) {
        $steps = [];
        if ($pieceToBlock['piece'] == 'knight') {
          // Do nothing because knights can't be blocked.
        }
        // Diagonal movement.
        else if ($pieceToBlock['y'] != $this->king['y'] && $pieceToBlock['x'] != $this->king['x']) {
          // Up right.
          if ($pieceToBlock['y'] > $this->king['y'] && $pieceToBlock['x'] < $this->king['x']) {
            $counter = 1;
            for ($i = $pieceToBlock['y'] - 1; $i >= $this->king['y']; $i--) {
              $steps[] = ['y' => $i, 'x' => $pieceToBlock['x'] + $counter];
              $counter++;
            }
          }
          // Up left.
          else if ($pieceToBlock['y'] > $this->king['y'] && $pieceToBlock['x'] > $this->king['x']) {
            $counter = 1;
            for ($i = $pieceToBlock['y'] - 1; $i >= $this->king['y']; $i--) {
              $steps[] = ['y' => $i, 'x' => $pieceToBlock['x'] - $counter];
              $counter++;
            }
          }
          // Down right.
          else if ($pieceToBlock['y'] < $this->king['y'] && $pieceToBlock['x'] < $this->king['x']) {
            $counter = 1;
            for ($i = $pieceToBlock['y'] + 1; $i <= $this->king['y']; $i++) {
              $steps[] = ['y' => $i, 'x' => $pieceToBlock['x'] + $counter];
              $counter++;
            }
          }
          // Down left.
          else {
            $counter = 1;
            for ($i = $pieceToBlock['y'] + 1; $i <= $this->king['y']; $i++) {
              $steps[] = ['y' => $i, 'x' => $pieceToBlock['x'] - $counter];
              $counter++;
            }
          }
        }
        // Horizontal movement.
        else if ($pieceToBlock['y'] == $this->king['y']) {
          // Left to right.
          if ($pieceToBlock['x'] < $this->king['x']) {
            for ($i = $pieceToBlock['x'] + 1; $i <= $this->king['x']; $i++) {
              $steps[] = ['y' => $pieceToBlock['y'], 'x' => $i];
            }
          }
          // Right to left.
          else {
            for ($i = $pieceToBlock['x'] - 1; $i >= $this->king['x']; $i--) {
              $steps[] = ['y' => $pieceToBlock['y'], 'x' => $i];
            }
          }
        }
        // Vertical movement.
        else {
          // Up.
          if ($pieceToBlock['y'] > $this->king['y']) {
            for ($i = $pieceToBlock['y'] - 1; $i >= $this->king['y']; $i--) {
              $steps[] = ['y' => $i, 'x' => $pieceToBlock['x']];
            }
          }
          // Down.
          else {
            for ($i = $pieceToBlock['y'] + 1; $i <= $this->king['y']; $i++) {
              $steps[] = ['y' => $i, 'x' => $pieceToBlock['x']];
            }
          }
        }
        $capturableFields = $this->getCapturableFields($piece);
        foreach ($capturableFields as $capturableField) {
          if ($piece['piece'] == 'pawn') {
            if ($piece['owner'] == 1) {
              $capturableField['y'] = $piece['y'] + 1;
              $capturableField['x'] = $piece['x'];
            }
            else {
              $capturableField['y'] = $piece['y'] - 1;
              $capturableField['x'] = $piece['x'];
            }
          }
          foreach ($steps as $step) {
            if (
              $capturableField['y'] == $step['y'] &&
              $capturableField['x'] == $step['x'] &&
              !($capturableField['y'] == $this->king['y'] && $capturableField['x'] == $this->king['x'])
            ) {
              return TRUE;
            }
          }
        }
      }
    }
    return FALSE;
  }

  /**
   * Get the position of the current player's king.
   *
   * @return array
   *   The current player's king.
   */
  private function getCurrentPlayerKing() {
    foreach ($this->pieces as $piece) {
      if ($piece['piece'] == 'king' && $piece['owner'] == $this->player) {
        return $piece;
      }
    }
    return [];
  }

  /**
   * Check if a piece threatens the king.
   *
   * @param array $piece
   *   The piece to check.
   *
   * @return bool
   *   Whether the piece threatens the king or not.
   */
  private function pieceDoesThreatenKing(array $piece) {
    $capturableFields = $this->getCapturableFields($piece);
    foreach ($capturableFields as $capturableField) {
      if ($capturableField['y'] == $this->king['y'] && $capturableField['x'] == $this->king['x']) {
        return TRUE;
      }
    }
    return FALSE;
  }

  /**
   * Get a list of fields the piece can capture.
   *
   * @param array $piece
   *   The piece to get capturable fields for.
   *
   * @return array
   *   A list of the capturable fields.
   */
  private function getCapturableFields(array $piece) {
    $result = [];
    switch ($piece['piece']) {
      case 'rook':
        $this->rookCapturableFields($result, $piece);
        break;
      case 'bishop':
        $this->bishopCapturableFields($result, $piece);
        break;
      case 'queen':
        $this->rookCapturableFields($result, $piece);
        $this->bishopCapturableFields($result, $piece);
        break;
      case 'knight':
        // Forward moves.
        $result[] = ['y' => $piece['y'] - 2, 'x' => $piece['x'] + 1];
        $result[] = ['y' => $piece['y'] - 2, 'x' => $piece['x'] - 1];
        $result[] = ['y' => $piece['y'] - 1, 'x' => $piece['x'] + 2];
        $result[] = ['y' => $piece['y'] - 1, 'x' => $piece['x'] - 2];

        // Backward moves.
        $result[] = ['y' => $piece['y'] + 2, 'x' => $piece['x'] + 1];
        $result[] = ['y' => $piece['y'] + 2, 'x' => $piece['x'] - 1];
        $result[] = ['y' => $piece['y'] + 1, 'x' => $piece['x'] + 2];
        $result[] = ['y' => $piece['y'] + 1, 'x' => $piece['x'] - 2];
        break;
      case 'pawn':
        // The owner is black (no we're not racists).
        if ($piece['owner'] == 1) {
          $result[] = ['y' => $piece['y'] + 1, 'x' => $piece['x'] + 1];
          $result[] = ['y' => $piece['y'] + 1, 'x' => $piece['x'] - 1];
        }
        else {
          $result[] = ['y' => $piece['y'] - 1, 'x' => $piece['x'] + 1];
          $result[] = ['y' => $piece['y'] - 1, 'x' => $piece['x'] - 1];
        }
        break;
    }
    // Remove positions that extend the boards size.
    foreach ($result as $key => $pos) {
      if ($pos['y'] < 0 || $pos['x'] < 0 || $pos['y'] > 7 || $pos['x'] > 7) {
        unset($result[$key]);
      }
    }

    return $result;
  }

  /**
   * Checks if a movement is blocked by another piece.
   *
   * @param array $movement
   *   A list of coordinates determining the piece's movement.
   *
   * @return bool
   *   Whether or not the movement is blocked.
   */
  private function movementBlockedByPiece(array $movement) {
    $steps = [];
    // Diagonal movement.
    if ($movement['y']['start'] != $movement['y']['end'] && $movement['x']['start'] != $movement['x']['end']) {
      // Up right.
      if ($movement['y']['start'] > $movement['y']['end'] && $movement['x']['start'] < $movement['x']['end']) {
        $counter = 1;
        for ($i = $movement['y']['start'] - 1; $i >= $movement['y']['end']; $i--) {
          $steps[] = ['y' => $i, 'x' => $movement['x']['start'] + $counter];
          $counter++;
        }
      }
      // Up left.
      else if ($movement['y']['start'] > $movement['y']['end'] && $movement['x']['start'] > $movement['x']['end']) {
        $counter = 1;
        for ($i = $movement['y']['start'] - 1; $i >= $movement['y']['end']; $i--) {
          $steps[] = ['y' => $i, 'x' => $movement['x']['start'] - $counter];
          $counter++;
        }
      }
      // Down right.
      else if ($movement['y']['start'] < $movement['y']['end'] && $movement['x']['start'] < $movement['x']['end']) {
        $counter = 1;
        for ($i = $movement['y']['start'] + 1; $i <= $movement['y']['end']; $i++) {
          $steps[] = ['y' => $i, 'x' => $movement['x']['start'] + $counter];
          $counter++;
        }
      }
      // Down left.
      else {
        $counter = 1;
        for ($i = $movement['y']['start'] + 1; $i <= $movement['y']['end']; $i++) {
          $steps[] = ['y' => $i, 'x' => $movement['x']['start'] - $counter];
          $counter++;
        }
      }
    }
    // Horizontal movement.
    else if ($movement['y']['start'] == $movement['y']['end']) {
      // Left to right.
      if ($movement['x']['start'] < $movement['x']['end']) {
        for ($i = $movement['x']['start'] + 1; $i <= $movement['x']['end']; $i++) {
          $steps[] = ['y' => $movement['y']['start'], 'x' => $i];
        }
      }
      // Right to left.
      else {
        for ($i = $movement['x']['start'] - 1; $i >= $movement['x']['end']; $i--) {
          $steps[] = ['y' => $movement['y']['start'], 'x' => $i];
        }
      }
    }
    // Vertical movement.
    else {
      // Up.
      if ($movement['y']['start'] > $movement['y']['end']) {
        for ($i = $movement['y']['start'] - 1; $i >= $movement['y']['end']; $i--) {
          $steps[] = ['y' => $i, 'x' => $movement['x']['start']];
        }
      }
      // Down.
      else {
        for ($i = $movement['y']['start'] + 1; $i <= $movement['y']['end']; $i++) {
          $steps[] = ['y' => $i, 'x' => $movement['x']['start']];
        }
      }
    }
    foreach ($this->pieces as $piece) {
      if ($piece['owner'] !== $this->player) {
        continue;
      }
      if (
        !($piece['y'] == $this->king['y'] && $piece['x'] == $this->king['x']) ||
        !($movement['y']['end'] == $this->king['y'] && $movement['x']['end'] == $this->king['x'])
      ) {
        foreach ($steps as $step) {
          if ($step['y'] == $piece['y'] && $step['x'] == $piece['x']) {
            return TRUE;
          }
        }
      }
    }

    return FALSE;
  }

  /**
   * Get a rook's capturable fields.
   *
   * @param array $result
   *   An array containing all the capturable fields.
   * @param array $piece
   *   The piece to get the fields from.
   */
  private function rookCapturableFields(array &$result, array $piece) {
    // Up.
    for ($i = $piece['y'] - 1; $i >= 0; $i--) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $i], 'x' => ['start' => $piece['x'], 'end' => $piece['x']]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
    }
    // Down
    for ($i = $piece['y'] + 1; $i <= 7; $i++) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $i], 'x' => ['start' => $piece['x'], 'end' => $piece['x']]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
    }
    // Left.
    for ($i = $piece['x'] - 1; $i >= 0; $i--) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $piece['y']], 'x' => ['start' => $piece['x'], 'end' => $i]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
    }
    // Right.
    for ($i = $piece['x'] + 1; $i <= 7; $i++) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $piece['y']], 'x' => ['start' => $piece['x'], 'end' => $i]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
    }
  }

  /**
   * Get a bishops's capturable fields.
   *
   * @param array $result
   *   An array containing all the capturable fields.
   * @param array $piece
   *   The piece to get the fields from.
   */
  private function bishopCapturableFields(array &$result, array $piece) {
    // Up right.
    $counter = 1;
    for ($i = $piece['y'] - 1; $i >= 0; $i--) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $i], 'x' => ['start' => $piece['x'], 'end' => $piece['x'] + $counter]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
      $counter++;
    }
    // Up left.
    $counter = 1;
    for ($i = $piece['y'] - 1; $i >= 0; $i--) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $i], 'x' => ['start' => $piece['x'], 'end' => $piece['x'] - $counter]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
      $counter++;
    }
    // Down right.
    $counter = 1;
    for ($i = $piece['y'] + 1; $i <= 7; $i++) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $i], 'x' => ['start' => $piece['x'], 'end' => $piece['x'] + $counter]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
      $counter++;
    }
    // Down left.
    $counter = 1;
    for ($i = $piece['y'] + 1; $i <= 7; $i++) {
      $movement = ['y' => ['start' => $piece['y'], 'end' => $i], 'x' => ['start' => $piece['x'], 'end' => $piece['x'] - $counter]];
      if (!$this->movementBlockedByPiece($movement)) {
        $result[] = ['y' => $movement['y']['end'], 'x' => $movement['x']['end']];
      }
      $counter++;
    }
  }
}

function isCheck($pieces, $player) {
  return (new Chess($pieces, $player))->isCheck();
}

function isMate($pieces, $player) {
  return (new Chess($pieces, $player))->isMate();
}
          
___________________________________________________
function isCheck($pieces, $player){
  foreach($pieces as $k=>$v){
    if($v['piece'] == 'king' && $v['owner'] == $player){
      $kingPosi = [$v['x'],$v['y']];
    }
  }
  $rs = isDanger($pieces,$kingPosi,$player);
  return $rs;
}

function isMate($pieces, $player){
  $isCheck = isCheck($pieces, $player);
  foreach($pieces as $k=>$v){
    if($v['piece'] == 'king' && $v['owner'] == $player){
      $kingPosi = [$v['x'],$v['y']];
      $kingP = $k;
    }
    if( !empty($v['prevX']) ){
      $lastMoves = [$v['x'],$v['y']];
      $lastMovesPosi = $k;
      $lastMovesUnit = $v['piece'];
    }
  }
  // Cac nuoc nam giua tuong va quan vua di
  if( $lastMovesUnit == 'queen' ){
    if( $lastMoves[0] == $kingPosi[0] ){
      $distanceCheck = $lastMoves[1] - $kingPosi[1];
      for($i = 1; $i< abs($distancCheck); $i++){
        $wayCheck[] = $distanceCheck > 0 ? [$lastMoves[0],$i+$kingPosi[1]] : [$lastMoves[0],$i+$lastMoves[1]]; 
      }
    }elseif( $lastMoves[1] == $kingPosi[1] ){
      $distanceCheck = $lastMoves[0] - $kingPosi[0];
      for($i = 1; $i< abs($distancCheck); $i++){
        $wayCheck[] = $distanceCheck > 0 ? [$i+$kingPosi[0],$lastMoves[1]] : [$i+$lastMoves[0],$lastMoves[1]];
      }
    }else{
      $distanceCheck[0] = $lastMoves[0] - $kingPosi[0];
      $distanceCheck[1] = $lastMoves[1] - $kingPosi[1];
      for($i = 1; $i< abs($distanceCheck[0]); $i++){
        if( $distanceCheck[0] > 0 ){
          $wayCheck[] = $distanceCheck[1] > 0 ? [$kingPosi[0] + $i ,$kingPosi[1] + $i] : [$kingPosi[0] + $i ,$kingPosi[1] - $i];
        }else{
          $wayCheck[] = $distanceCheck[1] > 0 ? [$lastMoves[0] + $i ,$lastMoves[1] + $i] : [$lastMoves[0] + $i ,$lastMoves[1] - $i];
        }
      }
    }
    $wayCheck[] = $lastMoves;
  }elseif( $lastMovesUnit == 'rook' ){
    if( $lastMoves[0] == $kingPosi[0] ){
      $distanceCheck = $lastMoves[1] - $kingPosi[1];
      for($i = 1; $i< abs($distancCheck); $i++){
        $wayCheck[] = $distanceCheck > 0 ? [$lastMoves[0],$i+$kingPosi[1]] : [$lastMoves[0],$i+$lastMoves[1]]; 
      }
    }elseif( $lastMoves[1] == $kingPosi[1] ){
      $distanceCheck = $lastMoves[0] - $kingPosi[0];
      for($i = 1; $i< abs($distancCheck); $i++){
        $wayCheck[] = $distanceCheck > 0 ? [$i+$kingPosi[0],$lastMoves[1]] : [$i+$lastMoves[0],$lastMoves[1]];
      }
    }
    $wayCheck[] = $lastMoves;
  }elseif( $lastMovesUnit == 'bishop' ){
    $distanceCheck[0] = $lastMoves[0] - $kingPosi[0];
    $distanceCheck[1] = $lastMoves[1] - $kingPosi[1];
    for($i = 1; $i< abs($distanceCheck[0]); $i++){
      if( $distanceCheck[0] > 0 ){
        $wayCheck[] = $distanceCheck[1] > 0 ? [$kingPosi[0] + $i ,$kingPosi[1] + $i] : [$kingPosi[0] + $i ,$lastMoves[1] + $i];
      }else{
        $wayCheck[] = $distanceCheck[1] > 0 ? [$lastMoves[0] + $i ,$kingPosi[1] + $i] : [$lastMoves[0] + $i ,$lastMoves[1] + $i];
      }
    }
    $wayCheck[] = $lastMoves;
  }else{
    $wayCheck[] = $lastMoves;
  }

  if( count(isCheck) > 0 ){
    $kingMoves = kingMoves($kingPosi);
    $help = 0;
    foreach($pieces as $i=>$j){
    
      // Check ăn còn vừa đi
      if($j['owner'] == $player){
        if($j['piece'] == 'queen'){
          $moves = queenMoves([ $j['x'], $j['y'] ]);          
          foreach($moves as $k=>$v){

            foreach($wayCheck as $key=>$value){
              // Check xem có vật cản k?
              if( $v[0] == $value[0] && $v[1] == $value[1] ){
                if( $j['x'] == $value[0] ){
                  $distance = $value[1] - $j['y'];
                  $haveBaries = checkMiddles($pieces, $value, $distance, 1);
                }elseif( $j['y'] == $value[1] ){
                  $distance = $value[0] - $j['x'];
                  $haveBaries = checkMiddles($pieces, $value, $distance, 2);
                }else{
                  $distance[0] = $value[0] - $j['x'];
                  $distance[1] = $value[1] - $j['y'];
                  $haveBaries = checkMiddles($pieces, $value, $distance, 3);
                }
                unset($distance);
                if( $haveBaries == 1 ){
                  // Nếu ăn có hở mặt tướng không?                
                  $piecesEx = $pieces;
                  $piecesEx[$i]['x'] = $value[0];
                  $piecesEx[$i]['y'] = $value[1];
                  unset($piecesEx[$lastMovesPosi]);
                  $danger = isDanger($piecesEx,$kingPosi,$player);                
                  if( count($danger) == 0){
                    $help += $haveBaries;
                  }                
                }
              }
            }

          }
        }elseif($j['piece'] == 'rook'){
          $moves = rookMoves([ $j['x'], $j['y'] ]);
          foreach($moves as $k=>$v){

            foreach($wayCheck as $key=>$value){
              if( $v[0] == $value[0] && $v[1] == $value[1] ){
                // Check xem có vật cản k?
                if( $j['x'] == $value[0] ){
                  $distance = $value[1] - $j['y'];
                  $haveBaries = checkMiddles($pieces, $value, $distance, 1);
                }elseif( $j['y'] == $value[1] ){
                  $distance = $value[0] - $j['x'];
                  $haveBaries = checkMiddles($pieces, $value, $distance, 2);
                }
                unset($distance);
                if( $haveBaries == 1 ){
                  // Nếu ăn có hở mặt tướng không?
                  $piecesEx = $pieces;
                  $piecesEx[$i]['x'] = $lastMoves[0];
                  $piecesEx[$i]['y'] = $lastMoves[1];
                  unset($piecesEx[$lastMovesPosi]);
                  $danger = isDanger($piecesEx,$kingPosi,$player);
                  if( count($danger) == 0){
                    $help += $haveBaries;
                  }
                }
                
              }
            }

          }
        }elseif($j['piece'] == 'bishop'){
          $moves = bishopMoves([ $j['x'], $j['y'] ]);
          foreach($moves as $k=>$v){

            foreach( $wayCheck as $key=>$value){
              if( $v[0] == $value[0] && $v[1] == $value[1] ){
                // Check xem có vật cản k?
                $distance[0] = $value[0] - $j['x'];
                $distance[1] = $value[1] - $j['y'];
                $haveBaries = checkMiddles($pieces, $value, $distance, 3);
                unset($distance);
                if( $haveBaries == 1 ){
                  // Nếu ăn có hở mặt tướng không?
                  $piecesEx = $pieces;
                  $piecesEx[$i]['x'] = $value[0];
                  $piecesEx[$i]['y'] = $value[1];
                  unset($piecesEx[$lastMovesPosi]);
                  $danger = isDanger($piecesEx,$kingPosi,$player);
                  if( count($danger) == 0){
                    $help += $haveBaries;
                  }
                }
                
              }
            }

          }
        }elseif($j['piece'] == 'knight'){
          $moves = knightMoves([ $j['x'], $j['y'] ]);
          foreach($moves as $k=>$v){
            
            foreach( $wayCheck as $key=>$value){
              if( $v[0] == $value[0] && $v[1] == $value[1] ){
                // Nếu ăn có hở mặt tướng không?
                $piecesEx = $pieces;
                $piecesEx[$i]['x'] = $value[0];
                $piecesEx[$i]['y'] = $value[1];
                unset($piecesEx[$lastMovesPosi]);
                $danger = isDanger($piecesEx,$kingPosi,$player);
                if( count($danger) == 0){
                  $help += 1;
                }
              }
            }
            
          }
        }elseif($j['piece'] == 'pawn'){
          // Check an con vua di
          $moves = pawnMoves([$j['x'], $j['y']], $j['player']);
          foreach($moves as $k=>$v){
            if( $v[0] == $lastMoves[0] && $v[1] == $lastMoves[1] ){
              // Nếu ăn có hở mặt tướng không?
              $piecesEx = $pieces;
              $piecesEx[$i]['x'] = $lastMoves[0];
              $piecesEx[$i]['y'] = $lastMoves[1];
              unset($piecesEx[$lastMovesPosi]);
              $danger = isDanger($piecesEx,$kingPosi,$player);
              if( count($danger) == 0){
                $help += 1;
              }
            }
          }
          
          // Bat tot qua duong
          if( $lastMovesUnit == 'pawn' && $j['y'] == $lastMoves[1] && ( $j['x'] == $lastMoves[0] - 1 || $j['x'] == $lastMoves[0] + 1) ){
            $piecesEx = $pieces;
            if( $j['owner'] == 0 ){
              $piecesEx[$i]['x'] = $lastMoves[0];
              $piecesEx[$i]['y'] = $lastMoves[1] - 1;
              unset($piecesEx[$lastMovesPosi]);
            }else{
              $piecesEx[$i]['x'] = $lastMoves[0];
              $piecesEx[$i]['y'] = $lastMoves[1] + 1;
              unset($piecesEx[$lastMovesPosi]);
            }
            $danger = isDanger($piecesEx,$kingPosi,$player);
            if( count($danger) == 0){
              $help += 1;
            }
          }
          
          // Check chan con vua di
          foreach( $wayCheck as $key=>$value){
            if( $value != $lastMoves){
              if( $j['owner'] == 0 ){
                $frontPawn = [ [$j['x'],$j['y'] - 1] ];
                if( $j['y'] == 6 ){
                  $frontPawn[] = [$j['x'],$j['y'] - 2];
                }
              }else{
                $frontPawn = [ [$j['x'],$j['y'] + 1] ];
                if( $j['y'] == 1 ){
                  $frontPawn[] = [$j['x'],$j['y'] + 2];
                }
              }
              foreach($frontPawn as $keys=>$values){
                if( $values[0] == $value[0] && $values[1] == $value[1] ){
                  // Nếu ăn có hở mặt tướng không?
                  $piecesEx = $pieces;
                  $piecesEx[$i]['x'] = $value[0];
                  $piecesEx[$i]['y'] = $value[1];
                  unset($piecesEx[$lastMovesPosi]);
                  $danger = isDanger($piecesEx,$kingPosi,$player);
                  if( count($danger) == 0){
                    $help += 1;
                  }
                }
              }
            }
          }
          
        }elseif($j['piece'] == 'king'){
          $moves = kingMoves([$j['x'], $j['y']]);
          $piecesEx = $pieces;
          unset($piecesEx[$lastMovesPosi],$piecesEx[$kingP]);
          $danger = isDanger($piecesEx,$lastMoves,$player);
          if( count($danger) == 0 ){
            foreach($moves as $k=>$v){
              if( $v[0] == $lastMoves[0] && $v[1] == $lastMoves[1] ){
                $help += 1;
              }
            }
          }
        }
        unset($distance);
        foreach($kingMoves as $k=>$v){
          if($v[0] == $j['x'] && $v[1] == $j['y']){
            unset($kingMoves[$k]);
          }
        }
//         print_r($help);
        
      }elseif($j['owner'] != $player){
        // Check đội bạn bo đường của vua
        if($j['piece'] == 'queen'){
          $moves = queenMoves([ $j['x'], $j['y'] ]);
          foreach($kingMoves as $k=>$v){
            foreach($moves as $kk=>$vv){
              if($v[0] == $vv[0] && $v[1] == $vv[1]){
                unset($kingMoves[$k]);
              }
            }
          }
        }elseif($j['piece'] == 'rook'){
          $moves = rookMoves([ $j['x'], $j['y'] ]);
          foreach($kingMoves as $k=>$v){
            foreach($moves as $kk=>$vv){
              if($v[0] == $vv[0] && $v[1] == $vv[1]){
                unset($kingMoves[$k]);
              }
            }
          }
        }elseif($j['piece'] == 'bishop'){
          $moves = bishopMoves([ $j['x'], $j['y'] ]);
          foreach($kingMoves as $k=>$v){
            foreach($moves as $kk=>$vv){
              if($v[0] == $vv[0] && $v[1] == $vv[1]){
                unset($kingMoves[$k]);
              }
            }
          }
        }elseif($j['piece'] == 'knight'){
          $moves = knightMoves([ $j['x'], $j['y'] ]);
          foreach($kingMoves as $k=>$v){
            foreach($moves as $kk=>$vv){
              if($v[0] == $vv[0] && $v[1] == $vv[1]){
                unset($kingMoves[$k]);
              }
            }
          }
        }elseif($j['piece'] == 'pawn'){
          $moves = pawnMoves([ $j['x'], $j['y'] ],$j['player'] );
          foreach($kingMoves as $k=>$v){
            foreach($moves as $kk=>$vv){
              if($v[0] == $vv[0] && $v[1] == $vv[1]){
                unset($kingMoves[$k]);
              }
            }
          }
        }
      }
    }
    print_r( count($kingMoves).'-');
    print_r( $help.'.');
    if( count($kingMoves) == 0 && $help == 0 ){
      return true;
    }
  }
  return false;
}

function kingMoves($pos){
  $moves = [ [$pos[0]-1,$pos[1]-1],[$pos[0]-1,$pos[1]],[$pos[0]-1,$pos[1]+1],[$pos[0],$pos[1]-1],[$pos[0],$pos[1]+1],[$pos[0]+1,$pos[1]-1],[$pos[0]+1,$pos[1]],[$pos[0]+1,$pos[1]+1] ];
  foreach($moves as $k=>$v){
    if( $v[0]<0 || $v[0] >7 || $v[1]<0 || $v[1] >7){
      unset($moves[$k]);
    }
  }
  return $moves;
}

function queenMoves($pos){
  for($i = 0; $i < 8; $i++){
    $moves[] = [$pos[0],$i];
    $moves[] = [$i,$pos[1]];
    
    $minus = abs($pos[0] - $i);
    for($j = 0; $j<8; $j++){
      if( abs($pos[1] - $j) == $minus ){
        $moves[] = [$i,$j];
      }
    }
  }
  $overlap = array_search($pos,$moves);
  unset($moves[$overlap]);
  return $moves;
}

function rookMoves($pos){
  for($i = 0; $i < 8; $i++){
    $moves[] = [$pos[0],$i];
    $moves[] = [$i,$pos[1]];
  }
  $overlap = array_search($pos,$moves);
  unset($moves[$overlap]);
  return $moves;
}

function bishopMoves($pos){
  for($i = 0; $i<8; $i++){
    $minus = abs($pos[0] - $i);
    for($j = 0; $j<8; $j++){
      if( abs($pos[1] - $j) == $minus ){
        $moves[] = [$i,$j];
      }
    }
  }
  $overlap = array_search($pos,$moves);
  unset($moves[$overlap]);
  return $moves;
}

function knightMoves($pos){
  for($i = 1; $i <= 2; $i++){    
    $j = $i == 1 ? 2 : 1 ;
    $moves[]=[$pos[0]-$i,$pos[1]-$j];
    $moves[]=[$pos[0]-$i,$pos[1]+$j];
    $moves[]=[$pos[0]+$i,$pos[1]-$j];
    $moves[]=[$pos[0]+$i,$pos[1]+$j];
  }
  return $moves;
}

function pawnMoves($pos,$play){
  if($play == 0){
    $moves = [ [$pos[0]-1,$pos[1]-1], [$pos[0]+1,$pos[1]-1] ];
  }else{
    $moves = [ [$pos[0]+1,$pos[1]+1], [$pos[0]-1,$pos[1]+1] ];
  }
  return $moves;
}

function isDanger($pieces,$kingPosi,$player){
  foreach($pieces as $k=>$v){
    if($v['owner'] != $player){
      if($v['piece'] == 'queen'){
        $moves = queenMoves([ $v['x'], $v['y'] ]);
        if( in_array($kingPosi, $moves) ){
          // Check vật cản
          if( $v['x'] == $kingPosi[0] ){
            $distance = $kingPosi[1] - $v['y'];
            $hasBaries = checkMiddles($pieces, $kingPosi, $distance, 1);
          }elseif( $v['y'] == $kingPosi[1] ){
            $distance = $kingPosi[0] - $v['x'];
            $hasBaries = checkMiddles($pieces, $kingPosi, $distance, 2);
          }else{
            $distance[0] =  $kingPosi[0] - $v['x'];
            $distance[1] =  $kingPosi[1] - $v['y'];
            $hasBaries = checkMiddles($pieces, $kingPosi, $distance, 3);
          }
          if($hasBaries == 1){
            $rs[] = $v;
          }
        }
      }elseif($v['piece'] == 'rook'){
        $moves = rookMoves([ $v['x'], $v['y'] ]);
        if( in_array($kingPosi, $moves) ){
          // Check vật cản
          if( $v['x'] == $kingPosi[0] ){
            $distance = $kingPosi[1] - $v['y'];
            $hasBaries = checkMiddles($pieces, $kingPosi, $distance, 1);
          }elseif( $v['y'] == $kingPosi[1] ){
            $distance = $kingPosi[0] - $v['x'];
            $hasBaries = checkMiddles($pieces, $kingPosi, $distance, 2);
          }
          if($hasBaries == 1){
            $rs[] = $v;
          }
        }
      }elseif($v['piece'] == 'bishop'){
        $moves = bishopMoves([ $v['x'], $v['y'] ]);
        if( in_array($kingPosi, $moves) ){
          $distance[0] =  $kingPosi[0] - $v['x'];
          $distance[1] =  $kingPosi[1] - $v['y'];
          $hasBaries = checkMiddles($pieces, $kingPosi, $distance, 3);
          if($hasBaries == 1){
            $rs[] = $v;
          }
        }
      }elseif($v['piece'] == 'knight'){
        $moves = knightMoves([ $v['x'], $v['y'] ]);
        if( in_array($kingPosi, $moves) ){
          $rs[] = $v;
        }
      }elseif($v['piece'] == 'pawn'){
        $moves = pawnMoves([ $v['x'], $v['y'] ],$v['owner'] );
        if( in_array($kingPosi, $moves) ){
          $rs[] = $v;
        }
      }
    }
  }
  return $rs;
}

function checkMiddles($pieces, $lastMoves, $distance, $way){
  if($way == 1){
    if($distance > 0){
      for($i = 1; $i < $distance; $i++){
        foreach($pieces as $k=>$v){
          if( $v['x'] == $lastMoves[0] && $v['y'] == ($lastMoves[1] - $distance + $i) ){
            return 0;
          }
        }
      }
    }elseif($distance < 0){
      for($i = 1; $i < abs($distance); $i++){
        foreach($pieces as $k=>$v){
          if( $v['x'] == $lastMoves[0] && $v['y'] == ($lastMoves[1] + $i) ){
            return 0;
          }
        }
      }
    }
  }elseif($way == 2){
    if($distance > 0){
      for($i = 1; $i < $distance; $i++){
        foreach($pieces as $k=>$v){
          if( $v['y'] == $lastMoves[1] && $v['x'] == ($lastMoves[0] - $distance + $i) ){
            return 0;
          }
        }
      }
    }elseif($distance < 0){
      for($i = 1; $i < abs($distance); $i++){
        foreach($pieces as $k=>$v){
          if($v['y'] == $lastMoves[1] && $v['x'] == ($lastMoves[0] + $i) ){
            return 0;
          }
        }
      }
    }
  }elseif($way == 3){
    if($distance[0] > 0 && $distance[1] > 0){
      for($i = 1; $i < $distance[0]; $i++){
        foreach($pieces as $k=>$v){
          if( $v['x'] == ($lastMoves[0] - $i) && $v['y'] == ($lastMoves[1] - $i) ){
            return 0;
          }
        }
      }
    }elseif($distance[0] > 0 && $distance[1] < 0 ){
      for($i = 1; $i < $distance[0]; $i++){
        foreach($pieces as $k=>$v){
          if( $v['x'] == ($lastMoves[0] - $i) && $v['y'] == ($lastMoves[1] + $i) ){
            return 0;
          }
        }
      }
    }elseif($distance[0] < 0 && $distance[1] > 0 ){
      for($i = 1; $i < $distance[1]; $i++){
        foreach($pieces as $k=>$v){
          if( $v['x'] == ($lastMoves[0] + $i) && $v['y'] == ($lastMoves[1] - $i) ){
            return 0;
          }
        }
      }
    }elseif($distance[0] < 0 && $distance[1] < 0 ){
      print_r(1);
      for($i = 1; $i < abs($distance[0]); $i++){
        foreach($pieces as $k=>$v){
          if( $v['x'] == ($lastMoves[0] + $i) && $v['y'] == ($lastMoves[1] + $i) ){
            return 0;
          }
        }
      }
    }
  }
  return 1;
}
