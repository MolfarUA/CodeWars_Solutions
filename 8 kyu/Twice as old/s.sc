5b853229cfde412a470000d0


object Sol { 

    def twice_as_old(dad: Int, son: Int) = {
        (dad - 2 * son).abs
    }
}
______________________________
object Sol { 

    def twice_as_old(dad: Int, son: Int) = math.abs(2 * son - dad)
}
______________________________
object Sol { 

    def twice_as_old(dad: Int, son: Int) = {
    val res = (dad.toDouble,son.toDouble) match {
      case (dad, 0) => dad
      case (dad, son) if dad/son == 2 => 0
      case (dad, son) if dad/son >  2 => (dad/son-2)*son
      case (dad, son) if dad/son <  2 => (2-dad/son)*son
      case _ => 0
    }
    res.toInt.abs
    }
}
