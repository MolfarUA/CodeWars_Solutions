import org.junit.Test

import java.*
import java.util.stream.Collectors
import java.util.stream.IntStream

data class ParseError(override val message: String) : Throwable()

fun matchBrackets(input: String): Map<Int, Int> {
    val res = mutableMapOf<Int, Int>()
    val seen = mutableListOf<Int>()
    for (i in input.indices) {
        if (input[i] == '(') {
            seen += i
        }
        if (input[i] == ')') {
            if (seen.isEmpty()) {
                throw ParseError(") with no corresponding (")
            }
            val p = seen.removeLast()
            res[p] = i
        }
    }
    return res
}

fun parseRegExp(input: String): RegExp {
    if (input.isEmpty()) {
        return Void()
    }
    val mb = matchBrackets(input)
    if (input[0] in "*") {
        throw ParseError("invalid input ${input[0]}")
    }
    val subs = mutableListOf<RegExp?>()
    var i = 0
    while (i < input.length) {
        val c = input[i]
        if (c == '(') {
            val j = mb[i] ?: throw ParseError("error matching (")
            subs.add(parseRegExp(input.substring(i + 1, j)))
            i = j
        } else if (c == '.') {
            subs.add(Any())
        } else if (c == '*') {
            if (subs.isEmpty()) {
                throw ParseError("expecting element before * $input:$i")
            }
            val e = subs.removeLast()
            if (e is ZeroOrMore) {
                throw ParseError("** found")
            }
            subs.add(ZeroOrMore(e!!))
        } else if (c == '|') {
            if (subs.isEmpty()) {
                throw ParseError("expecting element before | $input:$i")
            }
            subs.add(null)
        } else {
            var next: RegExp = Normal(c)
            if (i < input.length - 1) {
                if (input[i + 1] == '*') {
                    next = ZeroOrMore(next)
                    i++
                }
            }
            subs.add(next)
        }
        ++i
    }
    if (subs.size == 1) {
        return subs[0]!!
    }
    if (subs.count { it == null } > 1) {
        throw ParseError("More then 1 |")
    }
    val o = subs.indexOf(null)
    if (o != -1) {
        val s1 = subs.subList(0, o).filterNotNull()
        val s2 = subs.subList(o + 1, subs.size).filterNotNull()
        if (s2.isEmpty()) {
            throw ParseError("Expecting expression after |")
        }
        val s1a = if (s1.size == 1) {
            s1[0]
        } else {
            Str(s1)
        }
        val s2a = if (s2.size == 1) {
            s2[0]
        } else {
            Str(s2)
        }
        return Or(s1a, s2a)
    }
    return Str(subs.filterNotNull())
}

class RegExpParser(private val input: String) {

    fun parse(): RegExp {
        try {
            return parseRegExp(input)
        } catch (e: ParseError) {
            println(e.message)
            return Void()
        }
    }
}
____________________________________________________________
class RegExpParser(input: String) {
    private var element: Sub = Sub(null)
    private var isValidator: Boolean = true

    init {
        var currentElement = element
        loop@ for (c in input) {
            when (c) {
                '(' -> {
                    val child = Sub(currentElement)
                    currentElement.subEle.add(child)
                    currentElement = child
                }
                ')' -> {
                    val parent = currentElement.parent

                    if (parent != null) {
                        if (parent.type == Sub.subType.Or) {
                            if (parent.parent == null) {
                                isValidator = false
                                break@loop
                            } else {
                                currentElement = parent.parent!!
                            }
                        } else {
                            currentElement = parent
                        }
                    } else {
                        isValidator = false
                        break@loop
                    }
                }
                '|' -> {
                    val newRoot = Sub(currentElement.parent, Sub.subType.Or)
                    val nextElement = Sub(newRoot, Sub.subType.Str)
                    val oldParent = currentElement.parent
                    currentElement.parent = newRoot
                    newRoot.subEle.add(currentElement)
                    newRoot.subEle.add(nextElement)

                    if (oldParent == null)
                        element = newRoot
                    else {
                        if (oldParent.type == Sub.subType.Or) {
                            isValidator = false
                            break@loop
                        }
                        for ((index, value) in oldParent.subEle.withIndex()) {
                            if (value == currentElement) {
                                oldParent.subEle[index] = newRoot
                                break
                            }
                        }
                    }
                    currentElement = nextElement
                }
                '.' -> currentElement.subEle.add(Sub(currentElement, Sub.subType.Any))
                '*' -> {
                    if (currentElement.type == Sub.subType.Normal) {
                        if (currentElement.type == Sub.subType.ZeroOrMore) {
                            isValidator = false
                            break@loop
                        }
                        currentElement.type = Sub.subType.ZeroOrMore
                    } else {
                        if (currentElement.subEle.lastIndex == -1) {
                            isValidator = false
                            break@loop
                        }
                        val sub = currentElement.subEle[currentElement.subEle.lastIndex]
                        val startSub = Sub(sub.parent, Sub.subType.ZeroOrMore)
                        startSub.subEle.add(sub)
                        sub.parent = startSub
                        currentElement.subEle[currentElement.subEle.lastIndex] = startSub
                    }
                }
                else -> currentElement.subEle.add(
                    Sub(
                        currentElement,
                        Sub.subType.Normal,
                        c
                    )
                )
            }
        }
        if (currentElement.parent != null && (currentElement.parent!!.type != Sub.subType.Or || currentElement.parent!!.parent != null))
            isValidator = false
        if (isVal(input) == false) {
            isValidator = false
        }
        print("")
    }

    class Sub(var parent: Sub?, var type: subType = subType.Str, var data: Char? = null) {
        enum class subType {
            Normal, ZeroOrMore, Or, Str, Any
        }

        val subEle: MutableList<Sub> = mutableListOf()

        override fun toString(): String {
            if (data != null)
                return if (type == subType.ZeroOrMore) "$data*" else data.toString()

            if (subEle.size == 1)
                return if (type == subType.ZeroOrMore) "${subEle[0]}*" else subEle[0].toString()

            return when (type) {
                subType.Or -> subEle.joinToString("|", "(", ")")
                subType.ZeroOrMore -> subEle.joinToString("", "(", ")") + "*"
                subType.Str -> subEle.joinToString("", "(", ")")
                subType.Any -> "."
                else -> ""
            }
        }
    }

    fun isVal(string: String): Boolean {
        if (string.contains("**")) return false
        if (string.matches(Regex("^\\|.*|.*\\|$"))) return false
        return true
    }

    fun parse(): RegExp {
        return if (isValidator) toRegExp(element) else Void()
    }

    fun toRegExp(element: Sub): RegExp {
        return when (element.type) {
            Sub.subType.Normal -> Normal(element.data ?: ' ')
            Sub.subType.Or -> Or(toRegExp(element.subEle[0]), toRegExp(element.subEle[1]))
            Sub.subType.ZeroOrMore -> ZeroOrMore(toRegExp(element.subEle[0]))
            Sub.subType.Str -> if (element.subEle.size == 1) toRegExp(element.subEle[0]) else
                Str(element.subEle.map { toRegExp(it) }.toList())
            Sub.subType.Any -> Any()
        }
    }
}
____________________________________________________________
import kotlin.collections.ArrayList

fun ArrayList<RegExp>.removeLast(): RegExp {
    val e = this.get(this.size-1)
    this.removeAt(this.size-1)
    return e
}

class RegExpParser(expression: String) {
    val symbols: CharArray = expression.toCharArray()
    fun parse(): RegExp {
        try {
            return this.__parse__(0, symbols.size)
        } catch (e: Exception) {
            return Void()
        }
    }
    fun __parse__(start: Int, end: Int): RegExp {
        val stack: ArrayList<RegExp> = ArrayList()
        var idx = start
        var operand: RegExp? = null
        fun makeStr(): RegExp {
            val token = Str(ArrayList(stack))
            stack.clear()
            return token
        }
        while (idx < end) {
            when (symbols[idx]) {
                '(' -> {
                    val startIdx = ++idx
                    var cnt = 1
                    while(idx < end) {
                        when (symbols[idx]) {
                            '(' -> cnt++
                            ')' -> cnt--
                        }
                        if (cnt == 0) break
                        idx++
                    }
                    if (cnt > 0) throw IllegalArgumentException()
                    stack.add(this.__parse__(startIdx, idx))
                }
                ')' -> throw IllegalArgumentException()
                '*' -> {
                    if (stack.last() is ZeroOrMore) throw IllegalArgumentException()
                    stack.add(ZeroOrMore(stack.removeLast()))
                }
                '|' -> {
                    if (operand != null || idx == 0) throw IllegalArgumentException()
                    operand = if (stack.size > 1) makeStr() else stack.removeLast()
                }
                '.' -> stack.add(Any())
                else -> stack.add(Normal(symbols[idx]))
            }
            idx++
        }
        if (operand != null)
            stack.add(Or(operand, if (stack.size > 1) makeStr() else stack.removeLast()))
        if (stack.size > 1) stack.add(makeStr())
        return stack.removeLast()
    }
}
____________________________________________________________
import org.junit.Test

import java.*
import java.util.stream.Collectors
import java.util.stream.IntStream
import java.io.StringReader

class RegExpParser(input: String) {
    val chars = Lex(input)

    // Start -> OrExpr
    fun parse(): RegExp {
        try {
            val result = parseOr()
            if (chars.next() != null) return Void()
            return result
        } catch (e: InvalidInput) {
            return Void()
        }
    }
    
    // OrExpr -> ConcatExpr
    // OrExpr -> ConcatExpr '|' ConcatExpr
    fun parseOr(): RegExp {
        val left = parseConcat()
        return when (chars.match<Bar>()) {
            null -> left
            else -> Or(left, parseConcat())
        }
    }
    
    // ConcatExpr -> PostfixExpr+
    fun parseConcat(): RegExp {
        val left = parsePostfix() ?: throw InvalidInput
        val list = arrayListOf(left, parsePostfix() ?: return left)
        while (true) {
            when (val next = parsePostfix()) {
                null -> return Str(list)
                else -> list += next
            }
        }
    }
    
    // PostfixExpr -> Atom
    // PostfixExpr -> Atom '*'
    fun parsePostfix(): RegExp? {
        val inside = parseAtom() ?: return null
        return when (chars.match<Star>()) {
            Star -> ZeroOrMore(inside)
            else -> inside
        }
    }
    
    // Atom -> '.'
    // Atom -> letter
    // Atom -> '(' OrExpr ')'
    fun parseAtom() = when (val c = chars.peek()) {
        LeftParen -> {
            chars.next()
            val inside = parseOr()
            when (chars.match<RightParen>()) {
                null -> throw InvalidInput
                else -> inside
            }
        }
        Dot -> {
            chars.next()
            Any()
        }
        is Letter -> {
            chars.next()
            Normal(c.c)
        }
        else -> null
    }
}

class Lex(input: String) {
    private val chars = StringReader(input)
    private var next: Token? = null
    
    fun peek(): Token? {
        if (next != null)
            return next
        val c = chars.read()
        if (c == -1)
            return null
        next = when (c.toChar()) {
            '*' -> Star
            '.' -> Dot
            '(' -> LeftParen
            ')' -> RightParen
            '|' -> Bar
            else -> Letter(c.toChar())
        }
        return next
    }
    
    fun next(): Token? {
        val n = peek()
        next = null
        return n
    }
    
    inline fun <reified T> match(): T? {
        val n = peek()
        if (n is T) {
            next()
            return n
        }
        return null
    }
}

sealed class Token
object Star : Token()
object LeftParen : Token()
object RightParen : Token()
object Dot : Token()
object Bar : Token()
class Letter(val c: Char) : Token()

object InvalidInput : RuntimeException()
____________________________________________________________
import org.junit.Test

import java.*
import java.util.stream.Collectors
import java.util.stream.IntStream

class RegExpParser(var input: String) {

   fun parse(): RegExp {
        try {
            return p(input, false)
        } catch (e: IllegalArgumentException) {
            return Void()
        }

    }

    fun p(s: String, fromOr: Boolean): RegExp {
        val exprs  = ArrayList<RegExp>()
        var str = s
        while (str != "") {
            if(str.startsWith("(")) {
                val cl = findClosingBracket(str, 0)
                if (cl != -1) {
                    exprs.add(p(str.substring(1, cl), false))
                    str = if (cl != str.lastIndex) str.substring(cl + 1) else ""
                } else {
                    throw IllegalArgumentException()
                }
            } else
            if ( str.first() == '.') {
                exprs.add(Any())
                str = str.drop(1)
            } else
            if (str.startsWith("|")) {
                val left = if (exprs.size > 1) Str(exprs) else if (exprs.size == 0) Void() else exprs.first()
                exprs.clear()
                val right = p(str.drop(1), true)
                exprs.add(Or(left, right))
                str = ""
            } else
            if (str.startsWith("*")) {
                if (exprs.isEmpty()) throw IllegalArgumentException()
                val exp = exprs.removeAt(exprs.size - 1)
                if (exp is ZeroOrMore) throw IllegalArgumentException()
                exprs.add(ZeroOrMore(exp))
                str = str.drop(1)
            } else
            if (str.startsWith(")")) {
                throw IllegalArgumentException()
            } else
            {
                exprs.add(Normal(str.first()))
                str = str.drop(1)
            }
        }
        if (fromOr && exprs.size == 1 && exprs.first() is Or) {
            throw IllegalArgumentException()
        }
        if (exprs.isEmpty()) {
            return Void()
        } else {
            if (exprs.size > 1) return Str(exprs)
            return exprs.first()
        }
    }
    
    fun findClosingBracket(s: String, i: Int) : Int {
        var openCounter = 1
        var closingCounter = 0
        for (k in i + 1 until s.length) {
            if (s[k] == '(') {
                openCounter++
            }
            if (s[k] == ')') {
                closingCounter++
            }
            if (closingCounter == openCounter) {
                return k;
            }
        }
        return -1;
    }
}
