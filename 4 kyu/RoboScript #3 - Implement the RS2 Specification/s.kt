58738d518ec3b4bf95000192


enum class Direction {
    N, E, S, W
}

fun execute(code: String): String {
    val codeWithoutBrackets = resolveBrackets(code)
    val longCode = codeWithoutBrackets.replace("[FLR][0-9]+".toRegex()) {
        "${it.value[0]}".repeat(it.value.drop(1).toInt())
    }
    val coords = longCode.fold(Pair(mutableListOf(Pair(0, 0)), Direction.W)) { acc, command ->
        var direction = acc.second
        when (command) {
            'L' -> direction = when (acc.second) {
                Direction.N -> Direction.E
                Direction.E -> Direction.S
                Direction.S -> Direction.W
                Direction.W -> Direction.N
            }
            'R' -> direction = when (acc.second) {
                Direction.N -> Direction.W
                Direction.W -> Direction.S
                Direction.S -> Direction.E
                Direction.E -> Direction.N
            }
            else -> {
                val last = acc.first.last()
                val newPos = when (direction) {
                    Direction.N -> last.copy(second = last.second - 1)
                    Direction.W -> last.copy(first = last.first + 1)
                    Direction.S -> last.copy(second = last.second + 1)
                    Direction.E -> last.copy(first = last.first - 1)
                }
                acc.first += newPos
            }
        }
        acc.copy(second = direction)
    }
    val minX = (coords.first.map { it.first }.min() ?: 0)
    val minY = (coords.first.map { it.second }.min() ?: 0)
    val transposed = coords.first.map { it.copy(first = it.first - minX, second = it.second - minY) }
    val board = MutableList<MutableList<String>>((transposed.map { it.second }.max() ?: 0) + 1 ) { MutableList<String>((transposed.map { it.first }.max() ?: 0) + 1) { " " } }
    transposed.forEach { board[it.second][it.first] = "*" }
    return board.joinToString("\r\n") { it -> it.joinToString("") }
}

fun resolveBrackets(code: String): String {
    val bracketMatcher = "\\([RFL,0-9]*\\)[0-9]*".toRegex()
    var resolved = code
    while (bracketMatcher.find(resolved) != null) {
        resolved =  resolved.replace("\\([RFL,0-9]*\\)[0-9]*".toRegex()) {
            val times = "\\d+$".toRegex().find(it.value)?.value?.toInt() ?: 1
            it.value.substringBeforeLast(")").substring(1).repeat(times)
        }
    }
    return resolved
}
__________________________
import kotlin.math.*

data class Coord(val x: Int, val y: Int)

enum class Offset(val x: Int, val y: Int) {
    RIGHT(1, 0),
    TOP(0, -1),
    LEFT(-1, 0),
    BOTTOM(0, 1)
}

class Board {
    private var startX = 0
    private var startY = 0
    private var endX = 0
    private var endY = 0
    private val visited = mutableSetOf(Coord(0, 0))
    var offset = Offset.RIGHT
    var curr = Coord(0, 0)
        set(value) {
            field = value
            startX = min(startX, value.x)
            startY = min(startY, value.y)
            endX = max(endX, value.x)
            endY = max(endY, value.y)
            visited += value
        }
        
    override fun toString() =
        (startY..endY).map { y ->
            (startX..endX).map { x ->
                if (visited.contains(Coord(x, y))) "*" else " "
            }.joinToString("")
        }.joinToString("\r\n")
}

abstract class Command {
    var repeat = 1
    abstract fun execute(board: Board)
}

class Forward : Command() {
    override fun execute(board: Board) {
        for (i in 1..repeat) {
            board.curr = Coord(board.curr.x + board.offset.x, board.curr.y + board.offset.y)
        }
    }
}

class Left : Command() {
    override fun execute(board: Board) {
        for (i in 1..repeat%4) {
            board.offset = when (board.offset) {
                Offset.RIGHT -> Offset.TOP
                Offset.TOP -> Offset.LEFT
                Offset.LEFT -> Offset.BOTTOM
                Offset.BOTTOM -> Offset.RIGHT
            }
        }
    }
}

class Right : Command() {
    override fun execute(board: Board) {
        for (i in 1..repeat%4) {
            board.offset = when (board.offset) {
                Offset.RIGHT -> Offset.BOTTOM
                Offset.TOP -> Offset.RIGHT
                Offset.LEFT -> Offset.TOP
                Offset.BOTTOM -> Offset.LEFT
            }
        }
    }
}

class CommandSequence : Command() {
    companion object {
        private val REPEAT_REGEX = Regex("\\d+")
    }
    
    private val commands = mutableListOf<Command>()
    
    fun feed(code: String, pos: Int): Int {
        var currPos = pos
        while (true) {
            if (currPos == code.length) {
                return currPos
            }
            var command: Command
            when (val c = code[currPos]) {
                ')' -> return currPos
                '(' -> {
                    command = CommandSequence()
                    currPos = command.feed(code, currPos + 1)
                }
                'F' -> command = Forward()
                'L' -> command = Left()
                'R' -> command = Right()
                else -> throw IllegalArgumentException(c.toString())
            }
            commands += command
            currPos++
            REPEAT_REGEX.find(code, currPos)?.let {
                if (it.range.start == currPos) {
                    command.repeat = it.value.toInt()
                    currPos += it.value.length
                }
            }
        }
    }
    
    override fun execute(board: Board) {
        (1..repeat).forEach {
            commands.forEach { it.execute(board) }
        }
    }
}

fun execute(code: String): String {
    val top = CommandSequence()
    assert(top.feed(code, 0) == code.length)
    
    val board = Board()
    top.execute(board)
    return board.toString()
}
__________________________
fun execute(code: String): String {
    val removedBrackets = removeBrackets(code)
    val steps = Regex("""\w\d*""").findAll(removedBrackets).map { it.value }
    val state = GameState()

    steps.forEach { step ->
        repeat(Regex("\\d+").find(step)?.value?.toInt() ?: 1) {
            when (step[0]) {
                'L' -> state.dir =
                    Direction.values().getOrElse(state.dir.ordinal - 1) { Direction.UP }
                'R' -> state.dir =
                    Direction.values().getOrElse(state.dir.ordinal + 1) { Direction.RIGHT }
                else -> move(state)
            }
        }
    }

    val x = state.pos.maxOf { it.first } + 1
    val y = state.pos.maxOf { it.second } + 1
    val matrix = MutableList(y) { MutableList(x) { " " } }
    state.pos.forEach { matrix[it.second][it.first] = "*" }

    return matrix.joinToString("\r\n") { it.joinToString("") }
}

fun removeBrackets(s: String): String {
    val reg = Regex("""\(\w+?\)(\d*)""")
    val first = reg.find(s)?.value
    return if (first != null) {
        val string: String = Regex("""\w+""").find(first)!!.value
        val dig = Regex("""\d+$""").find(first)?.value?.toInt() ?: 1

        removeBrackets(reg.replaceFirst(s, string.repeat(dig)))
    } else s
}


data class GameState(
    var dir: Direction = Direction.RIGHT,
    var pos: MutableList<Pair<Int, Int>> = mutableListOf(0 to 0)
)

fun move(state: GameState) {
    var pos = state.pos.last()
    pos = pos.first + state.dir.x to pos.second + state.dir.y

    state.pos.remove(pos)
    state.pos.add(pos)

    if (pos.first < 0) state.pos = state.pos.map { it.first + 1 to it.second }.toMutableList()
    if (pos.second < 0) state.pos = state.pos.map { it.first to it.second + 1 }.toMutableList()
}

enum class Direction(val x: Int, val y: Int) {
    RIGHT(1, 0), DOWN(0, 1), LEFT(-1, 0), UP(0, -1)
}
