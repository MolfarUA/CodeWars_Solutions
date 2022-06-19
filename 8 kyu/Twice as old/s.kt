5b853229cfde412a470000d0


fun twiceAsOld(dadYearsOld: Int, sonYearsOld: Int): Int = Math.abs(dadYearsOld - (sonYearsOld * 2))
______________________________
fun twiceAsOld(dadYearsOld: Int, sonYearsOld: Int) =
    if (dadYearsOld >= 2 * sonYearsOld) dadYearsOld - 2 * sonYearsOld else 2 * sonYearsOld - dadYearsOld
______________________________
    fun twiceAsOld(dadYearsOld: Int, sonYearsOld: Int) = when (val result = dadYearsOld - (sonYearsOld * 2)) {
        in 0..Int.MAX_VALUE -> result
        else -> (sonYearsOld * 2) - dadYearsOld
    }
______________________________
fun twiceAsOld(dadYearsOld: Int, sonYearsOld: Int): Int {
      val gapAge = dadYearsOld - sonYearsOld
      if (gapAge < sonYearsOld) 
          return sonYearsOld - gapAge
      else 
          return gapAge - sonYearsOld
}
______________________________
fun twiceAsOld(dadYearsOld: Int, sonYearsOld: Int): Int {
  var a = dadYearsOld
  var b = sonYearsOld
  var count = 0
  while ( b * 2 < a){
  a = a + 1
  b = b + 1
  count = count + 1 
  }
  if ( count == 0 ) {
  count = 2 * b - a}
  return count
}
