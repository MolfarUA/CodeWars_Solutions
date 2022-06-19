515de9ae9dcfc28eb6000001


object Kata {

  def solution(s: String): List[String] = {
    s.grouped(2).map(_.padTo(2, '_')).toList
  }
}
________________________________
object Kata {

  def solution(s: String): List[String] =
    s.padTo(s.size + s.size%2, '_').grouped(2).toList
}
________________________________
object Kata {
  def solution(s: String): List[String] = s.length match {
    case 0 => List()
    case 1 => List(s ++ "_")
    case _ => List(s.take(2)) ++ solution(s.drop(2))
  }
}
________________________________
object Kata {

  def solution(s: String): List[String] =
    (s + "_" * (s.size%2)).grouped(2).toList
}
________________________________
object Kata {

  def solution(s: String): List[String] = {
    if(s.length % 2 == 0) s.grouped(2).toList else s.concat("_").grouped(2).toList
  }
}
