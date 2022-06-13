function bouncingBall($h, $bounce, $window) {
  if($h <= 0 || $window <= 0 || $h <= $window || $bounce >= 1 || $bounce <= 0) {
    return -1;
  }
  
  return bouncingBall($h * $bounce, $bounce, $window) + 2;
}
_______________________________________________
function bouncingBall($h, $bounce, $window) {
    $bounds = -1;
    if ($bounce > 0 && $bounce < 1) {
        while ($h > $window) {
            $bounds += 2; $h *= $bounce;
        }
    }
    return $bounds;
}
_______________________________________________
function bouncingBall($h, $bounce, $window) {
      // first test all math improper conditions
    if($window>=$h || $bounce>=1 || $bounce<=0) return -1;
      // geometrical row for height:
      // n-th jump hight is an = a1 * bounce ^ (n-1)
      // so log(an/a1) = log(bounce) * (n-1)
      // ... and so we count when height will be at least window:
    $n = log($window/$h+1e-6)/log($bounce) + 1;
      // (that special 1um is because alg. is otherwise OK with height equal to window height)
      // and ball passes twice for every peak (up+down), except first time (just down)
    return 2*floor($n) - 1;
}
_______________________________________________
function bouncingBall($h, $bounce, $window) {
    $ct = 1;
    if ($h > 0 && $window < $h && $bounce > 0 && $bounce < 1) {
        while($bounce * $h > $window){
        $ct += 2;
        $h *= $bounce;
    }
      return $ct;
    } else {
    return -1;
    }
}

echo bouncingBall (3.0, 0.66, 1.5);
