561e9c843a2ef5a40c0000a4


function isPrime($n) {
    if ($n === 1) {
        return false;
    }
    if ($n === 2) {
        return true;
    }
    if ($n % 2 === 0) {
        return false;
    }
    $upperBound = ceil(sqrt($n));
    for ($i = 3; $i <= $upperBound; $i = $i + 2) {
        if ($n % $i === 0) {
            return false;
        }
    }
    return true;
}

function gap($g, $m, $n) {
    $previousPrime = null;
    for ($i = $m; $i <= $n; $i += 1) {
        if (isPrime($i)) {
            if ($previousPrime !== null && $i - $previousPrime === $g) {
                return [ $previousPrime, $i ];
            }
            $previousPrime = $i;
        }
    }
    return null;
}
__________________________________
function gap($g, $m, $n) {
    $previousPrime = null;
    for ($i = $m; $i <= $n; $i++) {
      if (isPrime($i)){
        if ($previousPrime && $i - $previousPrime == $g){
          return [$previousPrime, $i];
        }
        $previousPrime = $i;
      }
    } 
    return null;
}

function isPrime ($number){
    $testLimit = floor(sqrt($number));
    $prime = true;
    for ($i = 2; $i<=$testLimit; $i++){
      if($number % $i == 0){
        $prime = false;
        break;
      }
    }
    if ($prime)
      return true;
    return false;
}
__________________________________
function gap($g, $m, $n) {
    // your code
    $previous = 0;
    
    while($m++ <= $n) {
        if (is_prime($m)) {
            if (abs($previous - $m) == $g) {
                return [$previous, $m];
                break;
            }
            $previous = $m;
        }
    }
    
    return NULL;
}

function is_prime($number) 
{
    $n = abs($number);
    $i = 2;
    while ($i <= sqrt($n))
    {
        if ($n % $i == 0) {
            return false;
        }
        $i++;
    }
    return true;
}
