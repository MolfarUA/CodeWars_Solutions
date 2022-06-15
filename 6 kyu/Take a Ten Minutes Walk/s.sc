object Solution {
  def isValidWalk(walk: Seq[Char]): Boolean = {
    walk.size == 10 &&
      walk.count(_ == 'n') == walk.count(_ == 's') &&
      walk.count(_ == 'e') == walk.count(_ == 'w')
  }
}
__________________________________________
object Solution {
  def isValidWalk(walk: Seq[Char]): Boolean = {
    val List(n, s, e, w) = "nsew".toList.map(x => walk.count(_ == x))
    walk.size == 10 && n == s && e == w
  }
}
__________________________________________
object Solution {
  def isValidWalk(walk: Seq[Char]): Boolean = walk.length == 10 && 
    walk.foldLeft((0,0)) { (acc, cur) => cur match {
        case 'n' => (acc._1 - 1, acc._2)
        case 's' => (acc._1 + 1, acc._2)
        case 'e' => (acc._1, acc._2 - 1)
        case 'w' => (acc._1, acc._2 + 1)
      }
    } == (0,0)
}
__________________________________________
object Solution {
  def isValidWalk(walk: Seq[Char]): Boolean = {
    if (walk.length != 10) return false;
    
    var deltaLoc = (0, 0);
    
    for(d <- walk) {
      val delta = d match {
        case 'n' => ( 0,  1);
        case 's' => ( 0, -1);
        case 'w' => ( 1,  0);
        case 'e' => (-1,  0);
      };
      deltaLoc = (deltaLoc._1 + delta._1, deltaLoc._2 + delta._2);
    }
    
    deltaLoc == (0, 0)
  }
}
__________________________________________
object Solution {
  def isValidWalk(walk: Seq[Char]): Boolean = walk match {
    case _ if walk.size != 10 => false
    case _ => val lengths = walk.groupBy(identity).map{case (k, v) => (k, v.length)}
              lengths.getOrElse('n',0) == lengths.getOrElse('s',0) && 
                lengths.getOrElse('w', 0) == lengths.getOrElse('e', 0)
  }
}
