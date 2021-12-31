<?php

function sudoku(array $puzzle): array {
  $allNumbers = [1,2,3,4,5,6,7,8,9];

  $currentPositionXY = [-1,0];
  $counter = 0;
  $maxAllowed = pow(count($allNumbers),3);
  while($counter < $maxAllowed) {
    try {
      $currentPositionXY[0]  = findNextUnsetXPoint($puzzle[$currentPositionXY[1]], $currentPositionXY[0]);

    } catch (\Exception) {
        $currentPositionXY[1] = ($currentPositionXY[1]+1)% count($allNumbers);
        $currentPositionXY[0] = -1;
        $counter++;
        continue;
    }
    
    //get horizantal & vertical matches
    $hMatches = getPossibilities($puzzle[$currentPositionXY[1]]);
    $vMatches = getPossibilities(buildVerticalArray($puzzle,$currentPositionXY[0]));
    $sMatches = buildMySquare($puzzle, $currentPositionXY);

    $possibilities = array_values( array_intersect($hMatches, $vMatches, $sMatches));
    if(count($possibilities) === 1 ) {
        $puzzle[$currentPositionXY[1]][$currentPositionXY[0]] = $possibilities[0];
    }
    $counter++;
    
  }
  return $puzzle;
}


function buildMySquare(array $puzzle, array $coordinates, bool $debug = false) {
    $x = intdiv($coordinates[0], 3);
    $y=  intdiv($coordinates[1], 3);
    $square = [];

    for($i=0; $i<3; $i++) {
        $slicedPart = array_slice($puzzle[$i+$y*3],3*$x, 3);
        $square = array_merge($square, $slicedPart);
    }
    
    $square = array_diff(array_unique($square), [0]);
    return array_diff([1,2,3,4,5,6,7,8,9], $square);
}

function buildVerticalArray(array $puzzle, int $index) {
  $verticalArray= [];
  foreach($puzzle as $row) {
    $verticalArray[] = $row[$index];
  }
  return $verticalArray;
} 


function findNextUnsetXPoint(array $puzzleRow, int  $lastGotXIndex =-1){
  $matchIndex = -1;
  foreach($puzzleRow  as $index => $val) {
    if($val === 0 && $index > $lastGotXIndex) {
      $matchIndex = $index;
      break;
    }
  }
  
  return $matchIndex === -1 ? throw new Exception('nothing found') :  $matchIndex;
}

function getPossibilities (array $puzzle) {
    $allNumbers = [0,1,2,3,4,5,6,7,8,9];
    return array_values(array_diff( $allNumbers,$puzzle));
}

___________________________________________________
function findPossibleNumbers(array $puzzle, $y, $x): array
{
    $numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    $foundNumbers = [];
    //check the line
    for ($i = 0; $i < 9; $i++) {
        if ($puzzle[$y][$i] != 0) {
            $foundNumbers[] = $puzzle[$y][$i];
        }
    }
    //check the column
    for ($i = 0; $i < 9; $i++) {
        if ($puzzle[$i][$x] != 0) {
            $foundNumbers[] = $puzzle[$i][$x];
        }
    }
    //check the grid
    $y = intdiv($y, 3) * 3;
    $x = intdiv($x, 3) * 3;
    for ($i = 0; $i < 3; $i++) {
        for ($j = 0; $j < 3; $j++) {
            if ($puzzle[$y + $i][$x + $j] != 0) {
                $foundNumbers[] = $puzzle[$y + $i][$x + $j];
            }
        }
    }
    $possibleNumbers = array_diff($numbers, array_unique($foundNumbers));
    return array_values($possibleNumbers);
}

function sudoku(array $puzzle): array {
  do {
        $flag = 0;
        for ($y = 0; $y < 9; $y++) {
            for ($x = 0; $x < 9; $x++) {
                if ($puzzle[$y][$x] == 0) {
                    $temp =  findPossibleNumbers($puzzle, $y, $x);
                    if (count($temp) == 1) {
                        $puzzle[$y][$x] = $temp[0];
                        $flag++;
                    }
                } else {
                    $flag++;
                }
            }
        }
    } while ($flag < 81);

    return $puzzle;
}

___________________________________________________
function sudoku(array $puzzle): array {
  
  // Search a number for a item with $column and $row coordinates
  $search = function($puzzle, $column, $row) {
    
    // Get initial index for a row or column
    $getIndexes = function($number) {
      switch($number) {
        case 0:
        case 1:
        case 2:
          return 0;
        case 3:
        case 4:
        case 5:
          return 3;
        case 6:
        case 7:
        case 8:
          return 6;  

      }
      return false;
    };
    
    $possibilities = [];
    foreach (range(1, 9) as $possibility) {
    
      // Get squeare options
      $square_options = [];
      $column_start = $getIndexes($column);      
      $square_rows = array_slice($puzzle, $getIndexes($row), 3);
      array_walk($square_rows, function($item) use ($puzzle, $column_start, &$square_options) {
        $square_options = array_merge($square_options, array_slice($item, $column_start, 3));
      });
      
      // Check row, column and square for current possibility
      if (!in_array($possibility, $puzzle[$row]) && 
          !in_array($possibility, array_column($puzzle, $column)) && 
          !in_array($possibility, $square_options)) {
        $possibilities[] = $possibility;
      }
      // Check if there are more than one, to not overloop (performance). More than one possibility means we can not be sure of found number
      if (count($possibilities) > 1) {
        return 0;
      }
    }
    // If script reaches this, means we found the only one possibility for the current item in puzzle
    return $possibilities[0];
  };
  
  // Search until no zeros in puzzle array
  do {
    $not_success = false;
    foreach($puzzle as $row_index => $row) {
      foreach($row as $column_index => $value) {
        if ($value) {
          continue;
        }
        $not_success = true;
        $puzzle[$row_index][$column_index] = $search($puzzle, $column_index, $row_index) ?: 0;
      }
    }
  }
  while($not_success);
  
  return $puzzle;

}

___________________________________________________
function sudoku(array $puzzle): array
{
    do {
        $changed = false;
        $size = 9;
        $offset = 3;
        for ($i = 0; $i < $size; $i++) {
            for ($j = 0; $j < $size; $j++) {
                if ($puzzle[$i][$j]) {
                    continue;
                }
                $availibleValues = range(1, 9);
                $availibleValues = array_diff($availibleValues, $puzzle[$i]);
                $availibleValues = array_diff($availibleValues, array_column($puzzle, $j));
                $availibleValues = array_diff($availibleValues, array_merge(
                    array_slice($puzzle[(int)($i / $offset) * $offset], (int)($j / $offset) * $offset, $offset),
                    array_slice($puzzle[(int)($i / $offset) * $offset + 1], (int)($j / $offset) * $offset, $offset),
                    array_slice($puzzle[(int)($i / $offset) * $offset + 2], (int)($j / $offset) * $offset, $offset)
                ));
                if (count($availibleValues) === 1) {
                    $puzzle[$i][$j] = array_pop($availibleValues);
                    $changed = true;
                }
            }
        }
    } while ($changed);

    return $puzzle;
}
