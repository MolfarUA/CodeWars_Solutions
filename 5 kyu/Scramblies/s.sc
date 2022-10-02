55c04b4cc56a697bb0000048


def scramble(s1: String, s2: String): Boolean = s2.diff(s1).isEmpty
______________________________
def scramble(s1: String, s2: String): Boolean = {
  val m1= s1.groupBy(identity).map(p=> (p._1, p._2.length))
  val m2= s2.groupBy(identity).map(p => (p._1, p._2.length))
  m2.map(c => m1.contains(c._1) && m1(c._1) >= c._2).fold(true)((acc, b) => acc & b)
}
______________________________
def scramble(s1: String, s2: String): Boolean =
  val s1Chars = s1.groupMapReduce(identity)(_ => 1)(_ + _)
  val s2Chars = s2.groupMapReduce(identity)(_ => 1)(_ + _)
  s2Chars.forall { case (c, count) => s1Chars.getOrElse(c, 0) >= count }
