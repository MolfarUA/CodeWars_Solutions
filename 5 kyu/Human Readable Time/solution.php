function human_readable(int $seconds): string
{
  return sprintf('%02d:%02d:%02d', $seconds / 3600, ($seconds % 3600) / 60, $seconds % 60);
}

_____________________________________
function human_readable($seconds) : string {
  return sprintf('%02d:%02d:%02d', $seconds / 3600, $seconds / 60 % 60, $seconds % 60);
}

_____________________________________
function human_readable($s) {
  $d = explode('.', date('j.H.i:s', $s));
  $h = ($d[0] - 1) * 24 + $d[1];
  return (strlen($h) == 1 ? '0' . $h : $h) . ':' . $d[2];
}

_____________________________________
function human_readable($seconds) {
  $h = floor($seconds / 3600);
  $m = floor($seconds % 3600 / 60);
  $s = floor($seconds % 3600 % 60);

  if ($h < 10) $h = "0$h";
  if ($m < 10) $m = "0$m";
  if ($s < 10) $s = "0$s";

  return "$h:$m:$s";
}

_____________________________________
function human_readable($seconds) {
  $formatted_secs = sprintf('%02d:%02d:%02d', (int)floor($seconds / 3600), gmdate("i", $seconds), gmdate("s", $seconds));
  var_dump($formatted_secs);
  return $formatted_secs;
}
