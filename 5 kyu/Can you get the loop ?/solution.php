function loop_size(Node $n): int {
  $a = [];
  while (!in_array($n, $a, true)) {
    array_push($a, $n);
    $n = $n->getNext();
  }
  return count($a) - array_search($n, $a, true);
}

_____________________________________________
function loop_size(Node $node): int {
    $i = 0;
    while ( !isset( $node->myf ) ) {
        $node->myf = $i;
        $node = $node->getNext();
        $i++;
    }
    return $i - $node->myf;
}
_____________________________________________
function iterate(Node &$node, SplObjectStorage &$hashes): int {
    $hashes->attach($node, $hashes->count());
    $next = $node->getNext();
    return $hashes->contains($next) ? $hashes->count() - $hashes->offsetGet($next) : iterate($next, $hashes);
}

function loop_size(Node $node): int {
    return iterate($node, new SplObjectStorage());
}
_____________________________________________
function loop_size(Node $node): int {
  $memory = [];

  for ($i = 0;; $i++) {
    $id = spl_object_id($node);
    
    if (isset($memory[$id])) {
        return count($memory) - $memory[$id];  
    } else {   
      $memory[$id] = $i;
      $node = $node->getNext();
    }
  }
}
_____________________________________________
function loop_size(Node $node): int {
    $onestep = $node;
    $twostep = $node->getNext();
    while($onestep !== $twostep) {
        $twostep = $twostep->getNext()->getNext();
        $onestep = $onestep->getNext();
    }
    $onestep = $onestep->getNext();
    $size = 1;
    while($onestep !== $twostep){
        $size += 1;
        $onestep = $onestep->getNext();
    }
    return $size;
}
