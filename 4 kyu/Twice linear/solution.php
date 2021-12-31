function dblLinear($n) {
    $h = 1; $cnt = 0; $q2 = array(); $q3 = array();
    while (true) {
        if ($cnt >= $n) {
            return $h;
        }
        array_push($q2, 2 * $h + 1);
        array_push($q3, 3 * $h + 1);
        $h = min($q2[0], $q3[0]);
        if ($h === $q2[0]) {
            $h = array_shift($q2);
        }
        if ($h === $q3[0]) {
            $h = array_shift($q3);
        }
        $cnt++;
    }
}

__________________________________________________
function dblLinear(int $n): int {
  foreach (genU() as $i => $v) {
    if ($i == $n) { 
      return $v;
    }
  } 
}

function genU(): Generator {
  $u = new SplMinHeap();

  $x = 1;
  $u->insert($x);

  while (true) { 
    $u->insert(2 * $x + 1);
    $u->insert(3 * $x + 1);

    yield $x;

    do {
      $u->next();
      $newX = $u->current();
    } while ($newX == $x);

    $x = $newX;
  }
}

__________________________________________________
function numberIsInSequence($n) {
    if ($n < 1 || $n != intval($n)) {
        return false;
    } else if ($n === 1) {
        return true;
    } else if ($n % 2 === 0) {
        return numberIsInSequence(($n-1)/3);
    } else {
        return numberIsInSequence(($n-1)/2) || numberIsInSequence(($n-1)/3);
    }
}

function dblLinear($n) {
    $position = 1;
    $i = 1;
    while($position <= $n) {
        $i++;
        if (numberIsInSequence($i))
            $position++;
    }
    return $i;
}
