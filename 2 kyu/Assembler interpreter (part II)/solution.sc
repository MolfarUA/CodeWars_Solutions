object AssemblerInterpreter {
    def interpret(input: String): Option[String] = {
      val noComments = input.lines.map(x => x.indexOf(";") match {
        case -1 => x
        case y => x.take(y)
      }).map(x => x.trim).filter(_ != "").toList
      
      def setLabels(input: List[String], n: Int = 0, acc: List[(String, Int)] = List()): Map[String, Int] = {
        if (input.isEmpty) acc.toMap
        else {
          if (input(0).last == ':') setLabels(input.tail, n, acc :+ (input(0).dropRight(1), n))
          else setLabels(input.tail, n + 1, acc)
        }
      }
      
      val labels = setLabels(noComments)
      val noLabels = noComments.filter(x => x.last != ':')
      
      var registers = scala.collection.mutable.Map[String, Int]()
      def execute(n: Int = 0, cmp: (Int, Int) = (1, 1), funcScope: List[Int] = List(), output: String = ""): Option[String] = {
        
        def valueOf(s: String): Int = {
          if (registers.keys.exists(_ == s)) registers(s) 
          else s.toInt
        }
        
        if (n >= noLabels.length) None
        else {
          val args = {
            val noSpaces = noLabels(n).replaceAll("[,]", "").split(" ").filter(_ != "").toList
            if (noSpaces(0) == "msg") {
              val toParse =  noLabels(n).drop(3).trim
              
              def parse(s: String, scoped: Boolean = false, acc: String = ""): String = {
                if (s == "") acc
                else {
                  if (scoped) {
                    val end = s.indexOf("'")
                    val message = s.take(end + 1).dropRight(1)
                    parse(s.drop(end + 1), !scoped, acc ++ message)
                  }
                  else {
                    val end = s.indexOf("'")
                    val message = if (end == -1) s else s.take(end)
                    val parsed = message.replaceAll("[,]", "").split(" ")
                    .filter(_ != "").map(x => valueOf(x).toString).mkString(" ")
                    parse(s.drop(message.length + 1), !scoped, acc ++ parsed)
                  }
                }
              }
              
              List(noSpaces(0), parse(toParse))
            }
            else noSpaces
          }
          args(0) match {
            case "mov" => {
              registers(args(1)) = valueOf(args(2)) 
              execute(n + 1, cmp, funcScope, output)
            }
            case "inc" => {
              registers(args(1)) += 1
              execute(n + 1, cmp, funcScope, output)
            }
            case "dec" => {
              registers(args(1)) -= 1
              execute(n + 1, cmp, funcScope, output)
            }
            case "add" => {
              registers(args(1)) += valueOf(args(2))
              execute(n + 1, cmp, funcScope, output)
            }
            case "sub" => {
              registers(args(1)) -= valueOf(args(2))
              execute(n + 1, cmp, funcScope, output)
            }
            case "mul" => {
              registers(args(1)) *= valueOf(args(2))
              execute(n + 1, cmp, funcScope, output)
            }
            case "div" => {
              registers(args(1)) /= valueOf(args(2))
              execute(n + 1, cmp, funcScope, output)
            }
            case "jmp" => {
              execute(labels(args(1)), cmp, funcScope, output)
            }
            case "cmp" => {
              execute(n + 1, (valueOf(args(1)), valueOf(args(2))), funcScope, output)
            }
            case "jne" => {
              if (cmp._1 != cmp._2) execute(labels(args(1)), cmp, funcScope, output)
              else execute(n + 1, cmp, funcScope, output)
            }
            case "je" => {
              if (cmp._1 == cmp._2) execute(labels(args(1)), cmp, funcScope, output)
              else execute(n + 1, cmp, funcScope, output)
            }
            case "jge" => {
              if (cmp._1 >= cmp._2) execute(labels(args(1)), cmp, funcScope, output)
              else execute(n + 1, cmp, funcScope, output)
            }
            case "jg" => {
              if (cmp._1 > cmp._2) execute(labels(args(1)), cmp, funcScope, output)
              else execute(n + 1, cmp, funcScope, output)
            }
            case "jle" => {
              if (cmp._1 <= cmp._2) execute(labels(args(1)), cmp, funcScope, output)
              else execute(n + 1, cmp, funcScope, output)
            }
            case "jl" => {
              if (cmp._1 < cmp._2) execute(labels(args(1)), cmp, funcScope, output)
              else execute(n + 1, cmp, funcScope, output)
            }
            case "call" => {
              execute(labels(args(1)), cmp, funcScope :+ (n + 1), output)
            }
            case "ret" => {
              if (funcScope.length == 0) execute(n + 1, cmp, funcScope, output)
              else execute(funcScope.last, cmp, funcScope.dropRight(1), output)
            }
            case "msg" => {
              execute(n + 1, cmp, funcScope, output ++ args(1))
            }
            case "end" => Some(output)
          }
        }
      }
      
      execute()
    }
}

____________________________________________________
import scala.collection.mutable
import scala.util.Try

abstract class Command(line: Int, command: String) extends Product with Serializable {
  def apply(context: Context): Option[String]

  override def toString: String = s"Line: $line, command: $command, ${this.getClass}"
}

abstract class JumpCommand(line: Int, command: String) extends Command(line: Int, command: String)

object Int {
  def unapply(s: String): Option[Int] = util.Try(s.toInt).toOption
}

case class Mov(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"mov\s*([a-zA-Z0-9_.-]+),\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x, Int(y)) => context.variable(x, y)
      case pattern(x, y) => context.variable(x, context.variable(y))
    }

    Some(result.toString)
  }
}

case class Inc(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"inc\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x) => context.variable(x, context.variable(x) + 1)
    }

    Some(result.toString)
  }
}

case class Dec(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"dec\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x) => context.variable(x, context.variable(x) - 1)
    }

    Some(result.toString)
  }
}

case class Add(line: Int, var command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"add\s*([a-zA-Z0-9_.-]+),\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x, Int(y)) => context.variable(x, context.variable(x) + y)
      case pattern(x, y) => context.variable(x, context.variable(x) + context.variable(y))
    }

    Some(result.toString)
  }
}

case class Sub(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"sub\s*([a-zA-Z0-9_.-]+),\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x, Int(y)) => context.variable(x, context.variable(x) - y)
      case pattern(x, y) => context.variable(x, context.variable(x) - context.variable(y))
    }

    Some(result.toString)
  }
}

case class Mul(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"mul\s*([a-zA-Z0-9_.-]+),\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x, Int(y)) => context.variable(x, context.variable(x) * y)
      case pattern(x, y) => context.variable(x, context.variable(x) * context.variable(y))
    }

    Some(result.toString)
  }
}

case class Div(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"div\s*([a-zA-Z0-9_.-]+),\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val result = command match {
      case pattern(x, Int(y)) => context.variable(x, context.variable(x) / y)
      case pattern(x, y) => context.variable(x, context.variable(x) / context.variable(y))
    }

    Some(result.toString)
  }
}

case class Cmp(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"cmp\s*([a-zA-Z0-9_.-]+),\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    val (x, y): (Int, Int) = command match {
      case pattern(Int(x), Int(y)) => (x, y)
      case pattern(x, Int(y)) => (context.variable(x), y)
      case pattern(Int(x), y) => (x, context.variable(y))
      case pattern(x, y) => (context.variable(x), context.variable(y))
    }

    context.comparation = x.compare(y);
    Some(context.comparation.toString)
  }
}

case class Label(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    Some(command)
  }
}

case class Jmp(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"jmp\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    command match {
      case pattern(x) => Some(x)
      case _ => None
    }
  }
}

case class Jne(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"jne\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    if (context.comparation != 0)
      command match {
        case pattern(x) => Some(x)
        case _ => None
      }
    else None
  }
}

case class Je(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"je\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    if (context.comparation == 0)
      command match {
        case pattern(x) => Some(x)
        case _ => None
      }
    else None
  }
}

case class Jge(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"jge\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    if (context.comparation >= 0)
      command match {
        case pattern(x) => Some(x)
        case _ => None
      }
    else None
  }
}

case class Jg(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"jg\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    if (context.comparation > 0)
      command match {
        case pattern(x) => Some(x)
        case _ => None
      }
    else None
  }
}

case class Jl(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"jl\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    if (context.comparation < 0)
      command match {
        case pattern(x) => Some(x)
        case _ => None
      }
    else None
  }
}

case class Jle(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"jle\s*([a-zA-Z0-9_.-]+)[;]?.*".r

    if (context.comparation <= 0)
      command match {
        case pattern(x) => Some(x)
        case _ => None
      }
    else None
  }
}

case class Ret(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    None
  }
}

case class End(line: Int, command: String) extends JumpCommand(line, command) {
  override def apply(context: Context): Option[String] = {
    None
  }
}

case class Msg(line: Int, command: String) extends Command(line, command) {

  def removeComment(str: String): String = {
    if (str.contains(";")) str.substring(0, str.indexOf(";")).trim else str
  }

  override def apply(context: Context): Option[String] = {
    val parts: mutable.ArrayBuffer[String] = mutable.ArrayBuffer[String]()

    val messageTemplate = command.replace("msg", "")
    var startString = messageTemplate.indexOf("'")
    if (startString != -1 )
      parts += messageTemplate.substring(0, startString).replace(",", "").trim
    while (startString != -1) {
      val endString = messageTemplate.indexOf("'", startString + 1)
      val stringPart = messageTemplate.substring(startString, endString)
      parts += stringPart

      startString = messageTemplate.indexOf("'", endString + 1)
      if (startString != -1) {
        val variablePart = messageTemplate.substring(endString + 1, startString)
        parts += variablePart.replace(",", "").trim
      }
    }

    parts += removeComment(
      messageTemplate.substring(messageTemplate.lastIndexOf("'"))
    ).replace("'", "").replace(",", "").trim

    val value = parts
      .filter(_.nonEmpty)
      .map {
        case x: String if x.startsWith("'") => x.replace("'", "")
        case x: String => context.variable(removeComment(x)).toString
      }

    val result = value.mkString("")
    context.result(result)
    Some(result)
  }
}

case class Call(line: Int, command: String) extends Command(line, command) {
  override def apply(context: Context): Option[String] = {
    val pattern = raw"call\s*([a-zA-Z0-9_.-]+)[;]?.*".r
    command match {
      case pattern(x) => Some(x)
      case _ => None
    }
  }
}

class Context(var _comparation: Int = 0) {
  val variables: mutable.Map[String, Int] = mutable.Map()

  def variable(name: String, value: Int): Int = {
    variables.put(name, value)
    value
  }

  def variable(name: String): Int = {
    variables(name)
  }

  def comparation: Int = _comparation;
  def comparation_= (newValue: Int): Unit = {
    _comparation = newValue
  }

  val results: mutable.ArrayBuffer[String] = mutable.ArrayBuffer[String]()
  def result(res: String): Unit = {
    results += res
  }
}

class Parser {
  def parse(commandsList: String): Array[Command] = {
    var counter = 0
    def `counter++`: Int = {counter += 1; counter}

    val commands = commandsList.split("\\n").map(_.trim()).filter(_.nonEmpty).filter(!_.startsWith(";"))

    val parsedCommands: Array[Command] = commands map {
      case x if x.startsWith("mov") => Mov(`counter++`, x)
      case x if x.startsWith("inc") => Inc(`counter++`, x)
      case x if x.startsWith("dec") => Dec(`counter++`, x)
      case x if x.startsWith("add") => Add(`counter++`, x)
      case x if x.startsWith("sub") => Sub(`counter++`, x)
      case x if x.startsWith("div") => Div(`counter++`, x)
      case x if x.startsWith("mul") => Mul(`counter++`, x)
      case x if x.endsWith(":") => Label(`counter++`, x.replace(":", ""))
      case x if x.startsWith("jmp") => Jmp(`counter++`, x)
      case x if x.startsWith("cmp") => Cmp(`counter++`, x)
      case x if x.startsWith("jne") => Jne(`counter++`, x)
      case x if x.startsWith("je") => Je(`counter++`, x)
      case x if x.startsWith("jge") => Jge(`counter++`, x)
      case x if x.startsWith("jg") => Jg(`counter++`, x)
      case x if x.startsWith("jle") => Jle(`counter++`, x)
      case x if x.startsWith("jl") => Jl(`counter++`, x)
      case x if x.startsWith("call") => Call(`counter++`, x)
      case x if x.startsWith("ret") => Ret(`counter++`, x)
      case x if x.startsWith("msg") => Msg(`counter++`, x)
      case x if x.startsWith("end") => End(`counter++`, x)
    }
    parsedCommands
  }
}

object AssemblerInterpreter {
  def findLabelNumber(commands: Seq[Command], name: String): Int = {
    val line = commands map {
      case x: Label if x.command == name => x.line
      case _ => -1
    }
    line.find(_ != -1).getOrElse(-1)
  }

  def interpret(input: String): Option[String] = {
    val operationNumbers: mutable.ArrayBuffer[Int] = mutable.ArrayBuffer[Int]()
    operationNumbers += 0
    val context = new Context()
    val commands = new Parser().parse(input)
    while (true) {
      Try { commands(operationNumbers.last) } getOrElse None match {
        case None => return None
        case _: End =>
          return Some(context.results.mkString)
        case x: Call =>
          operationNumbers(operationNumbers.length - 1) = operationNumbers(operationNumbers.length - 1) + 1
          x.apply(context).map(x => findLabelNumber(commands.toIndexedSeq, x))
            .foreach(x => operationNumbers += x)
        case _: Ret =>
          operationNumbers.remove(operationNumbers.length - 1)
        case x: JumpCommand =>
          x.apply(context) match {
            case Some(x) => findLabelNumber(commands.toIndexedSeq, x) match {
              case x if x != -1 => operationNumbers(operationNumbers.length - 1) = x
              case _ => operationNumbers(operationNumbers.length - 1) = operationNumbers(operationNumbers.length - 1) + 1
            }
            case None => operationNumbers(operationNumbers.length - 1) = operationNumbers(operationNumbers.length - 1) + 1
          }
        case x: Command =>
          x.apply(context)
          operationNumbers(operationNumbers.length - 1) = operationNumbers(operationNumbers.length - 1) + 1
      }
    }
    None
  }
}

____________________________________________________
object AssemblerInterpreter {
  import scala.util.chaining._
  
    @scala.annotation.tailrec def tailRecM[A, B](a: A)(f: A => Either[A, B]): B =
    f(a) match {
      case Left(a1) => tailRecM(a1)(f)
      case Right(b) => b
    }

  implicit class ListOps[A](private val list: List[A]) extends AnyVal {
    def uncons: (Option[A], List[A]) =
      list match {
        case head :: tl => (Some(head), tl)
        case _ => (None, Nil)
      }
  }

  implicit class StringOps(private val string: String) extends AnyVal {
    def asReg: Either[String, Int] = string.toIntOption.toRight(string)
  }
  
  sealed trait Cmd extends Product with Serializable

  type RegOr = Either[String, Int]
  object Cmd {

    def of(string: String): Option[Cmd] =
      if (string.startsWith("msg")) Some(Msg(string.drop(3).dropWhile(_ == ' ')))
      else
        string.split("\\s+").toList match {
          case "jmp" :: label :: _ => Some(Jmp(label))
          case "call" :: label :: _ => Some(Call(label))
          case "je" :: label :: _ => Some(Check(label, _ == 0))
          case "jne" :: label :: _ => Some(Check(label, _ != 0))
          case "jge" :: label :: _ => Some(Check(label, _ >= 0))
          case "jg" :: label :: _ => Some(Check(label, _ > 0))
          case "jl" :: label :: _ => Some(Check(label, _ < 0))
          case "jle" :: label :: _ => Some(Check(label, _ <= 0))
          case "mov" :: s"$reg," :: value :: _ => Some(Mov(reg, value.asReg))
          case "cmp" :: s"$valuea," :: valueb :: _ => Some(Cmp(valuea.asReg, valueb.asReg))
          case "inc" :: reg :: _ => Some(Mapping(reg, Right(1), _ + _))
          case "dec" :: reg :: _ => Some(Mapping(reg, Right(1), _ - _))
          case "add" :: s"$reg," :: valueb :: _ => Some(Mapping(reg, valueb.asReg, _ + _))
          case "sub" :: s"$reg," :: valueb :: _ => Some(Mapping(reg, valueb.asReg, _ - _))
          case "mul" :: s"$reg," :: valueb :: _ => Some(Mapping(reg, valueb.asReg, _ * _))
          case "div" :: s"$reg," :: valueb :: _ => Some(Mapping(reg, valueb.asReg, _ / _))
          case "ret" :: _ => Some(Ret)
          case "end" :: _ => Some(End)
          case _ => None
        }

    final case class Mov(reg: String, regOr: RegOr) extends Cmd
    final case class Cmp(regOr1: RegOr, regOr2: RegOr) extends Cmd
    final case class Jmp(label: String) extends Cmd
    final case class Call(label: String) extends Cmd
    final case object Ret extends Cmd
    final case object End extends Cmd
    final case class Msg(template: String) extends Cmd
    final case class Mapping(reg: String, regOr: RegOr, f: (Int, Int) => Int) extends Cmd
    final case class Check(label: String, p: Int => Boolean) extends Cmd
  }

  def asCmds(list: List[String]) = list.flatMap(Cmd.of)

  final case class State(output: Option[String] = None, regs: Map[String, Int] = Map.empty, comp: Option[Boolean])

  def splitted(input: String) = input.split("\\n").toList

  def splitlogic(input: List[String]) = input
    .map(_.pipe(s => s.indexOf(";").pipe(idx => if (idx != -1) s.take(idx) else s)).trim)
    .filter(_ != "")
    .collect {
      case s @ s"msg$_" => s
      case s => s.replaceAll("\\s+", " ")
    }
    .span(s => !s.endsWith(":"))

  def dropState[T](state: Option[(String, List[String])], acc: List[(String, List[T])])(f: List[String] => List[T]) =
    state.fold(acc) { case (name, cmds) => (name, f(cmds.reverse)) :: acc }

  def splitfn[T](input: List[String])(f: List[String] => List[T]) = tailRecM(
    (input.dropWhile(s => !s.endsWith(":")), Option.empty[(String, List[String])], List.empty[(String, List[T])])
  ) { case (rest, state, acc) =>
    rest match {
      case s"$fname:" :: next =>
        Left((next, Some((fname, List.empty)), dropState(state, acc)(f)))
      case cmd :: next =>
        Left((next, state.map(tp => tp.copy(_2 = cmd :: tp._2)), acc))
      case Nil => Right(dropState(state, acc)(f).toMap)
    }
  }
  
    def interpret(input: String): Option[String] = {
    val splitte = splitted(input)
    val (main, rest) = splitlogic(splitte)

    val mainLogic = asCmds(main)

    case class State(
      cmp: Option[Int] = None,
      out: Option[String] = None,
      regs: Map[String, Int] = Map.empty,
      stack: List[(String, List[Cmd])] = Nil,
      hasRet: Boolean = false
    )

    val routinesMap = splitfn(rest)(_.flatMap(Cmd.of))

    tailRecM(State(stack = List(("main", mainLogic)))) { state =>
      import Cmd._
      import state._
      state.stack match {
        case Nil => Right(None)
        case logic :: stackRest =>
          logic match {
            case (_, Nil) => if (hasRet) Left(state.copy(stack = stackRest)) else Right(None)
            case _ if hasRet => Left(state.copy(hasRet = false))
            case (thread, cmd :: restT) =>
              val rest = (thread, restT)
              cmd match {
                case End => Right(state.out)
                case Ret => Left(state.copy(stack = stackRest, hasRet =  true))
                case Jmp(sub) => Left(state.copy(stack = (sub, routinesMap.getOrElse(sub, Nil)) :: stackRest))
                case Call(sub) => Left(state.copy(stack = (sub, routinesMap.getOrElse(sub, Nil)) :: rest :: stackRest))
                case Mov(reg, regOr) =>
                  val newRegValue = regOr match {
                    case Left(value) => regs.get(value).fold(regs)(regs.updated(reg, _))
                    case Right(value) => regs.updated(reg, value)
                  }
                  Left(state.copy(regs = newRegValue, stack = rest :: stackRest))

                case Mapping(reg, regOr, f) =>
                  val newRegValue = regOr match {
                    case Left(value) => regs.get(value).fold(regs)(v => regs.updatedWith(reg)(_.map(f(_, v))))
                    case Right(value) => regs.updatedWith(reg)(_.map(f(_, value)))
                  }
                  Left(state.copy(regs = newRegValue, stack = rest :: stackRest))
                case Cmp(regOr1, regOr2) =>
                  (regOr1, regOr2) match {
                    case (Right(a), Right(b)) => Left(state.copy(cmp = Some(a.compare(b)), stack = rest :: stackRest))
                    case (Right(a), Left(r)) =>
                      regs.get(r).map(b => state.copy(cmp = Some(a.compare(b)), stack = rest :: stackRest)).toLeft(None)
                    case (Left(l), Right(b)) =>
                      regs.get(l).map(a => state.copy(cmp = Some(a.compare(b)), stack = rest :: stackRest)).toLeft(None)
                    case (Left(l), Left(r)) =>
                      regs
                        .get(l)
                        .flatMap(a => regs.get(r).map((a, _)))
                        .map { case (a, b) => state.copy(cmp = Some(a.compare(b)), stack = rest :: stackRest) }
                        .toLeft(None)
                  }

                case Check(sub, pred) =>
                  cmp
                    .map { cmp =>
                      if (pred(cmp)) state.copy(cmp = None, stack = (sub, routinesMap.getOrElse(sub, Nil)) :: stackRest)
                      else
                        state.copy(cmp = None, stack = rest :: stackRest)
                    }
                    .toLeft(None)
                case Msg(template) =>
                  val out = tailRecM((template, "")) { case (str, acc) =>
                    if (str.isEmpty) Right(Some(acc))
                    else {
                      val (run, string) = str.span(_ != '\'')
                      val (t, rest) = string.tail.span(_ != '\'')
                      (if (run.isEmpty) Some("") else run.takeWhile(_ != ',').asReg match {
                        case Left(value) => regs.get(value).map(_.toString)
                        case Right(value) => Some(value.toString)
                      }) match {
                        case Some(v) => Left((rest.drop(3), acc + v + t))
                        case _ => Right(None)
                      }
                    }
                  }
                  Left(state.copy(out = out, stack = rest :: stackRest))

              }
          }
      }
    }
    }
}

____________________________________________________
import Interpreter._

import scala.collection.mutable
import scala.collection.mutable.ListBuffer
import scala.util.control.Breaks.{break, breakable}


class Interpreter(
  var variables: mutable.Map[String, Int] = mutable.Map.empty[String, Int],
  var instructions: ListBuffer[Instruction] = ListBuffer.empty[Instruction]
) {
  var nextInstruction = 0
  var functionIndexes = Map.empty[String, Int] // label -> index
  var e = 0
  var output: Option[String] = Option.empty[String]
  val stack: mutable.Stack[Int] = mutable.Stack.empty[Int]

  abstract class Shift(instructionOffset: => Int) extends Instruction {
    def getNextInstruction: Int = nextInstruction + instructionOffset
  }

  abstract class Operation extends Shift(1)

  case class msg(messagesAndRegs: String*) extends Operation {
    override def apply: Unit =
      output = Option { output.getOrElse("") +
        messagesAndRegs
          .map(messageOrReg => variables
            .getOrElse(messageOrReg, messageOrReg)
          ).mkString
      }
  }

  case class mov(reg: String, value: String) extends Operation {
    override def apply: Unit =
      if (variables.contains(reg)) variables(reg) = parseValue(value)
      else variables += reg -> parseValue(value)
  }

  class inc(reg: String) extends add(reg, 1)

  class dec(reg: String) extends add(reg, -1)

  class add(reg: String, value: => Int) extends Operation {
    def this(reg: String, regOrValue: String) =
      this(reg, parseValue(regOrValue))
    override def apply: Unit =
      variables(reg) += value
  }

  class sub(reg: String, value: String) extends add(reg, -parseValue(value))

  case class mul(reg: String, value: String) extends Operation {
    override def apply: Unit = variables(reg) *= parseValue(value)
  }

  case class div(reg: String, value: String) extends Operation {
    override def apply: Unit = variables(reg) /= parseValue(value)
  }
  case class cmp(value1: String, value2: String) extends Operation {
    override def apply: Unit = e = parseValue(value1) compare parseValue(value2)
  }

  class jump(
    var p: () => Boolean,
    _nextInstruction: => Int
  ) extends Operation {
    override def apply: Unit = {}
    override def getNextInstruction: Int =
      if (p()) _nextInstruction
      else super.getNextInstruction
  }

  abstract class jumpToLabel(p: () => Boolean, label: String)
    extends jump(p, functionIndexes(label))

  case class jmp(label: String) extends jumpToLabel(() => true, label)
  case class jne(label: String) extends jumpToLabel(() => e != 0, label)
  case class je (label: String) extends jumpToLabel(() => e == 0, label)
  case class jge(label: String) extends jumpToLabel(() => e == 1 || e == 0, label)
  case class jg (label: String) extends jumpToLabel(() => e == 1, label)
  case class jle(label: String) extends jumpToLabel(() => e == -1 || e == 0, label)
  case class jl (label: String) extends jumpToLabel(() => e == -1, label)

  case class call(label: String) extends Instruction {
    override def apply: Unit = stack.append(nextInstruction + 1)
    override def getNextInstruction: Int = functionIndexes(label)
  }

  def define(label: String, functionInstructions: List[Instruction]): Unit = {
    val index = instructions.length
    instructions.appendAll(functionInstructions)
    functionIndexes += label -> index
  }

  def parseValue(value: String): Int =
    value.toIntOption.getOrElse(variables(value))

  case class jnz(reg: String, value: String)
    extends jump(() => parseValue(reg) != 0, parseValue(value))

  class ret extends Instruction {
    private def next = stack.pop
    override def apply: Unit = {}
    override def getNextInstruction: Int = next
  }

  class end extends Operation {
    override def apply: Unit = break
  }

  val instructionTypes = List(
    classOf[mov], classOf[msg],
    classOf[inc], classOf[dec],
    classOf[sub], classOf[add],
    classOf[div], classOf[mul],
    classOf[jnz], classOf[jmp], classOf[call],
    classOf[cmp],
    classOf[je], classOf[jne],
    classOf[jge], classOf[jg],
    classOf[jle], classOf[jl],
    classOf[ret], classOf[end]
  )

  def run: Interpreter = {
    nextInstruction = 0
    breakable {
      while (true) {
        val instruction = instructions(nextInstruction)
        instruction.apply
        nextInstruction = instruction.getNextInstruction
      }
    }
    this
  }
}

object Interpreter {

  trait Instruction {
    def apply: Unit
    def getNextInstruction: Int
  }

  def parseArguments(args: String): List[String] = {
      val buffer = new mutable.StringBuilder()
      val parsedArgs = new ListBuffer[String]
      var waitString = false

      def appendArg: Unit = {
        if (buffer.nonEmpty) parsedArgs.append(buffer.toString)
        buffer.clear
      }

      args
        .foreach {
          case '\'' => waitString = !waitString
          case ';' =>
            appendArg
            return parsedArgs.toList
          case ' ' | ',' if !waitString => appendArg
          case c => buffer.append(c)
        }
      appendArg
      parsedArgs.toList
    }

    def parseProgram(program: String): Interpreter = {
      val interpreter = new Interpreter()

      val instructionTypeByName = interpreter
        .instructionTypes
        .map(instructionType => (instructionType.getSimpleName, instructionType))
        .toMap

      val stringInstructions = program
        .split("\n")
        .toList
        .map(parseArguments)
        .filter(_.nonEmpty)

      val instructionBuffer = ListBuffer.empty[Instruction]
      var prevLabel = "@start"

      stringInstructions
        .foreach {
          case s"$label:" :: _ =>
            interpreter.define(prevLabel, instructionBuffer.toList)
            prevLabel = label
            instructionBuffer.clear

          case List("msg", args@_*) => instructionBuffer.append(interpreter.msg(args: _*))
          case List(instructionName, args@_*)
            if instructionTypeByName contains instructionName =>
              val argClasses: Seq[Class[_]] = classOf[Interpreter] +: args.map(_.getClass)
              val constructorArgs = interpreter +: args

              instructionBuffer.append {
                instructionTypeByName(instructionName)
                  .getConstructor(argClasses: _*)
                  .newInstance(constructorArgs: _*)
              }

          case line => throw new IllegalArgumentException(s"Cannot parse line: $line")
        }

      interpreter.define(prevLabel, instructionBuffer.toList)
      interpreter
    }
}

object AssemblerInterpreter {
  def interpret(input: String): Option[String] = {
    val interpreter = parseProgram(input)
    
    try interpreter.run
    catch { case _: Throwable => 
      return Option.empty[String]
    }
    
    interpreter.output
  }
}
