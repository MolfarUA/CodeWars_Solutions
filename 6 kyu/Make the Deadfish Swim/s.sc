object DeadFish {

  def parse(data: String): List[Int] =
    data.foldLeft(0, List[Int]()) {
      case ((v, out), 'i') => (v+1, out)
      case ((v, out), 'd') => (v-1, out)
      case ((v, out), 's') => (v*v, out)
      case ((v, out), 'o') => (v,   out :+ v)
    }._2
}
__________________________________________
import scala.collection.mutable.ListBuffer

object DeadFish {
  def parse(data: String): List[Int] = {
    // Implement me! :)
    data.foldLeft((0, List[Int]())) {
      case ((value, output), 'i') => (value + 1, output)
      case ((value, output), 'd') => (value - 1, output)
      case ((value, output), 's') => (value * value, output)
      case ((value, output), 'o') => (value, output :+ value)
      case ((value, output), _) => (value, output)
    }._2
  }
}
__________________________________________
import scala.collection.mutable.ListBuffer

object DeadFish {
  def parse(data: String): List[Int] = {
    // Implement me! :)
    var value = 0
    var output = new ListBuffer[Int]()
    data.split("").map{c=>
      
      c match{
        case "i" => value = value + 1
        case "d" => value = value - 1
        case "s" => value = value * value
        case "o" => output += value
      }
//     if(c == "i") value = value + 1
//     if(c == "d") value = value - 1
//     if(c == "s") value = value * value
//     if(c == "o") output += value
    println(data)
    println(value)
    }

    output.toList
  }
}
__________________________________________
import scala.collection.mutable.ListBuffer

object DeadFish {
  def parse(data: String): List[Int] = {
   
  val stringAsList = data.toList

  var initV = 0
  val resultList = ListBuffer[Int]()

  stringAsList.map(x => x match {
    case 'o' => resultList += initV
    case 'i' => initV = initV + 1
    case 'd' => initV = initV - 1
    case 's' => initV = initV * initV
  })
  resultList.toList
}
}
__________________________________________
import scala.collection.mutable.ListBuffer

object DeadFish {
  def parse(data: String): List[Int] = data.toCharArray.foldLeft(0, List[Int]())((s, c) => c match {
    case 'i' => (s._1 + 1, s._2)
    case 'd' => (s._1 - 1, s._2)
    case 's' => (s._1 * s._1, s._2)
    case 'o' => (s._1, s._2 :+ s._1)
  })._2
}
__________________________________________
import scala.collection.mutable.ListBuffer

object DeadFish {
  def parse(data: String): List[Int] = {
    var output: List[Int] = List()
    var cur_val:Int = 0
    for (s <- data){
      println(cur_val)
      s match{
        case 'i' => cur_val +=1
        case 'd' => cur_val -=1
        case 's' => cur_val = math.pow(cur_val, 2).toInt
        case 'o' =>{
          output = output :+ cur_val
        }
      }
    }
    return output
  }
}
