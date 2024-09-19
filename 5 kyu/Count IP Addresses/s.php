function ips_between ($start, $end) {
  return abs(ip2long($start) - ip2long($end)); 
}
_____________
function ips_between ($start, $end) {
    $ip_start = from_octet_to_32_bit(array_map('intval', explode('.', $start)));
    $ip_end = from_octet_to_32_bit(array_map('intval', explode('.', $end)));

    
    
    return $ip_end - $ip_start;
}

function from_octet_to_32_bit(array $values)
{
    return ($values[0] * 256 ** 3) + ($values[1] * 256 ** 2) + ($values[2] * 256 ** 1) + ($values[3] * 256 ** 0);
}
________________
function ips_between ($start, $end) {
  $startIpNum = ip2long($start);
    $endIpNum = ip2long($end);
    return $endIpNum - $startIpNum;
}
