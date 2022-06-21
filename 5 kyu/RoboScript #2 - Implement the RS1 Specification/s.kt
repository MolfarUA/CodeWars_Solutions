5870fa11aa0428da750000da


enum class Direction { RIGHT, LEFT, UP, DOWN }

fun execute(code: String): String {
    val pos: ArrayList<Pair<Int, Int>> = arrayListOf(Pair(0, 0))
    val rem: String = code
    var dir: Direction = Direction.RIGHT
    var matchResult = Regex("""(L\d*|R\d*|F\d*)""").find(rem)


    while (matchResult != null) {
        with(matchResult.groupValues[1]) {
            val move = first()
            val nb = if (length == 1) 1 else substring(1).toInt()

            when (move) {
                'L' -> repeat(nb) {
                    dir = when (dir) {
                        Direction.RIGHT -> Direction.UP
                        Direction.UP -> Direction.LEFT
                        Direction.LEFT -> Direction.DOWN
                        Direction.DOWN -> Direction.RIGHT
                    }
                }
                'R' -> repeat(nb) {
                    dir = when (dir) {
                        Direction.RIGHT -> Direction.DOWN
                        Direction.UP -> Direction.RIGHT
                        Direction.LEFT -> Direction.UP
                        Direction.DOWN -> Direction.LEFT
                    }
                }
                'F' -> {
                    repeat(nb) {
                        pos.last().let {
                            pos.add(when (dir) {
                                Direction.RIGHT -> Pair(it.first + 1, it.second)
                                Direction.UP -> Pair(it.first, it.second - 1)
                                Direction.LEFT -> Pair(it.first - 1, it.second)
                                Direction.DOWN -> Pair(it.first, it.second + 1)
                            })
                        }
                    }
                }
            }
        }

        matchResult = matchResult.next()
    }

    val min: Pair<Int, Int> = Pair(pos.map { it.first }.min() ?: 0, pos.map { it.second }.min() ?: 0)
    val max: Pair<Int, Int> = Pair(pos.map { it.first }.max() ?: 0, pos.map { it.second }.max() ?: 0)
    val rx = max.first - min.first
    val ry = max.second - min.second
    val list: List<MutableList<String>> = generateSequence { generateSequence { " " }.take(rx + 1).toMutableList() }.take(ry + 1).toList()
    pos.forEach { list[it.second - min.second][it.first - min.first] = "*" }

    return list.map {
        it.joinToString("")
    }.joinToString("\r\n")
}
__________________________
import java.awt.Point
import java.awt.Rectangle

fun execute(code: String): String {
    var current = Point()
    var dir = Point(1, 0)
    val visited = mutableSetOf(current)

    for (result in Regex("(F+|R+|L+)(\\d*)").findAll(code)) {
        val action = result.groupValues[1][0]
        val repeat = result.groupValues[1].length - 1 + (result.groupValues[2].toIntOrNull() ?: 1)

        for (i in 0 until repeat) {
            when (action) {
                'F' -> {
                    current = Point(current.x + dir.x, current.y + dir.y)
                    visited.add(current)
                }
                'L' -> dir = Point(dir.y, -dir.x)
                'R' -> dir = Point(-dir.y, dir.x)
            }
        }
    }

    val bounds = visited.fold(Rectangle(-1, -1)) { r, p -> r.add(p); r }
    return (bounds.y..bounds.y + bounds.height).joinToString("\r\n") { row ->
        (bounds.x..bounds.x + bounds.width).joinToString("") { col -> if (Point(col, row) in visited) "*" else " " }
    }
}
__________________________
class Robot(
    private val grid: Grid
) {
    private var x = 0
    private var y = 0
    private var dx = 1
    private var dy = 0

    init {
        grid.footstep(x, y)
    }

    fun moveForward() {
        x += dx
        y += dy
        grid.footstep(x, y)
    }

    fun rotateLeft() {
        if (dx != 0) {
            dy = -dx
            dx = 0
        } else {
            dx = dy
            dy = 0
        }
    }

    fun rotateRight() {
        if (dx != 0) {
            dy = dx
            dx = 0
        } else {
            dx = -dy
            dy = 0
        }
    }
}

class Grid {
    private var top = 0
    private var bottom = 0
    private var left = 0
    private var right = 0
    private val grid = mutableMapOf<Int, MutableSet<Int>>()

    fun footstep(x: Int, y: Int) {
        grid.computeIfAbsent(y) {
            top = minOf(top, y)
            bottom = maxOf(bottom, y)
            mutableSetOf()
        }
        left = minOf(left, x)
        right = maxOf(right, x)
        grid[y]!! += x
    }

    override fun toString(): String {
        if (grid.isEmpty()) return ""
        
        val sb = StringBuilder()
        for (row in 0 until (bottom - top + 1)) {
            for (column in 0 until (right - left + 1)) {
                val symbol = if (grid[row + top]!!.contains(column + left)) '*' else ' '
                sb.append(symbol)
            }
            if (row != bottom - top) sb.append("\r\n")
        }

        return sb.toString()
    }
}

fun execute(code: String): String {
    val grid = Grid()
    val robot = Robot(grid)

    val commands = "[LFR]\\d*".toRegex().findAll(code).map { it.value }
    commands.forEach { command ->
        val move = command.first()
        val times = if (command.length > 1) command.substring(1).toInt() else 1

        for (i in 0 until times) {
            when (move) {
                'F' -> robot.moveForward()
                'L' -> robot.rotateLeft()
                'R' -> robot.rotateRight()
            }
        }
    }

    return grid.toString()
}
