object Kata {

  def uniqueInOrder[T](xs: Iterable[T]): Seq[T] =
    if (xs.isEmpty) Nil else xs.head +: uniqueInOrder(xs.dropWhile(_ == xs.head))
}
_____________________________________________
object Kata {

  def uniqueInOrder[T](xs: Iterable[T]): Seq[T] = {
    if(xs.isEmpty) return Seq()
    @scala.annotation.tailrec
    def orderHelper(it: Iterable[T], acc: List[T]): List[T] = {
        if(it.isEmpty) acc
        else if(it.head == acc.head) orderHelper(it.tail, acc)
        else orderHelper(it.tail, it.head :: acc)
    }
    orderHelper(xs, List(xs.head)).toSeq.reverse
  }
}
_____________________________________________
object Kata {

  def uniqueInOrder[T](xs: Iterable[T]): Seq[T] = {
    val seq = xs.toList
    seq match {
      case x::_ =>  x:: uniqueInOrder(seq.dropWhile(_ == x)).toList
      case List() => Nil
    }
  }
}
_____________________________________________
object Kata {
  def uniqueInOrder[T](xs: Iterable[T]): Seq[T] =
    xs.foldLeft(List.empty[T])((res, e) => res.headOption match {
      case None => res.+:(e)
      case Some(last) => if (e.equals(last)) res else res.+:(e)
    }).reverse
}
_____________________________________________
object Kata {

  def uniqueInOrder[T](xs: Iterable[T]): Seq[T] = {
    (xs.take(1) ++ xs.lazyZip(xs.drop(1)).filter((x, y) => x != y).map(_._2)).toSeq
  }
}
