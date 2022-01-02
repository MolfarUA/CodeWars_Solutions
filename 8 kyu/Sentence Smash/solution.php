function smash(array $words): string {
  return implode(" ", $words);
}

_____________________________________
function smash(array $words): string {
   return join(' ', $words);
}

_____________________________________
function smash(array $words): string {
  return trim(implode(" ",$words));
}
