function alphabet_position(string $s): string {
  
  $result = [];
  
  for ($i = 0; $i < strlen($s); $i++) {

    if (preg_match("/^[a-zA-Z]$/", $s[$i])) {
      $result[] = ord(strtolower($s[$i])) - ord('a') + 1;
    }
  }
  
  return join(' ', $result);
}
                               
________________________________________________
function alphabet_position(string $s): string {
  //THE BULLSHITIEST WAY TO DO THIS
  $s = strtolower($s);
  $s = str_replace(" ", "", $s);
  $s = str_replace(".", " ", $s);
  $s = str_replace(",", " ", $s);
  $s = str_replace("!", " ", $s);
  $s = str_replace("?", " ", $s);
  $s = str_replace("'", " ", $s);
  $s = str_replace("ß", " ", $s);
  $s = str_replace("§", " ", $s);
  $s = str_replace("$", " ", $s);
  $s = str_replace("%", " ", $s);
  $s = str_replace("&", " ", $s);
  $s = str_replace("/", " ", $s);
  $s = str_replace("(", " ", $s);
  $s = str_replace(")", " ", $s);
  $s = str_replace("=", " ", $s);
  $s = str_replace("@", " ", $s);
  $s = str_replace("-", " ", $s);
  $s = str_replace("_", " ", $s);
  $s = str_replace(";", " ", $s);
  $s = str_replace(":", " ", $s);
  $s = str_replace("+", " ", $s);
  $s = str_replace(">", " ", $s);
  $s = str_replace("<", " ", $s);
  $s = str_replace("#", " ", $s);
  $s = str_replace("^", " ", $s);
  $s = str_replace("*", " ", $s);
  $s = str_replace("1", " ", $s);
  $s = str_replace("2", " ", $s);
  $s = str_replace("3", " ", $s);
  $s = str_replace("4", " ", $s);
  $s = str_replace("5", " ", $s);
  $s = str_replace("6", " ", $s);
  $s = str_replace("7", " ", $s);
  $s = str_replace("8", " ", $s);
  $s = str_replace("9", " ", $s);
  $s = str_replace("0", " ", $s);
  $s = str_replace("a", " 1 ", $s);
  $s = str_replace("b", " 2 ", $s);
  $s = str_replace("c", " 3 ", $s);
  $s = str_replace("d", " 4 ", $s);
  $s = str_replace("e", " 5 ", $s);
  $s = str_replace("f", " 6 ", $s);
  $s = str_replace("g", " 7 ", $s);
  $s = str_replace("h", " 8 ", $s);
  $s = str_replace("i", " 9 ", $s);
  $s = str_replace("j", " 10 ", $s);
  $s = str_replace("k", " 11 ", $s);
  $s = str_replace("l", " 12 ", $s);
  $s = str_replace("m", " 13 ", $s);
  $s = str_replace("n", " 14 ", $s);
  $s = str_replace("o", " 15 ", $s);
  $s = str_replace("p", " 16 ", $s);
  $s = str_replace("q", " 17 ", $s);
  $s = str_replace("r", " 18 ", $s);
  $s = str_replace("s", " 19 ", $s);
  $s = str_replace("t", " 20 ", $s);
  $s = str_replace("u", " 21 ", $s);
  $s = str_replace("v", " 22 ", $s);
  $s = str_replace("w", " 23 ", $s);
  $s = str_replace("x", " 24 ", $s);
  $s = str_replace("y", " 25 ", $s);
  $s = str_replace("z", " 26 ", $s);
  $s = str_replace("  ", " ", $s);
  $s = str_replace("   ", " ", $s);
  $s = str_replace("  ", " ", $s);
  $s = trim($s);
  $s = str_replace("  ", " ", $s);
  return $s;
}
                               
________________________________________________
function alphabet_position(string $s):string {
  return implode(' ', array_filter(array_map(function($x){
    return array_search($x, str_split('_abcdefghijklmnopqrstuvwxyz'));}, str_split(strtolower($s)))));
}
                               
________________________________________________
function alphabet_position(string $s): string {
  preg_match_all('/[a-z]/', strtolower($s), $out);
  return join(' ', array_map(function($ch){return ord($ch) - 96;}, $out[0]));
}

