5a2a597a8882f392020005e5

package kata

object Blox {
    fun bloxSolver(puzzle: Array<String>): String {
        val solver = Solver(puzzle)
        return solver.solve()
    }

    class Solver(data: Array<String>) {
        val board = data.map{ row ->
            row.map {
                it != '0'
            }
        }

        private val winState: BloxState
        val paths = HashMap<BloxState, String>()
        var recentStates = ArrayList<BloxState>()

        init {
            val winY = data.indexOfFirst { it.contains('X') }
            val winX = data[winY].indexOf('X')
            winState = BloxState(winX, winY, Blox.BloxState.BloxDirection.Upright)

            val startY = data.indexOfFirst { it.contains('B') }
            val startX = data[startY].indexOf('B')
            val startState = BloxState(startX, startY, Blox.BloxState.BloxDirection.Upright)
            paths[startState] = ""
            recentStates.add(startState)
        }

        fun solve(): String {
            while (paths[winState] == null) {
                val newStates = ArrayList<BloxState>()
                recentStates.forEach {
                    val state = it
                    val path = paths[it]!!

                    attemptMove(state.up, path, "U", newStates)
                    attemptMove(state.right, path, "R", newStates)
                    attemptMove(state.down, path, "D", newStates)
                    attemptMove(state.left, path, "L", newStates)
                }
                recentStates = newStates
            }

            return paths[winState]!!
        }

        private fun attemptMove(state: BloxState, path: String, char: String, newStates: ArrayList<BloxState>) {
            if (!isValid(state)) return
            if (paths[state] != null) return
            paths[state] = "$path$char"
            newStates.add(state)
        }

        private fun isValid(state: BloxState): Boolean {
            fun safeGet(x: Int, y:Int): Boolean {
                if (x < 0 || y < 0 || y >= board.size || x >= board[y].size) {
                    return false
                }
                return board[y][x]
            }
            if (!safeGet(state.x, state.y)) {
                return false
            }

            return when (state.direction) {
                Blox.BloxState.BloxDirection.Upright -> true
                Blox.BloxState.BloxDirection.Vertical -> safeGet(state.x, state.y+1)
                Blox.BloxState.BloxDirection.Horizontal -> safeGet(state.x + 1, state.y)
            }
        }
    }


    data class BloxState(
        val x: Int,
        val y: Int,
        val direction: BloxDirection
    ) {
        enum class BloxDirection {
            Upright,
            Vertical,
            Horizontal
        }

        val up get() = when(direction) {
            BloxDirection.Upright -> BloxState(x, y-2, BloxDirection.Vertical)
            BloxDirection.Vertical -> BloxState(x, y-1, BloxDirection.Upright)
            BloxDirection.Horizontal -> BloxState(x, y-1, BloxDirection.Horizontal)
        }

        val down get() = when(direction) {
            BloxDirection.Upright -> BloxState(x, y+1, BloxDirection.Vertical)
            BloxDirection.Vertical -> BloxState(x, y+2, BloxDirection.Upright)
            BloxDirection.Horizontal -> BloxState(x, y+1, BloxDirection.Horizontal)
        }

        val right get() = when(direction) {
            BloxDirection.Upright -> BloxState(x+1, y, BloxDirection.Horizontal)
            BloxDirection.Vertical -> BloxState(x+1, y, BloxDirection.Vertical)
            BloxDirection.Horizontal -> BloxState(x+2, y, BloxDirection.Upright)
        }

        val left get() = when(direction) {
            BloxDirection.Upright -> BloxState(x-2, y, BloxDirection.Horizontal)
            BloxDirection.Vertical -> BloxState(x-1, y, BloxDirection.Vertical)
            BloxDirection.Horizontal -> BloxState(x-1, y, BloxDirection.Upright)
        }
    }
}
_________________________________
package kata

import java.util.ArrayDeque
import java.util.Queue

object Blox {
    fun bloxSolver(puzzle: Array<String>): String {
        return solve(object : Level {
            override fun isTile(v: Vec2): Boolean {
                if (v.x < 0 || v.y >= puzzle.size ||
                    v.y < 0 || v.x >= puzzle[0].length
                ) {
                    return false
                }
                return puzzle[v.y][v.x] != '0'
            }

            override val startPosition: Vec2
                get() = findTile('B')

            override val destination: Vec2
                get() = findTile('X')

            private fun findTile(c: Char): Vec2 {
                for ((y, s) in puzzle.withIndex()) {
                    val x = s.indexOf(c)
                    if (x != -1) {
                        return Vec2(x, y)
                    }
                }
                throw AssertionError()
            }
        })
    }

    private fun solve(level: Level): String {
        val parents = hashMapOf<State, State>()
        val queue: Queue<State> = ArrayDeque()
        queue.add(State(Upright(level.startPosition), null))

        while (!queue.isEmpty()) {
            val currentState = queue.poll()
            val position = currentState.position
            if (position is Upright && position.pos == level.destination) {
                var state = currentState
                val sb = StringBuilder()
                while (state.lastMove != null) {
                    sb.append(state.lastMove!!.name.first())
                    state = parents[state]
                }
                return sb.reverse().toString()
            }

            for (direction in Direction.values()) {
                val newPosition = position.moveIn(direction)
                if (!level.isValid(newPosition)) {
                    continue
                }
                val newState = State(newPosition, direction)
                val previous = parents.putIfAbsent(newState, currentState)
                if (previous == null) {
                    queue.add(newState)
                }
            }
        }
        throw RuntimeException("No solution")
    }

    private interface Level {
        fun isValid(position: BlockPosition): Boolean {
            return when (position) {
                is Upright -> isTile(position.pos)
                is OnLongEnd -> isTile(position.pos1) && isTile(position.pos2)
            }
        }

        fun isTile(v: Vec2): Boolean

        val destination: Vec2
        val startPosition: Vec2
    }

    private data class State(val position: BlockPosition, val lastMove: Direction?) {

        override fun equals(other: Any?): Boolean {
            if (this === other) return true
            if (javaClass != other?.javaClass) return false
            other as State
            return position == other.position
        }

        override fun hashCode(): Int {
            return position.hashCode()
        }
    }

    private sealed interface BlockPosition {
        fun moveIn(direction: Direction): BlockPosition
    }

    private data class Upright(val pos: Vec2) : BlockPosition {
        override fun moveIn(direction: Direction): BlockPosition {
            val pos1 = pos.moveIn(direction)
            val pos2 = pos1.moveIn(direction)
            return OnLongEnd(pos1, pos2)
        }
    }

    private data class OnLongEnd(val pos1: Vec2, val pos2: Vec2) : BlockPosition {

        override fun moveIn(direction: Direction): BlockPosition {
            if (pos1.x == pos2.x) {
                if (direction == Direction.UP || direction == Direction.DOWN) {
                    if (direction == Direction.DOWN) {
                        val edge = maxOf(pos1, pos2) { a, b -> a.y.compareTo(b.y) }
                        return Upright(edge.moveIn(direction))
                    } else {
                        val edge = minOf(pos1, pos2) { a, b -> a.y.compareTo(b.y) }
                        return Upright(edge.moveIn(direction))
                    }
                } else {
                    return OnLongEnd(pos1.moveIn(direction), pos2.moveIn(direction))
                }
            } else {
                if (direction == Direction.LEFT || direction == Direction.RIGHT) {
                    if (direction == Direction.RIGHT) {
                        val biggerX = maxOf(pos1, pos2) { a, b -> a.x.compareTo(b.x) }
                        return Upright(biggerX.moveIn(direction))
                    } else {
                        val smallerX = minOf(pos1, pos2) { a, b -> a.x.compareTo(b.x) }
                        return Upright(smallerX.moveIn(direction))
                    }
                } else {
                    return OnLongEnd(pos1.moveIn(direction), pos2.moveIn(direction))
                }
            }
        }
    }

    private enum class Direction(private val dx: Int, private val dy: Int) {
        UP(0, -1),
        DOWN(0, 1),
        LEFT(-1, 0),
        RIGHT(1, 0);

        fun move(v: Vec2): Vec2 = Vec2(v.x + dx, v.y + dy)
    }

    private data class Vec2(val x: Int, val y: Int) {
        fun moveIn(direction: Direction): Vec2 {
            return direction.move(this)
        }
    }
}
_________________________________
package kata

object Blox {
    fun bloxSolver(puzzle:Array<String>): String {
        val isItAvailable: (Int, Int) -> Boolean = { x, y -> puzzle.isItAvailable(x, y) }
        val start = StandingPosition(puzzle.startPoint(), isItAvailable)!!
        val end = StandingPosition(puzzle.endPoint(), isItAvailable)!!
        val visitedFromMap = hashMapOf<Position, Direction>()
        val queue : MutableList<Position> = mutableListOf(start)
        
        while (queue.size > 0) {
            val poll = queue.removeFirst()
            val allNextPossiblePositions = poll.allNextPossiblePositions(isItAvailable)
            allNextPossiblePositions.forEach {(direction, nextPosition) ->
                if(!visitedFromMap.contains(nextPosition)) {
                    visitedFromMap[nextPosition] = direction
                    queue.add(nextPosition)
                }
            }
        }
        if(visitedFromMap[end] == null) return ""
        var currentPosition = end
        val path = mutableListOf<Direction>()
        while (currentPosition != start) {
            val direction = visitedFromMap[currentPosition]!!
            currentPosition = currentPosition.back(direction)
            path.add(direction)
        }
        return path.reversed().map { it.char }.joinToString("")
    }
}

enum class Direction(val char: Char) {
    UP('U'), RIGHT('R'), DOWN('D'), LEFT('L');
}

fun Array<String>.isItAvailable(x: Int, y: Int): Boolean {
    if (x < 0 || y < 0) return false
    if (x > first().lastIndex || y > lastIndex) return false
    return this[y][x] != '0'
}

fun Array<String>.startPoint(): Pair<Int, Int> = find('B')
fun Array<String>.endPoint(): Pair<Int, Int> = find('X')
fun Array<String>.find(char: Char): Pair<Int, Int> {
    for ((y, row) in this.withIndex()) {
        val x = row.indexOf(char)
        if (x != -1) return x to y
    }
    return -1 to -1
}

interface Position {

    fun allNextPossiblePositions(isItAvailable: (x: Int, y: Int) -> Boolean) =
        Direction.values().mapNotNull {
            val position = move(it, isItAvailable)
            if (position == null) null else it to position
        }

    fun move(direction: Direction, isItAvailable: (x: Int, y: Int) -> Boolean): Position?

    fun back(direction: Direction) : Position = when(direction) {
        Direction.UP -> move(Direction.DOWN) { _, _ -> true }
        Direction.RIGHT -> move(Direction.LEFT) { _, _ -> true }
        Direction.DOWN -> move(Direction.UP) { _, _ -> true }
        Direction.LEFT -> move(Direction.RIGHT) { _, _ -> true }
    }!!
}

data class StandingPosition private constructor(private val x: Int, private val y: Int) : Position {
    override fun move(direction: Direction, isItAvailable: (x: Int, y: Int) -> Boolean) =
        when (direction) {
            Direction.UP -> VerticalPosition(x, y - 2, isItAvailable)
            Direction.RIGHT -> HorizontalPosition(x + 1, y, isItAvailable)
            Direction.DOWN -> VerticalPosition(x, y + 1, isItAvailable)
            Direction.LEFT -> HorizontalPosition(x - 2, y, isItAvailable)
        }

    companion object {
        operator fun invoke(point: Pair<Int, Int>, isItAvailable: (x: Int, y: Int) -> Boolean): Position? =
            invoke(point.first, point.second, isItAvailable)

        operator fun invoke(x: Int, y: Int, isItAvailable: (x: Int, y: Int) -> Boolean): Position? =
            if (isItAvailable(x, y)) StandingPosition(x, y) else null
    }
}

/*
[x,y]
[x,y+1] 
*/
data class VerticalPosition private constructor(private val x: Int, private val y: Int) : Position {
    override fun move(direction: Direction, isItAvailable: (x: Int, y: Int) -> Boolean) =
        when (direction) {
            Direction.UP -> StandingPosition(x, y - 1, isItAvailable)
            Direction.RIGHT -> VerticalPosition(x + 1, y, isItAvailable)
            Direction.DOWN -> StandingPosition(x, y + 2, isItAvailable)
            Direction.LEFT -> VerticalPosition(x - 1, y, isItAvailable)
        }

    companion object {
        operator fun invoke(x: Int, y: Int, isItAvailable: (x: Int, y: Int) -> Boolean): Position? =
            if (isItAvailable(x, y) && isItAvailable(x, y + 1)) VerticalPosition(x, y) else null
    }
}

/*
  [x,y][x+1,y]
 */
data class HorizontalPosition(private val x: Int, private val y: Int) : Position {
    override fun move(direction: Direction, isItAvailable: (x: Int, y: Int) -> Boolean) =
        when (direction) {
            Direction.UP -> HorizontalPosition(x, y - 1, isItAvailable)
            Direction.RIGHT -> StandingPosition(x + 2, y, isItAvailable)
            Direction.DOWN -> HorizontalPosition(x, y + 1, isItAvailable)
            Direction.LEFT -> StandingPosition(x - 1, y, isItAvailable)
        }

    companion object {
        operator fun invoke(x: Int, y: Int, isItAvailable: (x: Int, y: Int) -> Boolean): Position? =
            if (isItAvailable(x, y) && isItAvailable(x + 1, y)) HorizontalPosition(x, y) else null
    }
}
