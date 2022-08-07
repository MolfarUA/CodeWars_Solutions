5a20eeccee1aae3cbc000090


/*
 * An attempt to design a simple, concise algorithm,
 * rather than an algorithm that generates an efficient solution.
 *
 * @param {number[][]} arr
 * @return {number[]|null}
 */
function slidePuzzle($arr) {
    $moves = [];
    $n = count($arr);
    $m = $n;
    $list = array_merge(...$arr);

    // Functions to do basic indexing.
    $col = function ($tile) use (&$list, &$m) { return array_search($tile, $list) % $m; };
    $row = function ($tile) use (&$list, &$m) { return intval(array_search($tile, $list)/$m); };
    // Functions to move the empty slot to a neighboring position.
    $shift = function ($offset, $count) use (&$list, &$moves) {
        $j = array_search(0, $list);
        $offset *= ($count < 0 ? -1 : 1);
        for ($count = abs($count); $count > 0; $count -= 1) {
            $moves[] = $list[$j] = $list[$j + $offset];
            $list[$j = $j + $offset] = 0;
        }
    };
    $right = function ($d = 1) use (&$shift) { $shift(1, $d); };
    $left = function ($d = 1) use (&$shift) { $shift(-1, $d); };
    $down = function ($d = 1) use (&$shift, &$m) { $shift($m, $d); };
    $up = function ($d = 1) use (&$shift, &$m) { $shift(-$m, $d); };
    // Function to move the empty slot around a rectangle.
    $box = function ($w, $h = 0) use (&$right, &$left, &$up, &$down) {
        $down(($h ?: $w) - 1); $left($w); $up($h ?: $w); $right($w); $down();
    };

    // On each level, we solve the top row and left column.
    for ($level = 0; $level < $n - 2; $level += 1) {
        // Ensure standard starting position.
        $down(1 - $row(0));
        $right($m - 1 - $col(0));

        // Start by loading some "safe" tiles into the top row - ones we won't
        // use on this level.  The paths traversed here are long enough
        // that we will always be able to find suitable tiles.
        for ($j = 0; $j < $m; $j += 1) {
            if ($j !== $m - 1 || $list[0] % $n === $level + 1) {
                $down();
                while ($list[2*$m - 1] <= $n*$level + $n || $list[2*$m - 1] % $n === $level + 1) {
                    $left($m - 1); $up(2);
                    $right($m - 1 - $j); $down(); $right($j); $down();
                }
                $up(); $box($m - 1, 2);
            }
        }

        // We have 2*m - 1 tiles to position for this level.
        for ($j = -$m + 1; $j < $m; $j += 1) {
            // This is the tile we want to position next.
            $subject = ($j < 0
                ? (($n + 1)*$level - $n*$j + 1)
                : (($n + 1)*$level + $j + 1)
            );

            // Position this tile to be next in line.
            if (array_search($subject, $list) !== array_search(0, $list) + $m) {
                if ($col($subject) === $m - 1) {
                    $down($row($subject) - $row(0));
                    for ($k = $row($subject) - 2; $k > 0; $k -= 1) {
                        $left(); $up(2); $right(); $down();
                    }
                    $left(); $up(2); $right();
                } else {
                    $down(min($m - 2, $row($subject)) - $row(0));
                    $left($col(0) - $col($subject));
                    if ($row($subject) == $m - 1) {
                        $down(); $right(); $up(); $left();
                    }
                    for ($k = $m - 1 - $col($subject); $k > 0; $k -= 1) {
                        $down(); $right(2); $up(); $left();
                    }
                    $down(); $right();
                    for ($k = $row($subject) - 1; $k > 0; $k -= 1) {
                        $left(); $up(2); $right(); $down();
                    }
                    $up();
                }
            }

            // March around the edges to shift the tiles by one position.
            $box($m - 1);
        }

        // Remove the completed row and column for the next iteration level.
        $m -= 1;
        $list = array_slice($list, $m + 2);
        for ($j = 0; $j < $m - 1; $j += 1) {
            array_splice($list, ($j + 1)*$m, 1);
        }
    }

    // We are left with a 2x2 array to solve and check.
    $down();
    while($list[0] !== $n*$n - $n - 1) {
        $box(1, 1);
    }
    return ($list[2] === $n*$n - 1 ? $moves : null);
}
_________________________________________
function slidePuzzle($matrix){
    $obj = new Solver($matrix);
  
//   if(count($matrix)>9){
//     var_dump($matrix);
//     return null;
//   }
  
  return $obj->solve();
}

class Solver
{
    public $board;
    public $dispatcher;
    public $matrix = [];

    public function __construct(array $matrix)
    {
        $this->matrix = $matrix;
        $this->board = new Board($matrix);
        $this->dispatcher = new Dispatcher($this->board);
    }

    public function solve()
    {
        while (!$this->dispatcher->result) {
            // get next walker
            $this->dispatcher->moveWalkerToTarget();
        }

        if ($this->dispatcher->result !== 'solved') {
            return null;
        }

        return $this->board->movedNumbers;
    }

}

class Dispatcher
{
    public $board;
    public $walker;
    public $pathfinder;
    public $allowed;
    public $result = '';

    public function __construct(Board $board)
    {
        $this->board = $board;
        $this->walker = new Tile();
        $this->pathfinder = new Pathfinder($this->board);

        $this->allowed = range(0, $this->board->getWidth() * $this->board->getHeight() - 1);
        unset($this->allowed[0]);
    }

    public function moveWalkerToTarget()
    {
        // Get next walker number
        $this->walker->number = $this->getNextWalkerNumber();

        // Get walker coords
        $this->walker->coords = $this->board->getCoords($this->walker->number);
        $this->walker->solvedCoords = $this->board->getCorrectCoords($this->walker->number);

        // Get walker target
        $this->walker->targetCoords = $this->getWalkerTarget();

        // While walker not reached the destination
        while ($this->walker->coords !== $this->walker->targetCoords) {
            // Get walker next step
            $this->walker->nextStepCoords = $this->getWalkerNextStepCoords();

            // Block or allow needed tiles
            $this->setAllowed();

            // Move zero to walker next step
            $this->pathfinder->moveZeroTo($this->walker->nextStepCoords, $this->allowed);

            // Swap Zero and Walker
            $this->swapZeroAndWalker();

            // Get new walker coords after swap
            $this->walker->coords = $this->board->getCoords($this->walker->number);
        }

        // finalize (all matrix solved except placing zero)
        if ($this->board->getLastPositionedNumber() >= $this->board->getWidth() * ($this->board->getHeight()) - 1
            || $this->board->getLastPositionedNumber() === $this->board->getWidth() * ($this->board->getHeight() - 1) - 1) {
            // Move zero to the correct (right bottom corner)
            $this->pathfinder->moveZeroTo($this->board->getCorrectCoords(0), $this->allowed);

            if ($this->board->getLastPositionedNumber() === 0) {
                $this->result = 'solved';
            } else {
                $this->result = 'unsolvable';
            }

        }

    }

    private function getNextWalkerNumber(): int
    {
        $lastPositionedNumber = $this->board->getLastPositionedNumber();

        $nextWalkerNumber = $lastPositionedNumber + 1;

        // if last positioned number is second last col number (3)
        if ($this->board->isSecondLastColNumber($lastPositionedNumber)) {
            // then check the last col number (4) position
            // and if it's on the preposition
            if ($this->board->getCoords($lastPositionedNumber + 1) === $this->getLastColPreposition($lastPositionedNumber + 1)) {
                // then set the second last (already positioned) as walker
                // for placing it's to the corner (last)
                $nextWalkerNumber = $lastPositionedNumber;
            }
        }

        // if last positioned is previous before second last col (2)
        if ($this->board->isSecondLastColNumber($lastPositionedNumber + 1)) {
            // and the last (4) on preposition
            if ($this->board->getCoords($lastPositionedNumber + 2) === $this->getLastColPreposition($lastPositionedNumber + 2)
                // and the second last col (3) already placed to the corner
                && $this->board->getCoords($lastPositionedNumber + 1) === $this->board->getCorrectCoords($lastPositionedNumber + 2)) {
                // then set the last as walker
                $nextWalkerNumber = $lastPositionedNumber + 2;
            }
        }

        // ****** TWO LAST ROWS *******
        // if last positioned is previous before second last row (8)
        if ($this->board->isSecondLastRowNumber($lastPositionedNumber + 1)) {
            // and the last row (13) on preposition
            if ($this->board->getCoords($lastPositionedNumber + 1 + $this->board->getWidth()) === $this->getLastRowPreposition($lastPositionedNumber + 1 + $this->board->getWidth())
                // and the second last row (9) already placed to the corner
                && $this->board->getCoords($lastPositionedNumber + 1) === $this->board->getCorrectCoords($lastPositionedNumber + 1 + $this->board->getWidth())) {
                // then set the last as walker
                $nextWalkerNumber = $lastPositionedNumber + 1 + $this->board->getWidth();
            } else {
                $nextWalkerNumber = $lastPositionedNumber + 1;
            }
        }


        // if last positioned number is second last row number (9)
        if ($this->board->isSecondLastRowNumber($lastPositionedNumber)) {
            // then check the last row number (13) position
            // and if it's on the preposition
            if ($this->board->getCoords($lastPositionedNumber + $this->board->getWidth())
                === $this->getLastRowPreposition($lastPositionedNumber + $this->board->getWidth())) {
                // then set the second last (already positioned) as walker
                // for placing it's to the corner (last)
                $nextWalkerNumber = $lastPositionedNumber;
            } elseif ($this->board->getCoords($lastPositionedNumber + $this->board->getWidth())
                !== $this->board->getCorrectCoords($lastPositionedNumber + $this->board->getWidth())) {
                $nextWalkerNumber = $lastPositionedNumber + $this->board->getWidth();
            }
        }

        // if last positioned number is last row number (13)
        if ($this->board->isLastRowNumber($lastPositionedNumber)) {
            // if next second last row (10) is on preposition
            if ($this->board->getCoords($lastPositionedNumber - $this->board->getWidth() + 1) === $this->board->getCorrectCoords($lastPositionedNumber + 1)
                // and if next last row (14) is on preposition
                && $this->board->getCoords($lastPositionedNumber + 1) === $this->board->getCorrectCoords($lastPositionedNumber + 3)) {
                // then set the last row (already positioned) as walker
                // for placing both positioned tiles to their solved position
                $nextWalkerNumber = $lastPositionedNumber + 1;
            } else {
                $nextWalkerNumber = $lastPositionedNumber - $this->board->getWidth() + 1;
            }
        }

        return $nextWalkerNumber;
    }

    private function getWalkerTarget(): array
    {
        $targetCoords = $this->walker->solvedCoords;

        // if walker is last col
        if ($this->board->isLastColNumber($this->walker->number)) {
            // and the second last on solved
            if ($this->board->isCorrectCoords($this->walker->number - 1)) {
                // considering locking zero into the corner case
                // if zero into the corner
                if ($this->board->getNumber($this->walker->solvedCoords) === 0
                    // and the walker right under it
                    && $this->walker->coords === $this->board->getCorrectCoords($this->walker->number + $this->board->getWidth())) {
                    // then swap walker and zero
                    $targetCoords = $this->walker->solvedCoords;
                } else {
                    // then move walker (last) to preposition
                    $targetCoords = $this->getLastColPreposition();
                }
            }
        }

        // if walker is second last col
        if ($this->board->isSecondLastColNumber($this->walker->number)) {
            // and the last on preposition,
            if ($this->board->getCoords($this->walker->number + 1)
                === $this->getLastColPreposition($this->walker->number + 1)) {
                // then move walker (second last) to the corner (last)
                $targetCoords = [$this->walker->solvedCoords[0], $this->walker->solvedCoords[1] + 1];
            }
        }

        // if walker is last row
        if ($this->board->isLastRowNumber($this->walker->number)) {
            // and the second last on solved
            if ($this->board->isCorrectCoords($this->walker->number - $this->board->getWidth())) {
                // considering locking zero into the corner case
                // if zero into the corner
                if ($this->board->getNumber($this->walker->solvedCoords) === 0
                    // and the walker right next to it
                    && $this->walker->coords === $this->board->getCorrectCoords($this->walker->number + 1)) {
                    // then swap walker and zero
                    $targetCoords = $this->walker->solvedCoords;
                } else {
                    // then move walker (last) to preposition
                    $targetCoords = $this->getLastRowPreposition();
                }

            }
        }

        // if walker is second last row (9)
        if ($this->board->isSecondLastRowNumber($this->walker->number)) {
            // and the last row (13) on preposition,
            if ($this->board->getCoords($this->walker->number + $this->board->getWidth())
                === $this->getLastRowPreposition($this->walker->number + $this->board->getWidth())) {
                // then move walker (second last) to the corner (last)
                $targetCoords = [$this->walker->solvedCoords[0] + 1, $this->walker->solvedCoords[1]];
            }
        }

        return $targetCoords;
    }

    private function getWalkerNextStepCoords(): array
    {
        $walkerNextStepCoords = [];

        if ($this->walker->firstMoveMode === 'horizontal') {
            if ($this->walker->coords[1] < $this->walker->targetCoords[1]) {
                $walkerNextStepCoords = [$this->walker->coords[0], $this->walker->coords[1] + 1]; // right
            } elseif ($this->walker->coords[1] > $this->walker->targetCoords[1]) {
                $walkerNextStepCoords = [$this->walker->coords[0], $this->walker->coords[1] - 1]; // left
            } elseif ($this->walker->coords[0] > $this->walker->targetCoords[0]) {
                $walkerNextStepCoords = [$this->walker->coords[0] - 1, $this->walker->coords[1]]; // up
            } elseif ($this->walker->coords[0] < $this->walker->targetCoords[0]) {
                $walkerNextStepCoords = [$this->walker->coords[0] + 1, $this->walker->coords[1]]; // down
            }
        }

        if ($this->walker->firstMoveMode === 'vertical') {
            if ($this->walker->coords[0] < $this->walker->targetCoords[0]) {
                $walkerNextStepCoords = [$this->walker->coords[0] + 1, $this->walker->coords[1]]; // down
            } elseif ($this->walker->coords[0] > $this->walker->targetCoords[0]) {
                $walkerNextStepCoords = [$this->walker->coords[0] - 1, $this->walker->coords[1]]; // up
            } elseif ($this->walker->coords[1] > $this->walker->targetCoords[1]) {
                $walkerNextStepCoords = [$this->walker->coords[0], $this->walker->coords[1] - 1]; // left
            } elseif ($this->walker->coords[1] < $this->walker->targetCoords[1]) {
                $walkerNextStepCoords = [$this->walker->coords[0], $this->walker->coords[1] + 1]; // right
            }
        }

        return $walkerNextStepCoords;
    }


    private function swapZeroAndWalker()
    {
        $this->board->stepZeroTo($this->walker->coords);
    }

    private function setAllowed()
    {
        $this->allowed = range(0, $this->board->getWidth() * $this->board->getHeight() - 1);

        // block all continually positioned
        foreach ($this->allowed as $number) {
            if ($number > $this->board->getWidth() * ($this->board->getHeight() - 2)) {
                break;
            }

            if ($number <= $this->board->getLastPositionedNumber()) {
                $this->blockNumbers($number);
            } else {
                break;
            }
        }

        // last COLUMN permutation
        // if this walker is second last col (3) and it's on solved position and last col (4) is prepositioned then block last col (4) too
        if ($this->board->isSecondLastColNumber($this->walker->number)
            && $this->walker->coords === $this->walker->solvedCoords
            && $this->board->getCoords($this->walker->number + 1)
            === $this->board->getCorrectCoords($this->walker->number + 1 + $this->board->getWidth() * 2)
        ) {
            $this->blockNumbers($this->walker->number + 1);
        }

        // if this walker is last col (4) and it's prepositioned and second last col (3) is prepositioned too
        // then block second last col (3) to avoid it's replacing
        if ($this->board->isLastColNumber($this->walker->number)
            && $this->board->getCoords($this->walker->number - 1)
            === [$this->board->getCorrectCoords($this->walker->number - 1)[0], $this->board->getCorrectCoords($this->walker->number - 1)[1] + 1]
            && $this->walker->coords === [$this->walker->solvedCoords[0] + 2, $this->walker->solvedCoords[1]]
        ) {
            $this->blockNumbers($this->walker->number - 1);
        }

        // last ROW permutation
        // if this walker is second last row (9)
        if ($this->board->isSecondLastRowNumber($this->walker->number)
            // and it's on solved position
            && $this->walker->coords === $this->walker->solvedCoords
            // and last row (13) is prepositioned
            && $this->board->getCoords($this->walker->number + $this->board->getWidth())
            === $this->board->getCorrectCoords($this->walker->number + $this->board->getWidth() + 2)) {
            // then block last row (13) too
            $this->blockNumbers($this->walker->number + $this->board->getWidth());
        }

        // if this walker is last row (13)
        if ($this->board->isLastRowNumber($this->walker->number)
            // and it's prepositioned
            && $this->walker->coords === [$this->walker->solvedCoords[0], $this->walker->solvedCoords[1] + 2]
            // and second last row (9) is prepositioned too
            && $this->board->getCoords($this->walker->number - $this->board->getWidth())
            === $this->walker->solvedCoords) {
            // then block second last row (9) to avoid it's replacing
            $this->blockNumbers($this->walker->number - $this->board->getWidth());
        }

        $this->blockNumbers($this->walker->number);
    }

    private function blockNumbers(...$numbers)
    {
        foreach ($numbers as $number) {
            unset($this->allowed[$number]);
        }
    }

    private function getLastColPreposition(int $number = null): array
    {
        $number = $number ? $number : $this->walker->number;

        return [$this->board->getCorrectCoords($number)[0] + 2, $this->board->getCorrectCoords($number)[1]];
    }

    private function getLastRowPreposition(int $number = null): array
    {
        $number = $number ? $number : $this->walker->number;

        return [$this->board->getCorrectCoords($number)[0], $this->board->getCorrectCoords($number)[1] + 2];
    }


}

class Pathfinder
{
    private $board;
    public $zero;
    private $allowed = [];

    public function __construct(Board $board)
    {
        $this->board = $board;
        $this->zero = new Tile();
    }

    public function moveZeroTo(array $targetCoords, array $allowed)
    {
        $this->allowed = $allowed;

        while (true) {
            // Get zero
            $this->zero->coords = $this->board->getCoords(0);
            $this->zero->targetCoords = $targetCoords;

            // *** EXIT ***
            if ($this->zero->coords === $this->zero->targetCoords) {
                break;
            }

            // Get zero next step coords
            $this->zero->nextStepCoords = $this->getZeroNextStepCoords();

            // Get zero first move mode
            $this->zero->firstMoveMode = $this->getZeroFirstMoveMode();

            // Step zero to next
            $this->board->stepZeroTo($this->zero->nextStepCoords);
        }
    }

    private function getZeroNextStepCoords(): array
    {
        $zeroNextStepCoords = [];
        $stepTryingOrder = $this->getStepTryingOrder();

        foreach ($stepTryingOrder as $tryingDirection) {

            $stepTryingCoords = $this->getCoordsByDirection($tryingDirection);
            $stepTryingNumber = $this->board->getNumber($stepTryingCoords);

            if (in_array($stepTryingNumber, $this->allowed)) {
                $zeroNextStepCoords = $stepTryingCoords;
                break;
            }
        }


        return $zeroNextStepCoords;
    }

    private function getStepTryingOrder(): array
    {
        $stepTryingOrder = [];
        $zeroRow = $this->zero->coords[0];
        $zeroCol = $this->zero->coords[1];
        $targetRow = $this->zero->targetCoords[0];
        $targetCol = $this->zero->targetCoords[1];

        if ($zeroRow > $targetRow && $zeroCol === $targetCol) {
            $stepTryingOrder = ['up', 'right', 'left', 'down']; // up
        }

        if ($zeroRow === $targetRow && $zeroCol < $targetCol) {
            $stepTryingOrder = ['right', 'down', 'up', 'left']; // right
        }

        if ($zeroRow < $targetRow && $zeroCol === $targetCol) {
            $stepTryingOrder = ['down', 'right', 'left', 'up']; // down
        }

        if ($zeroRow === $targetRow && $zeroCol > $targetCol) {
            $stepTryingOrder = ['left', 'down', 'up', 'right']; // left
        }

        if ($zeroRow > $targetRow && $zeroCol < $targetCol) {
            if ($this->zero->firstMoveMode === 'horizontal') {
                $stepTryingOrder = ['right', 'up', 'left', 'down']; // right-up
            } elseif ($this->zero->firstMoveMode === 'vertical') {
                $stepTryingOrder = ['up', 'right', 'down', 'left']; // up-right
            }
        }

        if ($zeroRow < $targetRow && $zeroCol < $targetCol) {
            if ($this->zero->firstMoveMode === 'horizontal') {
                $stepTryingOrder = ['right', 'down', 'left', 'up']; // right-down
            } elseif ($this->zero->firstMoveMode === 'vertical') {
                $stepTryingOrder = ['down', 'right', 'up', 'left']; // 'down-right'
            }
        }

        if ($zeroRow < $targetRow && $zeroCol > $targetCol) {
            if ($this->zero->firstMoveMode === 'horizontal') {
                $stepTryingOrder = ['left', 'down', 'right', 'up']; // left-down
            } elseif ($this->zero->firstMoveMode === 'vertical') {
                $stepTryingOrder = ['down', 'left', 'up', 'right']; // 'down-left'
            }

        }

        if ($zeroRow > $targetRow && $zeroCol > $targetCol) {
            if ($this->zero->firstMoveMode === 'horizontal') {
                $stepTryingOrder = ['left', 'up', 'right', 'down']; // left-up
            } elseif ($this->zero->firstMoveMode === 'vertical') {
                $stepTryingOrder = ['up', 'left', 'down', 'right']; // 'up-left'
            }
        }

        return $stepTryingOrder;
    }

    private function getCoordsByDirection(string $direction): array
    {
        $coords = [];

        if ($direction === 'right') {
            $coords = [$this->zero->coords[0], $this->zero->coords[1] + 1];
        } elseif ($direction === 'left') {
            $coords = [$this->zero->coords[0], $this->zero->coords[1] - 1];
        } elseif ($direction === 'up') {
            $coords = [$this->zero->coords[0] - 1, $this->zero->coords[1]];
        } elseif ($direction === 'down') {
            $coords = [$this->zero->coords[0] + 1, $this->zero->coords[1]];
        }

        return $coords;
    }

    private function getZeroFirstMoveMode(): string
    {
        if ($this->zero->nextStepCoords === $this->getCoordsByDirection('right')
            || $this->zero->nextStepCoords === $this->getCoordsByDirection('left')) {
            $zeroFirstMoveMode = 'vertical';
        } elseif ($this->zero->nextStepCoords === $this->getCoordsByDirection('up')
            || $this->zero->nextStepCoords === $this->getCoordsByDirection('down')) {
            $zeroFirstMoveMode = 'horizontal';
        } else {
            // TODO Exception
            die(__METHOD__);
        }

        return $zeroFirstMoveMode;
    }

}

class Board
{
    private $width;
    private $height;
    private $matrix;
    public $movedNumbers;

    public function __construct(array $matrix)
    {
        $this->matrix = $matrix;

        $this->width = count($this->matrix[0]);
        $this->height = count($this->matrix);
    }

    public function getHeight(): int
    {
        return $this->height;
    }

    public function getWidth(): int
    {
        return $this->width;
    }

    public function getSolved(): array
    {
        $solved = [];

        // for upper rows except two nearest
        for ($r = 0; $r <= $this->height - 3; $r++) {
            for ($c = 0; $c <= $this->width - 1; $c++) {
                if ($this->getCorrectCoords($this->matrix[$r][$c]) === [$r, $c]) {
                    $solved[] = $this->matrix[$r][$c];
                } else {
                    return $solved;
                }
            }
        }

        // for two last rows
        for ($c = 0; $c <= $this->width - 1; $c++) {
            for ($r = $this->height - 2; $r <= $this->height - 1; $r++) {
                if ($this->getCorrectCoords($this->matrix[$r][$c]) === [$r, $c]) {
                    $solved[] = $this->matrix[$r][$c];
                } else {
                    break 2;
                }
            }
        }

        return $solved;
    }

    public function getLastPositionedNumber(): int
    {
        $positioned = $this->getSolved();

        if (count($positioned) < 1) {
            $lastPositioned = 0;
        } else {
            $lastPositioned = $positioned[count($positioned) - 1];
        }

        return $lastPositioned;
    }

    public function isCorrectCoords(int $number): bool
    {
        return $this->getCoords($number) === $this->getCorrectCoords($number);
    }

    public function getCorrectCoords(int $number): array
    {
        if ($number === 0) {
            $correctCoords = [$this->height - 1, $this->width - 1];
        } else {
            $correctCoords = [(int)(($number - 1) / $this->width), (int)(($number - 1) % $this->width)];
        }

        return $correctCoords;
    }

    public function getCoords(int $number): array
    {
        $coords = [];
        foreach ($this->matrix as $r => $row) {
            foreach ($row as $c => $n) {
                if ($n === $number) {
                    $coords = [$r, $c];
                    break 2;
                }
            }
        }

        return $coords;
    }

    private function setNumber(int $number, array $coords)
    {
        $maxNumber = $this->width * $this->height - 1;
        if (0 <= $number || $number <= $maxNumber) {
            $this->matrix[$coords[0]][$coords[1]] = $number;
        } else {
            // TODO make exception
            die('Try to set out of range number value!');
        }
    }

    public function getNumber(array $coords): int
    {
        if ($coords[0] < 0 || ($this->height - 1) < $coords[0]) {
            return -1;
        }

        if ($coords[1] < 0 || ($this->width - 1) < $coords[1]) {
            return -1;
        }

        return $this->matrix[$coords[0]][$coords[1]];
    }

    public function isSecondLastColNumber(int $number): bool
    {
        return $this->getCorrectCoords($number)[1] === $this->width - 2;
    }

    public function isLastColNumber(int $number): bool
    {
        return $this->getCorrectCoords($number)[1] === $this->width - 1;
    }

    public function isSecondLastRowNumber(int $number): bool
    {
        return $this->getCorrectCoords($number)[0] === $this->height - 2;
    }

    public function isLastRowNumber(int $number): bool
    {
        if ($number === 0) {
            return false;
        }

        return $this->getCorrectCoords($number)[0] === $this->height - 1;
    }

    public function stepZeroTo(array $nextZeroStepCoords)
    {
        $nextZeroStepNumber = $this->getNumber($nextZeroStepCoords);
        $zeroCoords = $this->getCoords(0);
        $this->setNumber($nextZeroStepNumber, $zeroCoords);
        $this->setNumber(0, $nextZeroStepCoords);
        $this->movedNumbers[] = $nextZeroStepNumber;
    }

}

class Tile
{
    public $number = -1;
    public $coords = [];
    public $solvedCoords = [];
    public $targetCoords = [];
    public $nextStepCoords = [];
    public $firstMoveMode = 'horizontal';

}
_________________________________________
/*
 * An attempt to design a simple, concise algorithm,
 * rather than an algorithm that generates an efficient solution.
 *
 * @param {number[][]} arr
 * @return {number[]|null}
 */
function slidePuzzle($arr) {
    $moves = [];
    $n = count($arr);
    $m = $n;
    $list = array_merge(...$arr);

    // Functions to do basic indexing.
    $col = function ($tile) use (&$list, &$m) { return array_search($tile, $list) % $m; };
    $row = function ($tile) use (&$list, &$m) { return intval(array_search($tile, $list)/$m); };
    // Functions to move the empty slot to a neighboring position.
    $shift = function ($offset, $count) use (&$list, &$moves) {
        $j = array_search(0, $list);
        $offset *= ($count < 0 ? -1 : 1);
        for ($count = abs($count); $count > 0; $count -= 1) {
            $moves[] = $list[$j] = $list[$j + $offset];
            $list[$j = $j + $offset] = 0;
        }
    };
    $right = function ($d = 1) use (&$shift) { $shift(1, $d); };
    $left = function ($d = 1) use (&$shift) { $shift(-1, $d); };
    $down = function ($d = 1) use (&$shift, &$m) { $shift($m, $d); };
    $up = function ($d = 1) use (&$shift, &$m) { $shift(-$m, $d); };
    // Function to move the empty slot around a rectangle.
    $box = function ($w, $h = 0) use (&$right, &$left, &$up, &$down) {
        $down(($h ?: $w) - 1); $left($w); $up($h ?: $w); $right($w); $down();
    };

    // On each level, we solve the top row and left column.
    for ($level = 0; $level < $n - 2; $level += 1) {
        // Ensure standard starting position.
        $down(1 - $row(0));
        $right($m - 1 - $col(0));

        // Start by loading some "safe" tiles into the top row - ones we won't
        // use on this level.  The paths traversed here are long enough
        // that we will always be able to find suitable tiles.
        for ($j = 0; $j < $m; $j += 1) {
            if ($j !== $m - 1 || $list[0] <= $n*$level + $n || $list[0] % $n === $level + 1) {
                $down();
                while ($list[2*$m - 1] <= $n*$level + $n || $list[2*$m - 1] % $n === $level + 1) {
                    $left($m - 1); $up(2);
                    $right($m - 1 - $j); $down(); $right($j); $down();
                }
                $up(); $box($m - 1, 2);
            }
        }

        // We have 2*m - 1 tiles to position for this level.
        for ($j = -$m + 1; $j < $m; $j += 1) {
            // This is the tile we want to position next.
            $subject = ($n + 1)*$level + 1 + ($j < 0 ? -$n*$j : $j);

            // Position this tile to be next in line.
            if (array_search($subject, $list) !== array_search(0, $list) + $m) {
                $down($row($subject) - $row(0));
                if ($col($subject) !== $m - 1) {
                    $left($col(0) - $col($subject));
                    if ($row($subject) === $m - 1) {
                        $up(); $right(); $down(); $left(); $up();
                    }
                    for ($k = $m - 1 - $col($subject); $k > 0; $k -= 1) {
                        $down(); $right(2); $up(); $left();
                    }
                    $down(); $right();
                }
                for ($k = $row($subject) - 1; $k > 0; $k -= 1) {
                    $left(); $up(2); $right(); $down();
                }
                $up();
            }

            // March around the edges to shift the tiles by one position.
            $box($m - 1);
        }

        // Remove the completed row and column for the next iteration level.
        $m -= 1;
        $list = array_slice($list, $m + 2);
        for ($j = 0; $j < $m - 1; $j += 1) {
            array_splice($list, ($j + 1)*$m, 1);
        }
    }

    // We are left with a 2x2 array to solve and check.
    $down();
    while($list[0] !== $n*$n - $n - 1) {
        $box(1, 1);
    }
    return ($list[2] === $n*$n - 1 ? $moves : null);
}
