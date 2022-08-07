54b72c16cd7f5154e9000457


object MorseDecoder {
  import MorseCodes.morseCodes

  def decodeBits(bitsRaw:String):String = {
    
    val bits = bitsRaw.dropWhile(_=='0').reverse.dropWhile(_=='0').reverse
      
    val timeUnit = Array(bits.split("0").filterNot(_ == "").distinct,
      bits.split("1").filterNot(_ == "").distinct).flatten.map(_.length).min
    
    val signal = bits.grouped(timeUnit).map(_.take(1)).toArray :+ "X"
        
    signal
      .sliding(2)
      .foldLeft("")((t,c) =>
        if (c(0) == c(1)) t+c(0)
        else t+c(0)+" ").trim.split(" ")
      .map(code =>
        (code(0), code.size) match {
          case ('0',7) => "   " // new word
          case ('0',3) => " " // new character
          case ('0',1) => "" // pause between elements
          case ('1',1) => "." // dot
          case ('1',3) => "-" // dash
          case _ => throw new RuntimeException("Decoding Error")
        }
      ).mkString("")
  }
  
  
  def decodeMorse(morseCode:String):String = {
    morseCode.trim.split("   ") //words
      .map(_.split(" ")) //letters
      .map(_.map(morseCodes).mkString)
      .mkString(" ")
  }
  
}
_____________________________
object MorseDecoder {
  import MorseCodes.morseCodes

  def decodeMorse(morseCode: String): String = morseCode.trim.split("  ").map(_.trim.split(" ").map(morseCodes).mkString("")).mkString(" ")

  def decodeBits(bits: String): String = {
    val trimmedBits = bits.dropWhile(_ == '0').reverse.dropWhile(_ == '0').reverse

    val timeUnit = (trimmedBits.split("0+").filterNot(_.isEmpty).map(_.length) ++ trimmedBits.split("1+").filterNot(_.isEmpty).map(_.length)).minOption.getOrElse(0)

    trimmedBits
      .replace("1" * timeUnit * 3, "-")
      .replace("1" * timeUnit, ".")
      .replace("0" * timeUnit * 7, "   ")
      .replace("0" * timeUnit * 3, " ")
      .replace("0", "")
  }

}
_____________________________
object MorseDecoder {
  import MorseCodes.morseCodes

  def decodeBits(bits:String):String = {
    val trimmed = bits.replaceAll("^0*|0*$", "")
    val maybeDot = trimmed.split("0+").map(_.length).min
    val len = trimmed.replaceAll("^1+|1+$","").split("1+").map(_.length).filter(_ > 0).minOption.map(math.min(_, maybeDot)).getOrElse(maybeDot)
    trimmed.replaceAll("^0*|0*$", "").replaceAll(s"0{${7*len}}", "   ").replaceAll(s"0{${3*len}}", " ")
      .replaceAll(s"1{${3*len}}0{0,${len}}", "-").replaceAll(s"1{${len}}0{0,${len}}", ".")
  }
 
  def decodeMorse(msg:String):String = msg.trim.split("   ").map(
    _.trim.split(" ").map(morseCodes(_)).mkString
  ).mkString(" ")
}
