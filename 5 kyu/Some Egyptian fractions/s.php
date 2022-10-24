54f8693ea58bce689100065f


function decompose($n) {
  $ans = [];
  $xs = explode("/", $n);
  $a = doubleval(0);
  $b = doubleval(1);
  if (count($xs) == 1) {
    $a = doubleval($n);
  } else {
    $a = doubleval($xs[0]);
    $b = doubleval($xs[1]);
  }
  while (($a - floor($a)) > 0) {
    $a *= 10;
    $b *= 10;
  }
  while ($a >= $b) {
    $d = doubleval(intdiv($a, $b));
    $s = strval($d);
    array_push($ans, $s);
    $a %= $b;
  }
  while ($a > 0) {
    $d = ceil($b / $a);
    $s = "1/" . strval($d);
    array_push($ans, $s);
    $a = $a * $d - $b;
    $b *= $d;
  }
  return $ans;
}
_________________________________
function decompose($n)
{
    if ($n == 0) {
        return [];
    }
    if (preg_match('|^\d+$|', $n)) {
        return [$n];
    }
    if (!preg_match('|(\d+)([/\.])(\d+)|', $n, $matches)) {
        return 'error: wrong format';
    }
    if ($matches[2] === '/') {
        $a = (int)$matches[1];
        $b = (int)$matches[3];
    } else {
        $a = (int)($matches[1] . $matches[3]);
        $b = 10 ** strlen($matches[3]);
    }

    $result = [];
    if ($a >= $b) {
        $whole = floor($a / $b);
        $a = $a - $whole * $b;
        $result[] = (string)$whole;
    }
    while ($a != 0) {
        $x = ceil($b / $a);
        $result[] = "1/$x";
        $a = $a * $x - $b;
        $b = $b * $x;
    }
    return $result;
}
_________________________________
function decompose($n) {
    if ($n == "0") return [];
    $res = []; $a = -1; $b = -1;
    $p = strpos($n, "/");
    if ($p == true) {
        $dec = explode("/", $n);
        $a = (float)($dec[0]);
        $b = (float)($dec[1]);
    } else {
        $p = strpos($n, ".");
        if ($p == true) {
            $a = (float)$n;
            $b = 1;
        }
    }
    while ($a != (int)$a) {
        $a = $a * 10;
        $b = $b * 10;
    }
    if ($a > $b) {
        array_push($res, strval($a / $b >> 0));
        $a %= $b;
    }
    while($a > 0) {
        $dv = ceil($b / $a);
        array_push($res, "1/".$dv);
        $a = $a * $dv - $b;
        $b = $b * $dv;
  }
  return $res;
}
