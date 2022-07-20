57a5c31ce298a7e6b7000334


function binToDec($bin) {
  return bindec($bin);
}
_________________________
use function bindec as binToDec;
_________________________
function binToDec($bin) {
  return intval($bin, 2);
}
_________________________
function binToDec(string $bin) 
{
  return bindec($bin);
}
