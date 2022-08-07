59eb1e4a0863c7ff7e000008


object BooleanOrderScala {
  case class Result(combinations: Long, trueCombinations: Long) {
    def falseCombinations: Long = combinations - trueCombinations
  }

  var memo: Map[String, Result] = Map()

  def getResult(operands: String, operators: String): Result = operators match {
    case "" => Result(1L, if (operands == "t") 1L else 0L)
    case _ =>
      val key = s"$operands-$operators"
      if (memo.contains(key)) {
        memo(key)
      } else {
        val result = operators.zipWithIndex.map { case (operator, index) =>
          val leftResult = getResult(operands.take(index + 1), operators.take(index))
          val rightResult = getResult(operands.drop(index + 1), operators.drop(index + 1))
          val trueCombinations =  operator match {
            case '&' => leftResult.trueCombinations * rightResult.trueCombinations
            case '|' => leftResult.combinations * rightResult.trueCombinations + leftResult.trueCombinations * rightResult.falseCombinations
            case '^' => leftResult.trueCombinations * rightResult.falseCombinations + leftResult.falseCombinations * rightResult.trueCombinations
          }
          Result(leftResult.combinations * rightResult.combinations, trueCombinations)
        }.reduce((a, b) => Result(a.combinations + b.combinations, a.trueCombinations + b.trueCombinations))
        memo += key -> result
        result
      }
  }

  def solve(operands: String, operators: String): Long = getResult(operands, operators).trueCombinations
}
_________________________________________
object BooleanOrderScala {
  /**
    * 一眼DP
    * 令 dp(i)(j) = 字符串str从i开始长度j的子串(str.substring(i,i+j))，计算的元祖 (结果为true的可能数量，结果为false的可能数量)
    * 那么 dp(x)(1) = (str(x)=='t':1:0, str(x)=='f':1:0)
    * 计算 dp(i)(j) 的时候情况多一些，需要遍历 i -> i+j -1 之间的operators符号，分类处理。
    * 迭代算dp的时候，需要看当前字符串（长度l）的l-1种切分情况，加起来：
    * dp(i)(j) = sum( combine(dp(i)(x-i+1), dp(x+1)(j-x), operators(x)) ), x=i until j
    * 其中combine是根据 operators里面x对应的符号，算合并起来的可能数
    * 比如:
    * combine((t1,f1),(t2,f2), '&')=(t1 * t2, t1 * f2 + t2 * f1 + f1 * f2) 两边都是true结果才是true，其余情况false
    * combine((t1,f1),(t2,f2), '|')=(t1 * f2 + t2 * f1 + t1 * t2, f1 * f2) 两边都是false结果才是false，其余情况true
    * combine((t1,f1),(t2,f2), '^')=(t1 * f2 + t2 * f1, t1 * t2 + f1 * f2) 两边都是不同结果才是true，两边一样的情况false
    * 最后结果就是 dp(0)(str长度)._1
    */
  def solve(operands: String, operators: String): Long = {
    def combine(t1: Long, f1: Long, t2: Long, f2: Long, op: Char): (Long, Long) = op match {
      case '&' => (t1 * t2, t1 * f2 + t2 * f1 + f1 * f2)
      case '|' => (t1 * f2 + t2 * f1 + t1 * t2, f1 * f2)
      case '^' => (t1 * f2 + t2 * f1, t1 * t2 + f1 * f2)
    }

    val N = operands.length
    val dp = Array.fill(N, N + 1)((0L, 0L))
    for (i <- 0 until N) dp(i)(1) = (if (operands(i) == 't') 1L else 0L, if (operands(i) == 'f') 1L else 0L)
    for (len <- 2 to N) {
      for (start <- 0 to N - len) {
        val end = start + len - 1
        dp(start)(len) = (start until end).map(mid => {
          val left = dp(start)(mid - start + 1) //[start,mid]子串
          val right = dp(mid + 1)(end - mid) //(mid,end]子串
          combine(left._1, left._2, right._1, right._2, operators(mid))
        }).foldLeft((0L, 0L))((s, c) => (s._1 + c._1, s._2 + c._2))
      }
    }
    dp(0)(N)._1
  }
}
_________________________________________
object BooleanOrderScala {  
  val memo = scala.collection.mutable.Map.empty[(String, String), (Long, Long)]

  def memoizedLoop(operands: String, operators: String): (Long, Long) = memo.get((operands, operators)) match {
    case Some(value) => value
    case None =>
      val value = loop(operands, operators)
      memo((operands, operators)) = value
      value
  }

  def loop(operands: String, operators: String): (Long, Long) =
    if (operators.isEmpty) {
      operands match {
        case "t" => (1L, 0L)
        case "f" => (0L, 1L)
      }
    } else {
      var t: Long = 0
      var f: Long = 0
      (0 until operators.size).foreach { i =>
        val operator = operators(i)
        var leftOperators = operators.slice(0, i)
        val rightOperators = operators.slice(i + 1, operators.size)
        var (leftOperands, rightOperands) = operands.splitAt(i + 1)

        val (lt, lf) = memoizedLoop(leftOperands, leftOperators)
        val (rt, rf) = memoizedLoop(rightOperands, rightOperators)

        operator match {
          case '&' =>
            t += lt * rt
            f += lt * rf + lf * rt + lf * rf
          case '|' =>
            t += lt * rt + lt * rf + lf * rt
            f += lf * rf
          case '^' =>
            t += lt * rf + lf * rt
            f += lt * rt + lf * rf
        }
      }
      (t, f)
    }

  def solve(operands: String, operators: String): Long =
    memoizedLoop(operands, operators)._1
}
_________________________________________
object BooleanOrderScala {  
  val memo = scala.collection.mutable.Map.empty[(String, String), (Long, Long)]

  def memoizedLoop(operands: String, operators: String): (Long, Long) = memo.get((operands, operators)) match {
    case Some(value) => value
    case None =>
      val value = loop(operands, operators)
      memo((operands, operators)) = value
      value
  }

  def loop(operands: String, operators: String): (Long, Long) =
    if (operators.isEmpty) {
      operands match {
        case "t" => (1L, 0L)
        case "f" => (0L, 1L)
      }
    } else {
      var t: Long = 0
      var f: Long = 0
      (0 until operators.size).foreach { i =>
        val operator = operators(i)
        var leftOperators = operators.slice(0, i)
        val rightOperators = operators.slice(i + 1, operators.size)
        var (leftOperands, rightOperands) = operands.splitAt(i + 1)

        val (lt, lf) = leftOperands match {
          case "t" => (1L, 0L)
          case "f" => (0L, 1L)
          case _ => memoizedLoop(leftOperands, leftOperators)
        }

        val (rt, rf) = rightOperands match {
          case "t" => (1L, 0L)
          case "f" => (0L, 1L)
          case _ => memoizedLoop(rightOperands, rightOperators)
        }

        operator match {
          case '&' =>
            t += lt * rt
            f += lt * rf + lf * rt + lf * rf
          case '|' =>
            t += lt * rt + lt * rf + lf * rt
            f += lf * rf
          case '^' =>
            t += lt * rf + lf * rt
            f += lt * rt + lf * rf
        }
      }
      (t, f)
    }

  def solve(operands: String, operators: String): Long =
    memoizedLoop(operands, operators)._1
}
