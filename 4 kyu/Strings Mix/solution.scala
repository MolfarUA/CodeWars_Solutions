object StringMix {
  def mix(s1: String, s2: String): String = {
    val f1 = s1.filter(x => x >= 'a' && x <= 'z').groupMapReduce(identity)(_ => 1)(_ + _)
    val f2 = s2.filter(x => x >= 'a' && x <= 'z').groupMapReduce(identity)(_ => 1)(_ + _)
    for {
      k <- (f1.keys ++ f2.keys).toSet[Char]
      n1 = f1.getOrElse(k, 0)
      n2 = f2.getOrElse(k, 0)
      ma = math.max(n1, n2).toInt
      if ma > 1
    } yield {
      if (n1 == n2) ("=", ma, k.toString)
      else if (n1 == ma) ("1", ma, k.toString)
      else ("2", ma, k.toString)
    }
  }.toList.map(x => s"${x._1}:${x._3 * x._2}").sortBy(x => (-x.length, x)).mkString("/")
}

_____________________________________________________
object StringMix extends App{

  def mix(s1: String, s2: String): String = {
    val m = for (let <- 'a' to 'z')
    yield (let -> (s1.count(_ == let), s2.count(_ == let)))
    m.map{
      case (chr, numbers) => numbers match {
        case numbers if numbers._1 > numbers._2 => "1:"+ chr.toString*numbers._1
        case numbers if numbers._1 < numbers._2 => "2:"+ chr.toString*numbers._2
        case _ => "=:"+chr.toString*numbers._2
      }
    }.filter(_.length > 3).sortBy(s => (-s.length, s(0))).mkString("/")
  }
}

_____________________________________________________
object StringMix {

  def mix(s1: String, s2: String): String = {
    val s1Grouped = s1.groupBy(key => key).filter { case (key, value) => key.isLower && value.length > 1 }
    val s2Grouped = s2.groupBy(key => key).filter { case (key, value) => key.isLower && value.length > 1 }
    val leftOvers = s2Grouped.filterKeys(key => !s1Grouped.contains(key)).map { case (_, value) => s"2:$value" }
    (matchGroupings(s1Grouped, s2Grouped) ++ leftOvers).filter(_.nonEmpty).sorted.sortWith(_.length > _.length).mkString("/")
  }

  private def matchGroupings(groupings1: Map[Char, String], groupings2: Map[Char, String]): List[String] = {
    groupings1.map { case (key, value) =>
      groupings2.get(key) match {
        case Some(value2) if value2 == value => s"=:$value"
        case Some(value2) if value2 > value => s"2:$value2"
        case _ => s"1:$value"
      }
    }.toList
  }
}

_____________________________________________________
object StringMix {

  def mix(s1: String, s2: String): String = {

  val xs1 = s1.filter(_.isLetter)
    .filter(_.isLower)
    .groupBy(x=>x)
    .filter(_._2.length>1)

  val xs2 = s2.filter(_.isLetter)
    .filter(_.isLower)
    .groupBy(x=>x)
    .filter(_._2.length>1)

  (xs1.keySet ++ xs2.keySet)
    .map {i=> (i, if (xs1.getOrElse(i,"").length > xs2.getOrElse(i,"").length) "1:"+xs1(i) else if (xs1.getOrElse(i,"").length < xs2.getOrElse(i,"").length) "2:"+xs2(i) else "=:"+xs1(i)  )}
    .toMap.toSeq
    .sortBy(x =>(-x._2.length, x._2.charAt(0), x._1))
    .map(_._2).mkString("/")
}}

_____________________________________________________
import scala.collection.immutable.ListMap

object StringMix {

  def mix(s1: String, s2: String): String = {
    // your code
    

var xs1 = s1.filter(_.isLetter)
  .filter(_.isLower)
  .groupBy(x=>x)
  .filter(_._2.length>1)

var xs2 = s2.filter(_.isLetter)
  .filter(_.isLower)
  .groupBy(x=>x)
  .filter(_._2.length>1)


var L = ListMap(
(xs1.keySet ++ xs2.keySet)
  .map {i=> (i, if (xs1.getOrElse(i,"").length > xs2.getOrElse(i,"").length) "1:"+xs1(i) else if (xs1.getOrElse(i,"").length < xs2.getOrElse(i,"").length) "2:"+xs2(i) else "=:"+xs1(i)  )}
  .toMap.toSeq.sortBy(_._2.length).reverse:_*)

if (L.isEmpty) "" else {
  


var i:Int = L.head._2.length
var s:String = ""

while (i>2)
  {
    if (!(L.filter(_._2.length == i).isEmpty))
      {
        //var L2 = L.filter(_._2.length == i).toMap.toSeq.sortBy(_._1).toMap
        var L2 = L.filter(_._2.length == i).toMap.toSeq.sortBy(_._1)

        print(i); print(" "); print("fff - ");println(L2)
        for (c <- L2)
          {
            if (c._2.charAt(0) == '1') s+=c._2+"/"
          }
        for (c <- L2)
        {
          if (c._2.charAt(0) == '2') s+=c._2+"/"
        }
        for (c <- L2)
        {
          if (c._2.charAt(0) == '=') s+=c._2+"/"
        }
      }
    i-=1
  }

s = s.slice(0,s.length-1) //.replace("/:","/=:")
if (s.slice(0,1)==":") "/"+s else s

}



    

    
    
    
    
    
    
  }
}

_____________________________________________________
object StringMix {
  
  def groupChars(str: String): Map[Char, Int] =
    str.filter(char => char >= 'a' && char <= 'z')
      .groupMapReduce(identity)(_ => 1)(_ + _)
      .filter { case (k, v) => v > 1 }
  
  def makeString(char: Char, fst: Map[Char, Int], snd: Map[Char, Int]): String =
    (fst.get(char), snd.get(char)) match { 
      case (Some(n), Some(k)) =>
        if (n > k)      s"1:${char.toString * n}"
        else if (n < k) s"2:${char.toString * k}"
        else            s"=:${char.toString * n}"
      case (Some(n), None   ) =>
        s"1:${char.toString * n}"
      case (None   , Some(m)) =>
        s"2:${char.toString * m}"
      case _ => 
        ""
    }


  def mix(s1: String, s2: String): String = {
    val fst = groupChars(s1)
    val snd = groupChars(s2)
    (fst.keySet ++ snd.keySet)
      .map(makeString(_, fst, snd))
      .filter(_.nonEmpty)
      .toList
      .sortWith { (a, b) =>
        a.length > b.length || 
          a.length == b.length && a < b
      }
      .mkString("/")
  }
}
