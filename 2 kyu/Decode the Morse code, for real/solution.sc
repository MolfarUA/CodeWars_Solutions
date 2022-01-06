case class MorseCodeToken(signal: Char, length: Int) {}

object MorseCodeTokenizer {
    def tokenize(bits: String): Seq[MorseCodeToken] = "(.)\\1*".r.findAllIn(trimLeadingTrailingZeros(bits)).map(t => MorseCodeToken(t.charAt(0), t.length)).toSeq
    private def trimLeadingTrailingZeros(bits: String) = (".*?(1[0,1]*?)0*$".r).findFirstMatchIn(bits) match {
        case None => ""
        case Some(s) => s.group(1)
    }
}

sealed trait MorseCodeLiteral {
    def encode:String
    def signalLength:Int
}

case class Dot(signalLength:Int) extends MorseCodeLiteral {
    override def encode:String = "."
}

case class Dash(signalLength:Int) extends MorseCodeLiteral {
    override def encode:String = "-"
}

case class SequenceDelimeter(signalLength:Int) extends MorseCodeLiteral {
    override def encode:String = ""
}

case class CharDelimeter(signalLength:Int) extends MorseCodeLiteral {
    override def encode:String = " "
}

case class WordDelimeter(signalLength:Int) extends MorseCodeLiteral {
    override def encode:String = "   "
}

case class MorseCodeMessage(signal: Seq[MorseCodeLiteral]) {
    def bitRateForLiteral(t: Class[_ <: MorseCodeLiteral]*):Double = {       
        val values = signal.filter(l => t.exists(_t => _t.isAssignableFrom(l.getClass())))
        return values.map(_.signalLength).sum / values.length.doubleValue()
    }
    def encode = signal.map(_.encode).mkString
}

case class SimpleMorseCodeTokenClassifier(bitMappings:Map[Char,Map[Double,Class[_ <: MorseCodeLiteral]]]) {
    def classify(token: MorseCodeToken):MorseCodeLiteral = {
        bitMappings.get(token.signal) match {
            case None => throw new IllegalArgumentException(s"unexpected token $token")
            case Some(lengthMappings) => lengthMappings(lengthMappings.keySet.toSeq.sortBy(key => (token.length - key).abs).head).getConstructors()(0).newInstance(token.length).asInstanceOf[MorseCodeLiteral]
        }
    }
}

case class MorseCodeClassifierParams(dotPrecedence:Double, sequencePrecedence:Double, charPrecedence:Double) {}

object SimpleMorseCodeTokenClassifier {
    def forMorseCodeMessage(msg: MorseCodeMessage, params: MorseCodeClassifierParams) = forTokenBitRates(
        msg.bitRateForLiteral(classOf[Dot], classOf[SequenceDelimeter]) + params.dotPrecedence,
        msg.bitRateForLiteral(classOf[Dash], classOf[CharDelimeter]),
        msg.bitRateForLiteral(classOf[Dot], classOf[SequenceDelimeter]) + params.sequencePrecedence,
        msg.bitRateForLiteral(classOf[CharDelimeter], classOf[Dash]) + params.charPrecedence,
        msg.bitRateForLiteral(classOf[WordDelimeter])
    )    
    
    def forSingleBitRate(bitRate:Double) = forTokenBitRates(bitRate, bitRate * 3, bitRate * .99, bitRate * 3, bitRate * 7)
    def forTokenBitRates(dot:Double, dash:Double, seqDelim:Double, charDelim:Double, wordDelim:Double):SimpleMorseCodeTokenClassifier = 
        SimpleMorseCodeTokenClassifier(Map(
        '0' -> Map(
            seqDelim -> classOf[SequenceDelimeter],
            charDelim -> classOf[CharDelimeter],
            wordDelim -> classOf[WordDelimeter]
        ),
        '1' -> Map(
            dot -> classOf[Dot],
            dash -> classOf[Dash]
        )))
}

object MorseDecoder {
    import MorseCodeTokenizer.tokenize
    import SimpleMorseCodeTokenClassifier.forSingleBitRate
    import SimpleMorseCodeTokenClassifier.forMorseCodeMessage
    def decode(bits: String):MorseCodeMessage = {
        val tokens = tokenize(bits)
        var classifier = forSingleBitRate(tokens.map(_.length).filter(_ > 0).minOption.fold(1)(identity))
        var message: MorseCodeMessage = null
        var params = MorseCodeClassifierParams(1, 1.2, 1)
        var newMessage = MorseCodeMessage(tokens.map(classifier.classify))
        var iterations = 0
        val MaxIterations = if(bits.length() > 10) {
            10
        } else {
            1
        }
        while(iterations < MaxIterations && newMessage != message) {
            message = newMessage            
            classifier = forMorseCodeMessage(message, params)
            newMessage = MorseCodeMessage(tokens.map(classifier.classify))
            iterations = iterations + 1        
        }
        // hack - tweak the precendence for seq/word break if the resulting message is not valid
        if(!valid(message.encode)) {
          classifier = forMorseCodeMessage(message, params.copy(charPrecedence = 0))
          message = MorseCodeMessage(tokens.map(classifier.classify))          
        }
        message
    }
  
    def valid(msg:String):Boolean = MorseDecoderReal.decodeMorse(msg).indexOf("unknown sequence") == -1

    def decodeTokens(tokens: Seq[MorseCodeToken], classifier:SimpleMorseCodeTokenClassifier):MorseCodeMessage = {   
        MorseCodeMessage(tokens.map(classifier.classify))
    }
}

object MorseDecoderReal {
  
  import MorseCodes.MORSE_CODE
  
  def decodeBitsAdvanced(bits:String):String = {
    println(s"bits: $bits.")
    if(bits.trim().isEmpty()) {
      return ""
    } 
    MorseDecoder.decode(bits).encode
  }
  def decodeMorse(msg:String):String = { 
    println(s"morse: $msg.")
    if(msg.trim().isEmpty()) {
      return ""
    }
    val result = msg.trim.split(" {3}")
    .map(s => s.split(" ").map(mc => MORSE_CODE.getOrElse(mc, s"unknown sequence $mc")).mkString(""))
    .mkString(" ")
    println(result)
    result
  }

}
_______________________________________________
object MorseDecoderReal {
    import MorseCodes.MORSE_CODE

    def decodeBitsAdvanced(bits:String):String = {
      if(bits.matches("\\s*|0+")) ""
      else {
        val nbits = bits.substring(bits.indexOf('1'), bits.lastIndexOf('1')+1)
        val (tmp1,register1) = "1+|0+".r.findAllIn(nbits).map(l=>(l.head, l.length)).duplicate
        val minall = tmp1.minBy(_._2)._2
        val maxone = register1.filter(_._1=='1').maxBy(_._2)._2
        val dashlen = if(maxone != minall)  maxone else minall*3

        "1+|0+".r.findAllIn(nbits).map(l=>l.head.toString*(if(l.length < (minall+dashlen)/2.0) 1 else if(l.length <= dashlen + 2) 3 else 7)).mkString("")
        .replaceAll("0000000", "   ")
          .replaceAll("111", "-")
          .replaceAll("000", " ")
          .replaceAll("1", ".")
          .replaceAll("0", "")
      }
    }

    def decodeMorse(morseCode:String):String = {
      if(morseCode.matches("\\s*")) ""
      else morseCode.trim.split("\\s{3}").map(w=>w.split("\\s").map(c=>MORSE_CODE(c)).mkString("")).mkString(" ")
    }

  }
