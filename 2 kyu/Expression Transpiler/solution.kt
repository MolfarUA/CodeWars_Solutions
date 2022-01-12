import java.math.BigInteger

interface Statement
interface Expression : Statement
interface NameOrNumber
data class Name(val n: String) : Expression, NameOrNumber
data class Number(val n: BigInteger) : Expression, NameOrNumber
data class Lambda(val parameters: List<NameOrNumber>, val statement: List<NameOrNumber>) : Expression
data class FunctionCall(val expression: Expression, val parameters: List<Expression>, val lambda: Lambda?) : Statement

data class ParseException(override val message: String) : Throwable()

fun parseKotlinNumber(n: String, p: Int): Pair<Number, Int> {
    var i = p
    while (i < n.length && n[i].isDigit()) {
        i++
    }
    if (i < n.length && n[i] !in "\n {},;()-") {
        throw ParseException("invalid trailing char on number: ${n.substring(i)}")
    }
    return Number(n.substring(p, i).toBigInteger()) to i
}

fun parseKotlinName(n: String, p: Int): Pair<Name, Int> {
    var i = p
    while (i < n.length && (n[i].isDigit() || n[i] in 'a'..'z' || n[i] in 'A'..'Z' || n[i] == '_')) {
        i++
    }
    return Name(n.substring(p, i)) to i
}

fun parseKotlinParameters(expression: String, p: Int, parameters: MutableList<Expression>): Int {
    var i = p
    check(expression[i] == '(')
    i++
    if (expression[i] == ')') {
        i++
        return i
    }
    while (true) {
        if (expression[i] == ')') {
             if (expression[i-1] == ',') {
                throw ParseException("trailing ,")
            }
            i++
            return i
        }
        parseKotlinExpression(expression, i).let {
            parameters.add(it.first)
            i = it.second
            if (expression[i] == ')') {
                i++
                return i
            } else if (expression[i] == ',') {
                i++
            } else {
                throw ParseException("expecting , or ) during parsing of parameters")
            }
        }
    }
}

fun parseKotlinLambda(l: String, p: Int): Pair<Lambda, Int> {
    var i = p
    if (l[i] != '{') { throw ParseException("{ exepected for lambda") }
    i++
    if (l[i] == '}') {
        i++
        return Lambda(emptyList(), emptyList()) to i
    }
    val endB = l.substring(i, l.length).indexOfFirst { it == '}' }
    if (endB == -1) {
        throw ParseException("missing } in lambda")
    }
    val sub = l.substring(i, i + endB)
    val hasArrow = "->" in sub
    val parameters = mutableListOf<NameOrNumber>()
    while (true) {
        if (l[i] == '}') {
            i++
            return Lambda(parameters, emptyList()) to i
        }
        if (l[i] == ' ') {
            i++
        }
        parseKotlinNameOrNumber(l, i).let { pair -> parameters.add(pair.first); i = pair.second }
        if (l[i] == '-') {
            i++
            if (l[i] != '>') {
                throw ParseException("expecting -> in lambda")
            }
            i++
            if (l[i] == '}') {
                i++
                return Lambda(parameters, emptyList()) to i
            }
            val statements = mutableListOf<NameOrNumber>()
            while (true) {
                if (l[i] == '}') {
                    i++
                    return Lambda(parameters, statements) to i
                }
                if (l[i] == ' ') {
                    i++
                }
                parseKotlinNameOrNumber(l, i).let { pair -> statements.add(pair.first); i = pair.second }
                if (l[i] == '}') {
                    i++
                    return Lambda(parameters, statements) to i
                } else if (l[i] == ';') {
                    i++
                }
            }
        } else if (l[i] == ',') {
            if (!hasArrow) {
                throw ParseException("illegal part of lambda ${l.substring(i)}")
            }
            i++
        } else if (l[i] == '}') {
            i++
            return Lambda(emptyList(), parameters) to i
        } else if (l[i] == ' ') {
            if (hasArrow) {
                throw ParseException("illegal part of lambda: ${l.substring(i)}")
            }
        } else {
            throw ParseException("illegal part of lambda: ${l.substring(i)}")
        }
    }
}

fun parseKotlinExpression(expression: String, p: Int): Pair<Expression, Int> {
    var e: Expression? = null
    var i = p
    if (expression[i].isDigit()) {
        parseKotlinNumber(expression, i).let { pair -> e = pair.first; i = pair.second }
    } else if (expression[i] in 'a'..'z' || expression[i] in 'A'..'Z' || expression[i] == '_') {
        parseKotlinName(expression, i).let { pair -> e = pair.first; i = pair.second }
    } else if (expression[i] == '{') {
        parseKotlinLambda(expression, i).let { pair -> e = pair.first; i = pair.second }
    } else {
        throw ParseException("expecting name, number or lambda")
    }
    return e!! to i
}

fun parseKotlinNameOrNumber(expression: String, p: Int): Pair<NameOrNumber, Int> {
    val (e, i) = parseKotlinExpression(expression, p)
    if (e is Lambda) {
        throw ParseException("unexpected lambba")
    }
    return e as NameOrNumber to i
}

fun parseKotlinStatement(expression: String, p: Int = 0): Statement {
    println("kotlin statement: $expression")
    var e: Expression? = null
    var i = p
    parseKotlinExpression(expression, i).let { e = it.first; i = it.second }
    if (expression[i] == '(') {
        val parameters = mutableListOf<Expression>()
        parseKotlinParameters(expression, i, parameters).let { i = it }
        var lambda: Lambda? = null
        if (i < expression.length) {
            parseKotlinLambda(expression, i).let {
                lambda = it.first
                i = it.second
            }
        }
        //  check for excess non-white-space
        if (i != expression.length) {
            throw ParseException("excess characters ${expression.substring(i)}")
        }
        return FunctionCall(e!!, parameters, lambda)
    } else if (expression[i] == '{') {
        parseKotlinLambda(expression, i).let {
            val lambda = it.first
            i = it.second
            if (i != expression.length) {
                throw ParseException("excess characters ${expression.substring(i)}")
            }
            return FunctionCall(e!!, mutableListOf(), lambda)
        }
    } else {
        throw ParseException("expecting arguments or lamba after expression, not ${expression.substring(i)}")
    }
}

fun makeDartLambda(l: Lambda): String {
    val parameters = l.parameters.joinToString(",") { makeDartExpression(it as Expression) }
    val statements = l.statement.joinToString("") { makeDartExpression(it as Expression) + ";" }
    return "($parameters){$statements}"
}

fun makeDartExpression(e: Expression): String {
    if (e is Name) {
        return e.n
    }
    if (e is Number) {
        return e.n.toString()
    }
    if (e is Lambda) {
        return makeDartLambda(e)
    }
    throw IllegalStateException()
}

fun makeDartFunctionCall(f: FunctionCall): String {
    val e = makeDartExpression(f.expression)
    val parameters = (f.parameters + listOfNotNull(f.lambda)).joinToString(",") { makeDartExpression(it) }
    return "$e($parameters)"
}

fun makeDartStatement(statement: Statement): String {
    return if (statement is Expression) {
        makeDartExpression(statement)
    } else {
        makeDartFunctionCall(statement as FunctionCall)
    }
}

fun stripKotlinExpression(expression: String): String {
    val e = expression.strip().lines().joinToString("")
    val res = StringBuilder()
    for (i in e.indices) {
        if (e[i].isWhitespace() && res.last() in ",;+-(){}>") {
            continue
        }
        if (e[i].isWhitespace() && i < e.length - 1 && (e[i + 1] in ",;+-(){}>" || e[i + 1].isWhitespace())) {
            continue
        }
        res.append(e[i])
    }
    return res.toString()
}

fun transpile(expression: String): String {
    try {
        val x = stripKotlinExpression(expression)
        println("$expression $x")
        val s = parseKotlinStatement(x)
        println(s)
        return makeDartStatement(s)
    } catch (e: ParseException) {
        println(e.message)
        return ""
    } catch (e: StringIndexOutOfBoundsException) {
        return ""
    }
}
_____________________________________________________
fun transpile(expression: String): String {
    try {
        val scanner = Scanner(expression.replace('\n', ' ').trim())
        val result = scanner.func().toString()
        if (!scanner.finished()) {
            throw java.lang.IllegalArgumentException("Scanner has extra characters")
        }
        return result
    } catch (e: Exception) {
        println(e)
    }
    return ""
}

sealed class Expr

data class NameOrNumber(private val value: String) : Expr() {
    override fun toString() = value
}

data class Func(
    private val expr: Expr,
    private val params: List<Expr>
) {
    override fun toString() = "$expr(" + params.joinToString(",") + ")"
}

data class Lambda(
    internal val params: List<Expr>,
    private val statements: List<Expr>
) : Expr() {
    override fun toString() = "(${params.joinToString(",")}){${statements.joinToString("") { "$it;" }}}"
}

class Scanner(source: String) {
    private var tokens = source.dropWhile { it.isWhitespace() }
        set(value) {
            field = value.dropWhile { it.isWhitespace() }
        }

    private fun head() = tokens.firstOrNull() ?: '~'
    private fun dropTokens(n: Int) {
        tokens = tokens.drop(n)
    }

    fun expr(allowLambda: Boolean = false): Expr? {

        val name = name()
        if (name != null)
            return name

        val number = number()
        if (number != null)
            return number

        if (allowLambda) {
            val lambda = lambda()
            if (lambda != null)
                return lambda
        }

        return null
    }

    fun number(): NameOrNumber? = tokens
        .takeIf { head().isDigit() }
        ?.takeWhile { it.isDigit() }
        ?.also { dropTokens(it.length) }
        ?.let(::NameOrNumber)

    fun name(): NameOrNumber? = tokens
        .takeIf { head().isLetter() || head() == '_' }
        ?.takeWhile { it.isLetter() || it == '_' || it.isDigit() }
        ?.also { dropTokens(it.length) }
        ?.let(::NameOrNumber)

    fun separator(char: Char): Char? = tokens
        .takeIf { head() == char }
        ?.let { head() }
        ?.also { dropTokens(1) }

    fun lambda(): Lambda? = tokens
        .takeIf { head() == '{' && '}' in tokens }
        ?.takeWhile { it != '}' }
        ?.drop(1)
        ?.also { dropTokens(it.length + 2) }
        ?.let { body ->
            val parts = body.split("->")
            when (parts.size) {
                1 -> Lambda(
                    emptyList(),
                    Scanner(parts[0]).args(false, ' ')
                )
                2 -> Lambda(
                    Scanner(parts[0]).args(false, ','),
                    Scanner(parts[1]).args(false, ' ')
                ).also {
                    if (it.params.isEmpty())
                        throw java.lang.IllegalArgumentException("Empty params")
                }
                else -> throw IllegalArgumentException("Wrong number of lambda parts")
            }
        }

    fun params(): List<Expr>? = tokens
        .takeIf { head() == '(' && ')' in tokens }
        ?.takeWhile { it != ')' }
        ?.drop(1)
        ?.also { dropTokens(it.length + 2) }
        ?.let { body ->
            Scanner(body).args(true, ',')
        }

    fun func(): Func {
        val expr = requireNotNull(expr(true)) { "Expression expected" }
        val params = params()
        return if (params == null) {
            val lambda = requireNotNull(lambda()) { "Lambda expected" }
            Func(
                expr = expr,
                params = listOf(lambda)
            )
        } else {
            val lambda = lambda()
            Func(
                expr = expr,
                params = params + if (lambda != null) listOf(lambda) else emptyList()
            )
        }
    }

    fun args(allowLambda: Boolean, separator: Char): List<Expr> {
        val expressions = mutableListOf<Expr>()
        var hasSep = false
        while (true) {
            val expr = expr(allowLambda)
            if (expr != null) {
                expressions.add(expr)
                if (separator == ' ')
                    continue
                if (separator(separator) != null) {
                    hasSep = true
                    continue
                } else {
                    hasSep = false
                }
            }
            break
        }
        if (hasSep || !finished()) {
            throw java.lang.IllegalArgumentException("Scanner has extra characters")
        }
        return expressions
    }

    fun finished(): Boolean = head() == '~'

}
_____________________________________________________
fun transpile(expression: String): String {
    return Parse(expression).expFunction()
}

class Parse(expression: String) {

    enum class lexType {
        nameOrNum, LP, RP, LL, RL, LAM, PP, none
    }

    companion object {
        fun getType(string: String): lexType {
            return when (string) {
                "(" -> lexType.LP
                ")" -> lexType.RP
                "{" -> lexType.LL
                "}" -> lexType.RL
                "->" -> lexType.LAM
                "," -> lexType.PP
                else -> lexType.nameOrNum
            }
        }
    }

    private val lex: List<Pair<String, lexType>>
    private var position = 0
    private var isCompiler = true

    init {
        lex = Regex("[_a-zA-Z][a-zA-Z0-9_]*|[0-9]+|[(){},]|->")
            .findAll(expression).map { it.value to getType(it.value) }.toMutableList()
        isCompiler = Regex("([a-zA-Z0-9_(){},\\n\\t\\r ]|->)*").matches(expression)
        lex.add("" to lexType.none)
        lex.add("" to lexType.none)
    }

    //function ::= expression "(" [parameters] ")" [lambda]
    //    | expression lambda

    //function ::= expression "(" [parameters] ")"
    fun expFunction(): String {
        println("function")
        val expression = expExp()
        var params = ""
        if (lex[position].second == lexType.LP) {
            if (lex[position + 1].second != lexType.RP) {
                position++
                params += expParameter() + ","
                position++
            } else
                position += 2
            if (lex[position].second == lexType.LL)
                params += expLambda() + ","
        }
        if (lex[position].second == lexType.LL) {
            params += expLambda() + ","
        }
        if (params.length > 1)
            params = params.substring(0, params.lastIndex)
        if(position != lex.size-2)
            return ""
        if (!isCompiler)
            return ""
        return "$expression($params)"
    }

    fun err() {
        println("err")
        isCompiler = false
    }

    //expression ::= nameOrNumber
    //    | lambda
    fun expExp(): String {
        println("expression")
        if (lex[position].second == lexType.nameOrNum) {
            position++
            return lex[position - 1].first
        } else if (lex[position].second == lexType.LL)
            return expLambda()
        err()
        return ""
    }

    //parameters ::= expression ["," parameters]
    fun expParameter(): String {
        println("parameters")
        var result = expExp()
        if (lex[position].second == lexType.PP) {
            position++
            result += "," + expParameter()
        }
        return result
    }

    //lambdaparam ::= nameOrNumber ["," lambdaparam]
    fun expLambdaParam(): String {
        println("lambda-param")
        var result = lex[position].first
        position++
        if (lex[position].second == lexType.PP) {
            position++
            result += "," + expLambdaParam()
        }
        return result
    }

    //lambdastmt  ::= nameOrNumber [lambdastmt]

    //lambdastmt  ::= nameOrNumber ";" [lambdastmt]
    fun expLambdaStmt(): String {
        println("lambda-stmt")
        var result = lex[position].first + ";"
        position++
        if (lex[position].second == lexType.nameOrNum)
            result += expLambdaStmt()
        return result
    }

    //lambda ::= "{" [lambdaparam "->"] [lambdastmt] "}"

    //lambda ::= "(" [lambdaparam] "){" [lambdastmt] "}"
    fun expLambda(): String {
        var params = ""
        var stmt = ""
        println("lambda")
        if (lex[position].second == lexType.LL)
            position++
        else {
            err()
            return ""
        }
        if (lex[position].second == lexType.nameOrNum &&
            (lex[position + 1].second == lexType.PP || lex[position + 1].second == lexType.LAM)
        ) {
            params = expLambdaParam()
            if (lex[position].second == lexType.LAM)
                position++
            else {
                err()
                return ""
            }
        }
        if (lex[position].second == lexType.nameOrNum)
            stmt = expLambdaStmt()
        if (lex[position].second == lexType.RL)
            position++
        else {
            err()
            return ""
        }
        return "($params){$stmt}"
    }

}
_____________________________________________________
class Peekable<T>(sequence: Sequence<T>) {
    private val iterator = sequence.iterator()
    var lookahead: T? = null
    fun next(): T? = when {
        lookahead != null -> lookahead.also { lookahead = null }
        iterator.hasNext() -> iterator.next()
        else -> null
    }
    fun peek(): T? = next().also { lookahead = it }
}

sealed class Token {
    override fun toString(): String = javaClass.simpleName

    object LEFT_PARENT: Token()
    object RIGHT_PARENT: Token()
    object LEFT_BRACE: Token()
    object RIGHT_BRACE: Token()
    object COMMA: Token()
    object ARROW: Token()
    object EOF: Token()
    data class NAME_OR_NUMBER(val string: String): Token()
}

fun tokenize(expression: String) = sequence<Token> {
    val chars = Peekable(expression.asSequence())
    while (chars.peek() != null) {
        while (chars.peek()?.isWhitespace() == true) {
            chars.next()
        }
        val char = chars.next() ?: break
        val nextToken = when (char) {
            '(' -> Token.LEFT_PARENT
            ')' -> Token.RIGHT_PARENT
            '{' -> Token.LEFT_BRACE
            '}' -> Token.RIGHT_BRACE
            ',' -> Token.COMMA
            '-' -> if (chars.next() == '>') Token.ARROW else throw Exception("unclosed arrow")
            else -> {
                when {
                    char.isJavaIdentifierStart() -> {
                        var name = char.toString()
                        while (chars.peek()?.isJavaIdentifierPart() == true) {
                            name += chars.next()!!
                        }
                        Token.NAME_OR_NUMBER(name)
                    }
                    char.isDigit() -> {
                        var number = char.toString()
                        while (chars.peek()?.isDigit() == true) {
                            number += chars.next()!!
                        }
                        Token.NAME_OR_NUMBER(number)
                    }
                    else -> throw Exception("Unexspected $char")
                }
            }
        }
        yield(nextToken)
    }
    while (true) {
        yield(Token.EOF)
    }
}

class FunctionCall(val name: Expr, val params: List<Expr>)

sealed class Expr {
    data class NameOrNumber(val string: String): Expr()
    data class Lambda(val params: List<String>, val statement: List<String>): Expr()
}

inline fun<reified T> expect(tokens: Peekable<Token>, msg: String = "something") : T  {
    val next = tokens.next()
    if (next is T) {
        return next
    } else {
        throw Exception("Expected $msg but saw $next")
    }
}

inline fun<reified T> parseList(tokens: Peekable<Token>, endTokens: List<Token>, commaSeparated: Boolean, parseItem: () -> T) : MutableList<T>  {
    val list = mutableListOf<T>()
    if (!endTokens.contains(tokens.peek())) {
        list.add(parseItem())
    }
    while (!endTokens.contains(tokens.peek()!!)) {
        if (commaSeparated) {
            if (tokens.peek() is Token.COMMA) {
                expect<Token.COMMA>(tokens, ",")
            } else {
                break
            }
        }
        list += parseItem()
        if (tokens.peek() is Token.EOF) {
            throw Exception("Unclosed list")
        }
    }
    return list
}

fun parse(expression: String): FunctionCall  {
    
    val tokens = Peekable(tokenize(expression))

    fun lambda(): Expr.Lambda {
        expect<Token.LEFT_BRACE>(tokens, "{")
        val content = parseList(tokens, listOf(Token.ARROW, Token.RIGHT_BRACE), true) {
            expect<Token.NAME_OR_NUMBER>(tokens, "name or number").string
        }
        var params = emptyList<String>()
        var stmts = emptyList<String>()
        if (content.size > 0 && tokens.peek() is Token.ARROW) {
            params = content
            expect<Token.ARROW>(tokens, "->")
        } else if (content.size == 1) {
            stmts = content
        } else if(content.isNotEmpty()) {
            throw Exception("expected ->")
        }
        stmts += parseList(tokens, listOf(Token.RIGHT_BRACE), false) {
            expect<Token.NAME_OR_NUMBER>(tokens, "name or number").string
        }
        expect<Token.RIGHT_BRACE>(tokens, "}")

        return Expr.Lambda(params, stmts)
    }

    fun expr(): Expr {
        return when (tokens.peek()) {
            is Token.NAME_OR_NUMBER -> Expr.NameOrNumber(expect<Token.NAME_OR_NUMBER>(tokens, "name or number").string)
            else -> lambda()
        }
    }

    fun functionCall(): FunctionCall {
        val name = expr()
        var params = mutableListOf<Expr>()
        if (tokens.peek() is Token.LEFT_PARENT) {
            expect<Token.LEFT_PARENT>(tokens, "(")
            params = parseList(tokens, listOf(Token.RIGHT_PARENT), true, ::expr)
            expect<Token.RIGHT_PARENT>(tokens, ")")
        } else if (tokens.peek() !is Token.LEFT_BRACE) {
            throw Exception("expected lambda, but got ${tokens.peek()}")
        }
        if (tokens.peek() is Token.LEFT_BRACE) {
            params.add(lambda())
        }
        return FunctionCall(name, params)
    }
    return functionCall().also { expect<Token.EOF>(tokens, "EOF") }
}

fun transpile(expression: String): String {
    
    fun lambda(lambda: Expr.Lambda) =
            "(${lambda.params.joinToString(",")})" +
            "{${lambda.statement.joinToString(";")}" +
            "${if (lambda.statement.isNotEmpty()) ";" else ""}}"

    fun expr(expr: Expr) =
        when (expr) {
            is Expr.NameOrNumber -> expr.string
            is Expr.Lambda -> lambda(expr)
        }

    fun functionCall(call: FunctionCall) =
            "${expr(call.name)}" +
            "(${call.params.joinToString(","){expr(it)}})"

    return try {
        functionCall(parse(expression))
    } catch(exception: Exception) {
        ""
    }
}
