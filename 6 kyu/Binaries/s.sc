object CodeDecode {

  def code(str: String): String =
    str.map(_.asDigit.toBinaryString).map(b => s"""${"0" * (b.size - 1)}1$b""").mkString

  val figures = (0 to 9).map(i => code(i.toString) -> i)
  
  def decode(str: String): String =
    Seq.unfold(str)(x => figures.collectFirst { case (s, i) if x.startsWith(s) => (i, x.stripPrefix(s)) }).mkString
}
__________________________
object CodeDecode {
  def code(strng: String): String =
    strng.map(_.asDigit).map {
      d => "0" * (d.toBinaryString.length - 1) + "1" + d.toBinaryString
    }.mkString

  def decode(str: String): String = str match {
    case s if s.length == 0 => ""
    case _ =>
      val i = str.indexOf('1')
      (Integer.parseInt(str.slice(i + 1, 2 * i + 2), 2).toString
        + decode(str.slice(2 * i + 2, str.length)))
  }
}
__________________________
object CodeDecode {

def code(strng: String): String = strng.split("").map(x=>"0"*(x.toInt.toBinaryString.length-1)+"1"+x.toInt.toBinaryString).mkString("")
  def decode(str: String): String = if(str.length==0) "" else Integer.parseInt(str.substring(str.indexOf('1')+1, 2*(str.indexOf('1')+1)), 2).toString+
    decode(str.substring(2*(str.indexOf('1')+1)))

}
__________________________
object CodeDecode {
  
  val decToBin = Map(
    '0' -> "0",
    '1' -> "1",
    '2' -> "10",
    '3' -> "11",
    '4' -> "100",
    '5' -> "101",
    '6' -> "110",
    '7' -> "111",
    '8' -> "1000",
    '9' -> "1001"
  )
  
  val binToDec = decToBin.map(_.swap)

  def code(str: String): String = {
    str
      .map(decToBin.getOrElse(_, ""))
      .map(num => "0" * (num.size - 1) + "1" + num)
      .mkString
  }
  
  def decode(str: String): String = {
    val it = str.iterator
    val result = new StringBuilder()
    while (it.hasNext) {
      val size = it.takeWhile(_ != '1').count(x => true) + 1
      val digit = it.take(size).mkString
      result.append(binToDec.getOrElse(digit, ""))
    }
    result.toString
  }
}
__________________________
object CodeDecode {

  def code(strng: String): String = {
    val list = strng.split("").toList.map(x => x.toInt.toBinaryString)
    list.flatMap(x => (List.fill(x.length-1)(0) :+ 1) ++ x).mkString("")
  }
  def decode(str: String, list: List[Int] = List()): String = {
    if (str.length == 0) {
      list.mkString("")
    }
    else {
      val n = str.takeWhile(_ == '0').length + 1
      val digit = Integer.parseInt(str.take(2*n).drop(n), 2)
      decode(str.drop(2*n), list :+ digit)
    }
  }
}
__________________________
object CodeDecode {

  def code(str: String): String =
    str.map(_.toString.toInt.toBinaryString).map(b => s"""${"0" * (b.size - 1)}1$b""").mkString

  val figures = (0 to 9).map(i => code(i.toString) -> i)
  
  def decode(str: String): String =
    Seq.unfold(str)(x => figures.collectFirst { case (s, i) if x.startsWith(s) => (i, x.stripPrefix(s)) }).mkString
}
__________________________
import scala.collection.mutable.ListBuffer

object CodeDecode {

  def code(s: String): String = {
    s.map(c => {
            val binrep = c.asDigit.toBinaryString
            val k = binrep.length
            val b = "0" * (k-1) + "1"
            b + binrep
          }
    ).mkString("")
  }

  def decode(str: String): String = {

    var start = 0
    var result = new ListBuffer[String]()

    while (start < str.length){
        var binStartIndex = (start to str.length).dropWhile(str(_) != '1').drop(1).take(1)(0)
        start = 2 * binStartIndex - start  
        result +=  decodeSlice(binStartIndex, start, str)
    
    }
    result.mkString("")
  }
  
  def decodeSlice(dropUntil : Int, end: Int, str: String): String ={
    val binarySt = str.slice(dropUntil, end)
    Integer.parseInt(binarySt, 2).toString
  }
}
__________________________
object CodeDecode {

  def code(strng: String): String =
    strng.map(ch => code(ch.asDigit)).mkString

  def decode(str: String): String =
    if (str.isEmpty) {
      ""
    } else {
      val i = if (str.startsWith("1")) 2 else if (str.startsWith("01")) 4 else if (str.startsWith("001")) 6 else 8
      decodePart(str.take(i)) + decode(str.drop(i))
    }

  def code(num: Int): String =
    num match {
      case 0 => "10"
      case 1 => "11"
      case 2 => "0110"
      case 3 => "0111"
      case 4 => "001100"
      case 5 => "001101"
      case 6 => "001110"
      case 7 => "001111"
      case 8 => "00011000"
      case 9 => "00011001"
    }

  def decodePart(str: String): String =
    str match {
      case "10"       => "0"
      case "11"       => "1"
      case "0110"     => "2"
      case "0111"     => "3"
      case "001100"   => "4"
      case "001101"   => "5"
      case "001110"   => "6"
      case "001111"   => "7"
      case "00011000" => "8"
      case "00011001" => "9"
    }
}
