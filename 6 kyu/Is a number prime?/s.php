function is_prime(int $n): bool {
  if ($n <= 1) {
    return false;
  }

  for ($i = 2; $i <= sqrt($n); $i++) {
    if ($n % $i === 0) {
      return false;
    }
  }
  
  return true;
}
_____________________________
function is_prime(int $n): bool 
{
  if ($n <= 1) 
  {
    return false; // 1, 0, and negative numbers are not prime
  }

  for ($i = 2; $i <= sqrt($n); $i++)
  {
    if($n % $i == 0)
    {
      return false; // n is divisible by i, so it's not prime
    }
  }

  return true; // n is prime
}
_____________________________
function is_prime(int $n): bool {
  
    // I numeri negativi, 0 e 1 non sono primi
    if ($n <= 1) {
        return false;
    }

    // 2 è l'unico numero pari primo
    if ($n == 2) {
        return true;
    }

    // Tutti gli altri numeri pari non sono primi
    if ($n % 2 == 0) {
        return false;
    }

    // Verifica divisori fino alla radice quadrata di $n
    for ($i = 3; $i * $i <= $n; $i += 2) {
        if ($n % $i == 0) {
            return false;
        }
    }

    return true;
}
