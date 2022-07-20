54d496788776e49e6b00052f


function sumOfDivided($lst) {
    $result = [];
    foreach ($lst as $number) {
        for ($i = 2; $i <= abs($number); $i++) {
            if ($number % $i == 0) {
                $prime = true;
                for ($j = 2; $j < $i; $j++) {
                    if ($i % $j == 0) {
                        $prime = false;
                        break;
                    }
                }
                if ($prime) $result[$i] = isset($result[$i]) ? $result[$i]+$number : $number;
            }
        }
    }
    
    ksort($result);
    return array_map(function($k, $v){
        return [$k, $v];
    }, array_keys($result), array_values($result));
}
________________________________________________
function is_prime($n)
{
    $divisors =[];

    for($i = 2; $i <= sqrt($n); $i++)
    {
        if($n%$i == 0)
        {
            return false;
        }
    }

    return true;
}


function sumOfDivided($lst)
{
    $lst1 = $lst;
    $lst =  array_map('abs',$lst);

    sort($lst);
    $prime_factors =[];
    $prime_numbers =[];

    for($i = 2; $i <= $lst[count($lst)-1] ; $i++)
    {
        if(is_prime($i))
        {
            $prime_numbers[] = $i;
        }
    }
    
    foreach($prime_numbers as $n => $p )
    {
        foreach($lst as $k => $l)
        {
            if($l%$p == 0 && !in_array($p,$prime_factors))
            {
                $prime_factors[]=$p;
            }
        }
    }

    $sum_by_factors =[];

    foreach($prime_factors as $p)
    {
        $divisors =[];

        foreach($lst1 as $l)
        {
            if($l%$p == 0)
            {
                $divisors[] = $l;
            }
        }

        $sum_by_factors[] = [$p,array_sum($divisors)];
    }

    return $sum_by_factors;
}
________________________________________________
function sumOfDivided($lst) {
    if (!is_array($lst) || empty($lst)) return array();

    $max = max(max($lst), abs(min($lst)));
    
    //get primes
    $sqrtmax = (int)sqrt($max);
    $primes[2] = true;
    for ($i = 3; $i <= $max; $i+=2) {
      $primes[$i] = true;
    }
    
    for($i = 3; $i <= $sqrtmax; $i+=2) {
      $z = 2;
      while($z*$i <=$max) {
        unset($primes[$i*$z]);
        $z++;
      }
    }
  

    foreach($primes as $prime => $true) {
      $isdivided = 0;
      $result = 0;
      foreach($lst as $num) {
        if ($num%$prime == 0) {
          $isdivided = 1;
          $result+=$num;
        }
      }
      if ($isdivided) {
        $return[]=[$prime, $result];
      }
    }

  return $return;
  
}
