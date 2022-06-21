5993c1d917bc97d05d000068



class Solution {

  def regexDivisibleBy(m: Int): String = {
    if (m == 1) return "[01]*"
    val b = Array.ofDim[String](m)
    val a = Array.ofDim[String](m,m)
    
    def fstar(pre: String) = if (pre == null) "" else s"($pre)*"
    
    def fand(pre: String, x: String): String = {
      if (pre == null || x == null) return null 
      if (pre == "")   return s"($x)"
      if (x == "")     return s"($pre)"
      s"($pre)($x)"
    }
    
    def ffor(pre: String, x: String): String = {
      if (pre == null) return x 
      if (x   == null) return pre  
      s"($pre)|($x)"
    }    
  
    b(0) = ""
    for (i <- 0 to m-1) {
      a(i)(i * 2 % m) = "0"
      a(i)((i * 2 + 1) % m) = "1"
    }
 
    for (n <- (m - 1) to 0 by -1) {
      b(n) = fand(fstar( a(n)(n) ), b(n) )
      for (j <- 0 to n) {
        a(n)(j) = fand(fstar( a(n)(n) ), a(n)(j) )
      }
      for (i <- 0 to n) {
        b(i) = ffor(b(i), (fand( a(i)(n), b(n)) ) )
        for (j <- 0 to n) {
          a(i)(j) = ffor(a(i)(j), fand( a(i)(n), a(n)(j) ) )
        }
      }
    }
    return b(0)   
  }
}
___________________________________________________________
class Solution {
    def regexDivisibleBy(n: Int): String = {
        if (n == 1) return "^[01]*$"
        val graphs = Array.ofDim[String](n, n)
        for (i <- 0 until n) {
            for (j <- 0 until n) {
              graphs(i)(j) = "-1"
            }
            graphs(i)((2 * i) % n) = "0"
            graphs(i)((2 * i + 1) % n) = "1"
        }
        for (k <- n - 1 to 0 by -1) {
            val loop = if (graphs(k)(k) == "-1") "" else (graphs(k)(k) + "*")
            for (i <- 0 until k) {
                if (graphs(i)(k) != "-1") {
                   for (j <- 0 until k) {
                        if (graphs(k)(j) != "-1") {
                            val s = if (graphs(i)(j) == "-1") "" else (graphs(i)(j) + "|")
                            graphs(i)(j) = "(?:" + s + graphs(i)(k) + loop + graphs(k)(j) + ")"
                        }
                    }
                }
            }
        }
        return "^" + graphs(0)(0) + "*$"
    }
}
___________________________________________________________
import scala.annotation.tailrec

object Solution {

  case class Digit(repr: Char, numericalValue: Int)

  type Base = List[Digit]

  def baseFromString(base: String): Base = {
    for {
      (repr, numericalValue) <- base.zipWithIndex.toList
    } yield Digit(repr, numericalValue)
  }

  type NodeValue = Int
  case class Node(value: NodeValue) extends AnyVal

  sealed trait LinkExpr {
    def r3g3x: String
  }

  case class DigitLinkExpr(value: Digit) extends LinkExpr {
    override def r3g3x: String = value.repr.toString
  }

  case class RepeatLinkExpr(expr: LinkExpr) extends LinkExpr {
    override def r3g3x: String = s"(${expr.r3g3x})*"
  }

  case class ConcatLinkExpr(a: LinkExpr, b: LinkExpr) extends LinkExpr {
    override def r3g3x: String = s"(${a.r3g3x}${b.r3g3x})"
  }

  case class OrLinkExpr(a: LinkExpr, b: LinkExpr) extends LinkExpr {
    override def r3g3x: String = s"((${a.r3g3x})|(${b.r3g3x}))"
  }

  case class Link(from: Node, to: Node, expr: LinkExpr)

  type Graph = List[Link]

  def addDigitToValue(value: Int, base: Base, digit: Digit): Int = value * base.length + digit.numericalValue

  def generateGraphFor(base: Base, modulo: Int): Graph = {
    for {
      remainder <- (0 until modulo).toList
      from = Node(remainder)
      digit <- base
      to = Node(addDigitToValue(remainder, base, digit) % modulo)
      rawExpr = DigitLinkExpr(digit)
      expr = if (from == to) RepeatLinkExpr(rawExpr) else rawExpr
    } yield Link(from, to, expr)
  }

  def prettyPrintGraph(graph: Graph): Unit = {
    for {
      links <- graph.groupBy(_.from).toList.sortBy(_._1.value)
      from = links._1
    } {
      println()
      println(s"from node ${from.value}:")
      for {
        link <- links._2
      } {
        println(s"${link.expr.r3g3x} => ${link.to.value}")
      }
    }
  }

  def findMaximumNode(graph: Graph): Node = {
    graph.flatMap(n => List(n.from, n.to)).maxBy(_.value)
  }

  def findLinksTo(graph: Graph, node: Node): List[Link] = graph.filter(_.to == node)
  def findLinksFrom(graph: Graph, node: Node): List[Link] = graph.filter(_.from == node)

  def tryReplaceSelfTarget(graph: Graph, node: Node): Graph = {
    val selfTargetOpt = graph.find(l => l.to == node && l.from == node)

    selfTargetOpt match {
      case None => graph
      case Some(repeatLink) =>
        graph.filter(_ != repeatLink).map { link =>
          if (link.to == node) {
            link.copy(expr = ConcatLinkExpr(link.expr, RepeatLinkExpr(repeatLink.expr)))
          } else {
            link
          }
        }
    }
  }

  def removeNode(graph: Graph, node: Node): Graph = {
    val woSelfTarget = tryReplaceSelfTarget(graph, node)

    val linksFrom = findLinksFrom(woSelfTarget, node)

    woSelfTarget.flatMap {
      case l if l.from == node => Nil
      case l if l.to != node => List(l)
      case l => linksFrom.map(lFrom => {
        Link(
          from = l.from,
          to = lFrom.to,
          expr = ConcatLinkExpr(l.expr, lFrom.expr)
        )
      })
    }
  }

  def mergeDuplicateTarget(graph: Graph): Graph = {
    graph.groupBy(l => l.from -> l.to).map {
      case (_, l:: Nil) => l
      case (_, links) => links.reduceLeft((l1, l2) => l1.copy(expr = OrLinkExpr(l1.expr, l2.expr)))
    }.toList
  }

  def simplifyGraph(graph: Graph): Graph = mergeDuplicateTarget(removeNode(graph, findMaximumNode(graph)))

  @tailrec
  def simplifyGraphToExpr(graph: Graph): LinkExpr = {
    graph match {
      case Nil => throw new Exception(s"Graph without link")
      case singleNode::Nil => singleNode.expr
      case _::_::_ => simplifyGraphToExpr(simplifyGraph(graph))
    }
  }
}

class Solution {
  import Solution._

  def regexDivisibleBy(n: Int): String = {
    if (n == 1) {
      "(0|1)*"
    } else {
      val base = baseFromString("01")
      val graph = generateGraphFor(base, n)
      val expr = RepeatLinkExpr(simplifyGraphToExpr(graph))

      "^" + expr.r3g3x + "$"
    }
  }
}
___________________________________________________________
import scala.collection._

class Solution {
  case class Key(a: Int, b: Int, c: Int, d: Int)
  val map = new mutable.HashMap[Key, String]()
  
  def gen(k: Key): String = map.get(k) match {
    case Some(v) => v
    case None =>
      val stack = new mutable.Stack[String]()
      for (d <- 0 to 1) {
        if ((2 * k.b + d) % k.a == k.d) {
          stack += d.toString
        }
      }

      for (l <- 0 until k.c) {
        val a = gen(Key(k.a, k.b, l, l))
        val b = gen(Key(k.a, l, l, l))
        val c = gen(Key(k.a, l, l, k.d))

        if (a.nonEmpty && c.nonEmpty) {
          if (b.nonEmpty) {
            stack += s"$a$b*$c"
          } else {
            stack += s"$a$c"
          }
        }
      }
      val res = if (stack.nonEmpty) "(?:" + stack.mkString("|") + ")" else ""
      map.addOne(k, res)
      res
  }

  def regexDivisibleBy(n: Int): String = {
     s"^${gen(Key(n, 0, n, 0))}$$"
  }
}
