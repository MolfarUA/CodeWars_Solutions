52597aa56021e91c93000cb0


function moveZeros(array $items): array {
  return array_pad(array_filter($items, function($x){return $x !== 0 and $x !== 0.0;}), count($items), 0);
}
_____________________________
function moveZeros(array $items): array
{
    foreach ($items as $key => $item) {
        if (isZero($item)) {
            unset($items[$key]);
            $items[] = $item;
        }
    }

    return array_values($items);
}

function isZero($item): bool
{
    return $item === 0 || $item === 0.0; 
}
_____________________________
function moveZeros(array $items): array
{
  $ret = array_diff($items,[0]);
  return array_merge($ret,array_fill(0,count($items)-count($ret),0));
}
_____________________________
function moveZeros(array $items): array
{
    $a=[];
    $b=[];
  foreach($items as $item){
    $item === 0 || $item === 0.0 ? $b[]=$item:$a[]=$item;
  
  }
  
   return array_merge($a,$b);
}
