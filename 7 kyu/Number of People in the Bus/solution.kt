fun people(busStops: Array<Pair<Int, Int>>) = busStops.sumBy { it.first - it.second }
_____________________________________
fun people(busStops: Array<Pair<Int, Int>>): Int {
    return busStops.sumBy { (on, off) -> on - off }
}
_____________________________________
fun people(busStops: Array<Pair<Int, Int>>) : Int {
  return busStops.map{it.first - it.second}.reduce{peopleRemaining, passengers -> 
                                  peopleRemaining + passengers}
}
_____________________________________
fun people(busStops: Array<Pair<Int, Int>>) : Int {
  var commonIn = busStops.sumBy { it.first }
  var commonOut = busStops.sumBy { it.second }

  var commonPeople = commonIn - commonOut
  return commonPeople
}
_____________________________________
fun people(busStops: Array<Pair<Int, Int>>) : Int = with(busStops.unzip()) { first.sum() - second.sum() }
