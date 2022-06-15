function fake_bin(string $s): string {
  return preg_replace(array('/[0-4]/', '/[5-9]/'), array('0', '1'), $s);
}
__________________________________
function fake_bin(string $s): string {
  return strtr($s, '0123456789', '0000011111');
}
__________________________________
function fake_bin(string $s): string {
  return preg_replace(['/[1-4]/','/[5-9]/'], [0,1], $s);
}
__________________________________
function fake_bin(string $s): string {
  return strtr($s, '123456789', '000011111'); 
}
__________________________________
function fake_bin(string $s): string {
  $niz = str_split($s);
for ($i=0; $i < strlen($s)  ; $i++) {
if($niz[$i] < 5){
 $niz[$i] = 0;
}else {
 $niz[$i] = 1;
 }
}
 $s = implode("",$niz);
return $s;
}
__________________________________
function fake_bin(string $s): string {
  return preg_replace(['/[0-4]/', '/[5-9]/'], ['0', '1'], $s);
}
