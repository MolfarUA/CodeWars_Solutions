class VigenèreCipher {
  private $key;
  private $alphabet;

  public function __construct($key, $alphabet)
  {
    $this->key = $key;
    $this->alphabet = $alphabet;
  }

  public function encode($text) 
  {
    $cipher = '';
    for ($i = 0; $i < strlen($text); $i++) {
      $cipher .= $this->encodeLetter($text[$i], $i);
    }
    
    return $cipher;
  }
  
  public function decode($cipher)
  {
    $text = '';
    for ($i = 0; $i < strlen($cipher); $i++) {
      $text .= $this->decodeLetter($cipher[$i], $i);
    }
    
    return $text;
  }
  
  private function encodeLetter($letter, $position)
  {
    return $this->shiftLetter($letter, $this->getKeyShiftAtPosition($position));
  }
  
  private function decodeLetter($letter, $position)
  {
    return $this->shiftLetter($letter, -$this->getKeyShiftAtPosition($position));
  }
  
  private function getKeyShiftAtPosition($position)
  {
    $keyLetter = $this->key[$position % strlen($this->key)];
    return strpos($this->alphabet, $keyLetter);
  }
  
  private function shiftLetter($letter, $shiftSize)
  {
    $pos = strpos($this->alphabet, $letter);
    if ($pos === false) {
      return $letter;
    }
  
    $length = strlen($this->alphabet);
    $cipherLetterPos = ($pos + $shiftSize + $length) % $length;
    return $this->alphabet[$cipherLetterPos];
  }
}
_____________________________________________
class VigenèreCipher {
  public $alph;
  public $key;
  
  public function __construct($key, $alphabet) {
    $this->alph = str_split($alphabet);
    $this->key = $key;
  }
  
  public function encode($s) {
    return $this->cipher($s, 'encode');
  }
  
  public function decode($s) {
    return $this->cipher($s, 'decode');
  }
  
  public function cipher($s, $dir) {
    $s = str_split($s);
    $a = $this->alph;
    $k = str_split(str_pad($this->key, count($s), $this->key));
    $result = '';
    for ($i = 0; $i < count($s); $i++) {
      $in = array_search($s[$i], $a);
      if (false !== $in) {
        $ci = array_search($k[$i], $a);
        $sum = ("encode" == $dir) ? $in + $ci : $in - $ci;
        $sum = ($sum < 0) ? count($a) + $sum : $sum;
        $sum = ($sum >= count($a)) ? $sum - count($a): $sum;
        $result .= $a[$sum];
      } else {
        $result .= $s[$i];
      }
    }
    
    return $result;
    
  }
}
_____________________________________________
class VigenèreCipher {
  function __construct($key, $alphabet) {
    $this->key = $key;
    $this->alphabet = $alphabet;
  }
  private function cipher($shifter, $text) {
    return implode('', array_map(function($ch, $i) use ($shifter, $text) {
      return (strpos($this->alphabet, $ch) !== false)
          ? $this->alphabet[($shifter * strpos($this->alphabet, $this->key[$i % strlen($this->key)]) + strpos($this->alphabet, $ch) + strlen($this->alphabet)) % strlen($this->alphabet)]
          : $ch;
    }, str_split($text), array_keys(str_split($text))));
  }
  
  public function encode($text) {
    return $this->cipher(1, $text);
  }
  public function decode($text) {
    return $this->cipher(-1, $text);
  }
}
_____________________________________________
class VigenèreCipher {
  private $key;
  private $alphabet;
  private $alphabetFlipepd;
  private $alphabetCount;
  
  public function __construct($key, $alphabet) {
    $this->key = str_split($key);
    $this->alphabet = str_split($alphabet);
    $this->alphabetFlipped = array_flip($this->alphabet);
    $this->alphabetCount = count($this->alphabet);
  }
  
  public function encode($s) {
    $return = '';
    
    foreach (str_split($s) as $position => $char) {
      if (!$this->isCharInAlphabet($char)) {
        $return .= $char;
        continue;
      }
      
      $return .= $this->offsetChar($this->charOffsetInAlphabet($char), $this->keyOffset($position));
    }
    
    return $return;
  }
  
  public function decode($s) {
    $return = '';
    
    foreach(str_split($s) as $position => $char) {
      if (!$this->isCharInAlphabet($char)) {
        $return .= $char;
        continue;
      }
      
      $return .= $this->offsetChar($this->charOffsetInAlphabet($char), -$this->keyOffset($position));
    }
    
    return $return;
  }
  
  private function isCharInAlphabet($char) {
    return isset($this->alphabetFlipped[$char]);
  }
  
  private function charOffsetInAlphabet($char) {
    return $this->alphabetFlipped[$char];
  }
  
  private function keyCharacterByPosition($position) {
    return $this->key[$position % count($this->key)];
  }
  
  private function keyOffset($position) {
    return $this->charOffsetInAlphabet($this->keyCharacterByPosition($position));
  }
  
  private function offsetChar($characterOffset, $keyOffset) {
    return $this->alphabet[($this->alphabetCount + $characterOffset + $keyOffset) % $this->alphabetCount];
  }
}
_____________________________________________
class VigenèreCipher {
  
  public $alphabet;
  public $key;
  
  function __construct($key, $alphabet)
  {
    $this->key = $key;
    $this->alphabet = $alphabet;
  }
  
  public function encode($s) 
  {
    $i = 0;
    $encoded = '';
    $key_len = strlen($this->key);
    $alphabet_len = strlen($this->alphabet);
    
    while ($s[$i] != '')
    {
      $index = strpos($this->alphabet, $s[$i]);
      if ($index !== false)
      {
        $index2 = strpos($this->alphabet, $this->key[$i % $key_len]) + $index;
        $encoded = $encoded.$this->alphabet[$index2 % $alphabet_len];
      }
      else
        $encoded = $encoded.$s[$i];
      $i++;
    }
    return ($encoded);
  }
  
  public function decode($s) 
  {
    $i = 0;
    $encoded = '';
    $key_len = strlen($this->key);
    $alphabet_len = strlen($this->alphabet);
    
    while ($s[$i] != '')
    {
      $index = strpos($this->alphabet, $s[$i]);
      if ($index !== false)
      {
        $index2 = $index - strpos($this->alphabet, $this->key[$i % $key_len]);
        $index2 = $index2 < 0 ? strpos($this->alphabet, $this->alphabet[$alphabet_len + $index2]) : $index2;
        $encoded = $encoded.$this->alphabet[$index2 % $alphabet_len];
      }
      else
        $encoded = $encoded.$s[$i];
      $i++;
    }
    return ($encoded);
  }
}
