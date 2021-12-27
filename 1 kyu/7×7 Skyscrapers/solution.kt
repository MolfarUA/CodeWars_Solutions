object Skyscrapers {
    fun solvePuzzle(clues: IntArray): Array<IntArray> = Board(clues).solve()

    class Board(
        private val clueData: IntArray,
        cellData: Array<Array<List<Int>>>? = null
    ) {
        private val size = clueData.size / 4
        private val cells = if (cellData == null) {
            Array(size) { Array(size) { Cell(size) } }
        }
        else {
            Array(size) { y ->
                Array(size) { x ->
                    Cell(cellData[y][x])
                }
            }
        }
        private val clues: Array<ClueRow>
        private var firstTime = cellData == null

        init {
            //Link up cells and clues
            val clues = ArrayList<ClueRow>()
            for (i in 0 until size) {
                val cells0 = ArrayList<Cell>()
                val cells1 = ArrayList<Cell>()
                for (j in 0 until size) {
                    cells0.add(cells[i][j])
                    cells1.add(cells[j][i])
                }

                clues.add(
                    ClueRow(
                        clueData[4 * size - i - 1],
                        clueData[size + i],
                        cells0.toTypedArray()
                    )
                )

                clues.add(
                    ClueRow(
                        clueData[i],
                        clueData[3 * size - i - 1],
                        cells1.toTypedArray()
                    )
                )
            }

            this.clues = clues.toTypedArray()
        }
        
        val output get() = cells.map { it.map { cell -> cell.possible[0] + 1 }.toIntArray() }.toTypedArray()

        fun solve(): Array<IntArray> {
            while (cells.any { it.any {cell -> !cell.solved }}) {
                for (clue in clues) {
                    clue.deduce(firstTime)
                }

                firstTime = false

                //Prioritise doing this as it is far quicker than deducing!
                while (clues.any { it.shouldFindNakedSingles} ) {
                    for (clue in clues) {
                        clue.findNakedSingles()
                    }
                }

                if (!clues.any { it.shouldFindNakedSingles || it.shouldDeduce }) {
                    //This is really expensive so only do it if we get stuck
                    //Damn you MedVed!
                    return bifurcate()
                }
            }

            return output
        }

        private fun bifurcate(): Array<IntArray> {
            //Find a cell with the fewest possibilities on which to bifurcate
            var minimum = size
            var cellToBifurcate: Cell? = null
            cells.forEach {
                it.forEach { cell ->
                    val size = cell.possible.size
                    if (size in 2 until minimum) {
                        cellToBifurcate = cell
                        minimum = size
                    }
                }
            }

            //Check all of the options for the bifurcated cell and hopefully only one will not cause a contradiction!
            val solutions = ArrayList<Array<IntArray>>()
            for (i in 0 until minimum) {
                val bifurcatedData = cells.map {
                    it.map { cell ->
                        if (cell != cellToBifurcate) {
                            cell.possible
                        } else {
                            listOf(cell.possible[i])
                        }
                    }.toTypedArray()
                }.toTypedArray()
                val bifurcatedBoard = Board(clueData, bifurcatedData)
                bifurcatedBoard.firstTime = false
                try {
                    solutions.add(bifurcatedBoard.solve())
                }
                catch (e: Exception) {
                    //We found a contradiction!
                }
            }

            if (solutions.size != 1) {
                //Both options are valid?!
                throw Exception("Fuck. Back to the drawing board!")
            }

            return solutions[0]
        }
    }

    class Cell(var possible: List<Int>) {
        constructor(size: Int): this((0 until size).toList())

        val solved get() = possible.size == 1
        val size get() = possible.size

        val clues = ArrayList<ClueRow>()

        operator fun get(n: Int) = possible[n]

        fun prune(possibilities: Array<Boolean>, source: ClueRow) {
            val new = possible.filter { possibilities[it] }

            if (new.size != possible.size) {
                clues.forEach {
                    it.shouldFindNakedSingles = true
                    if (it != source) {
                        it.shouldDeduce = true
                    }
                }
            }

            possible = new
        }

        fun set(n: Int, source: ClueRow): Boolean {
            if (solved) return false
            possible = arrayListOf(n)
            clues.forEach {
                it.shouldDeduce = true
                if (it != source) {
                    it.shouldFindNakedSingles = true
                }
            }
            return true
        }

        fun remove(i: Int, source: ClueRow) {
            if (possible.contains(i)) {
                possible = possible.filter { it != i }
                clues.forEach {
                    it.shouldDeduce = true
                    if (it != source) {
                        it.shouldFindNakedSingles = true
                    }
                }
            }
        }

        fun contains(n: Int) = possible.contains(n)
    }

    class ClueRow(
        private val startClue: Int,
        private val endClue: Int,
        private val cells: Array<Cell>
    ) {
        private val size = cells.size

        var shouldDeduce = true
        var shouldFindNakedSingles = true

        val consider = IntArray(size)
        private val indices = IntArray(size)
        private val possibilities = Array(size) { Array(size) { false } }

        init {
            cells.forEach {
                it.clues.add(this)
            }
        }

        fun deduce(firstTime: Boolean) {
            if (!shouldDeduce) return
            if (firstTime && startClue == 0 && endClue == 0) return
            reset()
            var i = 0
            while (i < size) {
                check()
                i = 0
                indices[i] += 1
                while (indices[i] == cells[i].size) {
                    for (j in 0..i) {
                        indices[j] = 0
                    }
                    i += 1
                    if (i == size) break
                    indices[i] += 1
                }
            }

            prune()
            shouldDeduce = false
        }

        private fun check() {
            for (i in 0 until size) {
                consider[i] = cells[i][indices[i]]
            }

            for (i in 0 until size) {
                for (j in i+1 until size) {
                    if (consider[i] == consider[j]) return
                }
            }

            if (startClue != 0) {
                var count = 1
                var highest = consider[0]
                for (i in 1 until size) {
                    if (consider[i] > highest) {
                        highest = consider[i]
                        count += 1
                    }
                }
                if (count != startClue) return
            }

            if (endClue != 0) {
                var count = 1
                var highest = consider[size - 1]
                for (i in size - 2 downTo 0) {
                    if (consider[i] > highest) {
                        highest = consider[i]
                        count += 1
                    }
                }
                if (count != endClue) return
            }

            for (i in 0 until size) {
                possibilities[i][consider[i]] = true
            }
        }

        private fun reset() {
            for (i in 0 until size) {
                indices[i] = 0
                for (j in 0 until size ) {
                    possibilities[i][j] = false
                }
            }
        }

        private fun prune() {
            for (i in 0 until size) {
                cells[i].prune(possibilities[i], this)
            }
        }

        fun findNakedSingles() {
            if (!shouldFindNakedSingles) return
            shouldFindNakedSingles = false

            for (i in 0 until size) {
                val cells = cells.filter{ it.contains(i) }
                if (cells.size != 1) continue
                if (cells[0].set(i, this)) {
                    cells.forEach {
                        if (it != cells[0]) {
                            it.remove(i, this)
                        }
                    }
                }
            }
        }
    }
}
______________________________________________________________
object Skyscrapers {
    fun solvePuzzle(clues: IntArray): Array<IntArray> {
        return SkyscrapersSolver.solvePuzzle(clues)
    }
}

const val N = 7
//const val N = 4
//const val N = 3

typealias List2D<T> = List<List<T>>

fun <T> createList2D(rows: Int, columns: Int, fieldInit: (Int, Int) -> T): List2D<T> =
        List(rows) {row ->
            List(columns) {column ->
                fieldInit(row, column)
            }
        }

fun <T> MutableSet<T>.clone(): MutableSet<T> {
    val original = this
    return mutableSetOf<T>().apply { addAll(original) }
}

fun List<MutableSet<Int>>.clone(): List<MutableSet<Int>> =
        List(this.size){this[it]}.map { it.clone() }

// r and c can be 0..N-1
class SkyscraperField(private val rowPermutationNums: MutableList<Int>,
                      private val columnPermutationNums: MutableList<Int>) {

    constructor(n: Int):
            this(MutableList<Int>(n){factorial(n-1)},
                    MutableList<Int>(n){factorial(n-1)})

    fun removeRow(height: Int): Int {
        val ix = height-1
        return --rowPermutationNums[ix]
    }

    fun removeColumn(height: Int): Int {
        val ix = height-1
        return --columnPermutationNums[ix]
    }

    fun clone(): SkyscraperField {
        return SkyscraperField(rowPermutationNums, columnPermutationNums)
    }
}

enum class Status {
    SOLVED, SOLVING, UNSOLVABLE
}

class Skyscrapers2(private val fields: List2D<SkyscraperField>,
                   private val rowPermutations: List<MutableSet<Int>>,
                   private val columnPermutations: List<MutableSet<Int>>) {

    enum class Alignment {
        ROW, COLUMN
    }

    private val toRemove = mutableSetOf<Triple<Alignment, Int, Int>>()

    constructor(n: Int):
            this(createList2D(n, n) {_, _ -> SkyscraperField(n)},
                    MutableList<MutableSet<Int>>(n) {Permutations.all.clone()},
                    MutableList<MutableSet<Int>>(n) {Permutations.all.clone()})

    fun clone(): Skyscrapers2 {
        return Skyscrapers2(
                createList2D(fields.size, fields.size){i: Int, j: Int -> fields[i][j].clone()},
                rowPermutations.clone(),
                columnPermutations.clone())
    }

    fun removeRow(field: Int, pix: Int) {
        scheduleRemoveRow(field, pix)
        remove()
    }

    fun removeColumn(field: Int, pix: Int) {
        scheduleRemoveColumn(field, pix)
        remove()
    }

    private fun scheduleRemoveRow(field: Int, pix: Int) {
        toRemove.add(Triple(Alignment.ROW, field, pix))
    }

    private fun scheduleRemoveColumn(field: Int, pix: Int) {
        toRemove.add(Triple(Alignment.COLUMN, field, pix))
    }

    private fun remove() {
        while (toRemove.isNotEmpty()) {
            val next = toRemove.first()
            when (next.first) {
                Alignment.ROW -> doRemoveRow(next.second, next.third)
                Alignment.COLUMN -> doRemoveColumn(next.second, next.third)
            }
            toRemove.remove(next)
        }
    }

    private fun doRemoveRow(rowIx: Int, pix: Int) {
        if (pix in rowPermutations[rowIx]) {
            rowPermutations[rowIx].remove(pix)
            for (columnIx in columnPermutations.indices) {
                val h = Permutations.index[pix]!![columnIx]
                if (fields[rowIx][columnIx].removeRow(h)<=0) {
                    val columnPermutationsToRemove =
                            columnPermutations[columnIx].intersect(
                                    Permutations.nx[Pair(rowIx, h)]?:listOf())
                    for (p in columnPermutationsToRemove) {
                        scheduleRemoveColumn(columnIx, p)
                    }
                }
            }
        }
    }

    private fun doRemoveColumn(columnIx: Int, pix: Int) {
        if (pix in columnPermutations[columnIx]) {
            columnPermutations[columnIx].remove(pix)
            for (rowIx in rowPermutations.indices) {
                val h = Permutations.index[pix]!![rowIx]
                if (fields[columnIx][rowIx].removeColumn(h)<=0) {
                    val rowPermutationsToRemove =
                            rowPermutations[rowIx].intersect(
                                    Permutations.nx[Pair(columnIx, h)]?:listOf())
                    for (p in rowPermutationsToRemove) {
                        scheduleRemoveRow(rowIx, p)
                    }
                }
            }
        }
    }

    fun status(): Status {
        if (rowPermutations.any{ it.size == 0 } or columnPermutations.any{it.size == 0}) {
            return Status.UNSOLVABLE
        }
        if (rowPermutations.all{ it.size == 1 }) {
            return Status.SOLVED
        }
        return  Status.SOLVING
    }

    fun split(): Pair<Int,MutableSet<Int>> {
        val splitRowIx = rowPermutations.indexOfFirst { it.size>1 }
        return Pair(splitRowIx, rowPermutations[splitRowIx].clone())
    }

    fun result(): Array<IntArray> {
        val r = Array(fields.size) { intArrayOf() }
        for (i in fields[0].indices) {
            r[i] = (Permutations.index[rowPermutations[i].first()]
                    ?: listOf()).toIntArray()
        }
        return r
    }
}

object SkyscrapersSolver {

    fun solvePuzzle(clues: IntArray): Array<IntArray> {
        val s = Skyscrapers2(N)
        applyClues(s, clues)
        val s1 = reduce(s)
        return s1.result()
    }

    private fun applyClues(s: Skyscrapers2, clues: IntArray) {
        for (i in 0 until 4 * N) {
            if (clues[i] == 0) {
                continue
            }
            when (i / N) {
                0 ->
                    for (pix in Permutations.leftNot[clues[i]]!!) {
                        s.removeColumn(i % N, pix)
                    }
                1 ->
                    for (pix in Permutations.rightNot[clues[i]]!!) {
                        s.removeRow(i % N, pix)
                    }
                2 ->
                    for (pix in Permutations.rightNot[clues[i]]!!) {
                        s.removeColumn(N - i % N - 1, pix)
                    }
                3 ->
                    for (pix in Permutations.leftNot[clues[i]]!!) {
                        s.removeRow(N - i % N - 1, pix)
                    }
            }
        }
    }

    private fun reduce(s: Skyscrapers2): Skyscrapers2 {
        if (s.status() == Status.SOLVING) {
            val (rowIx, pixs) = s.split()
            for (pix in pixs) {
                var s1 = s.clone()
                s1.removeRow(rowIx, pix)
                s1 = reduce(s1)
                if (s1.status() == Status.SOLVED) {
                    return s1
                }
            }
        }
        return s
    }
}


object Permutations {
    val index = HashMap<Int,List<Int>>()
    val all = (1..factorial(N)).toMutableSet()
    val leftNot = HashMap<Int,MutableSet<Int>>()
    val rightNot = HashMap<Int,MutableSet<Int>>()
    // (n, x) -> the permutations whose nth element is x
    // n in 0..N-1, x in 1..N
    val nx = HashMap<Pair<Int, Int>,MutableSet<Int>>()

    init {
        initPermutations()
        initViews()
    }

    private fun initPermutations() {
        var ix = 0
        for (p in permutation((1..N).toSet())) {
            index[++ix] = p
        }
    }

    private fun initViews() {
        val noPermutations = mutableSetOf<Int>()
        for (i in 1..N) {
            leftNot[i] = all.clone()
            rightNot[i] = all.clone()
            for (j in 1..N) {
                nx[Pair(i-1, j)] = noPermutations.clone()
            }
        }
        for ((pix, p) in index) {
            val leftCount = count(p)
            val rightCount = count(p.reversed())
            leftNot[leftCount]?.remove(pix)
            rightNot[rightCount]?.remove(pix)
            for (i in 0 until N) {
                nx[Pair(i, p[i])]?.add(pix)
            }
        }
    }
}

fun factorial(n: Int): Int {
    var p = 1
    for (i in 1..n) {
        p*=i
    }
    return p
}

// count the visible towers
fun count(towers: List<Int>) =
        towers.fold(Pair(0,0)){
            (max, n), k ->
            if (k>max) {
                Pair(k, n+1)
            } else {
                Pair(max, n)
            }
        }.second

fun <T> permutation(elements: Set<T>): Sequence<MutableList<T>> =
        sequence {
            if (elements.isNotEmpty()) {
                for (e in elements) {
                    val elements1 = HashSet<T>().apply{addAll(elements)}
                    elements1.remove(e)
                    val p1 = permutation(elements1)
                    for (p in p1) {
                        p.add(e)
                        yield(p)
                    }
                }
            } else {
                yield(mutableListOf())
            }
        }
        
________________________________________________________
@file:Suppress("NOTHING_TO_INLINE")

const val SIZE = 7
const val FULL_CELL = (1L shl SIZE) - 1
const val FULL_ROW = (1L shl (SIZE * SIZE)) - 1

// This should really be inline class with Kotlin 1.3
data class Mask(val value: Long) {
    inline val isEmpty: Boolean get() = value == 0L

    inline infix fun intersect(other: Mask): Mask {
        return Mask(this.value and other.value)
    }

    inline infix fun union(other: Mask): Mask {
        return Mask(this.value or other.value)
    }

    inline infix fun diff(other: Mask): Mask {
        return Mask(this.value and other.value.inv())
    }

    inline fun getCell(index: Int): Long {
        val right = (SIZE - index - 1) * SIZE
        return value shr right and FULL_CELL
    }

    inline fun getPerm(): IntArray {
        val nums = IntArray(SIZE)
        for (i in 0 until SIZE) {
            val cellMask = this.getCell(i)
            nums[i] = if (cellMask == 0L) {
                0
            } else {
                java.lang.Long.numberOfTrailingZeros(cellMask) + 1
            }
        }
        return nums
    }

    companion object {
        val EMPTY = Mask(0L)
        val FULL = Mask(FULL_ROW)

        inline fun from(f: (Int) -> Long): Mask {
            var mask: Long = 0
            for (j in 0 until SIZE) {
                mask = (mask shl SIZE) + f(j)
            }
            return Mask(mask)
        }
    }
}

internal inline fun Array<Mask>.transpose(): Array<Mask> {
    return Array(SIZE) { i -> Mask.from { j -> this[j].getCell(i) } }
}

internal class Permutation(val nums: IntArray) {
    val leftClue: Int
    val rightClue: Int
    val mask: Mask

    init {
        this.leftClue = calcClue(nums, 1)
        this.rightClue = calcClue(nums, -1)
        this.mask = calcMask(nums)
    }

    override fun toString(): String {
        val ns = StringBuilder()
        for (n in nums) {
            ns.append(n)
        }
        return "Permutation{" +
                "nums=" + ns.toString() +
                ", leftClue=" + leftClue +
                ", rightClue=" + rightClue +
                ", value=" + mask +
                '}'.toString()
    }

    companion object {
        fun calcClue(nums: IntArray, dir: Int): Int {
            var last = 0
            val end = if (dir == 1) nums.size else -1
            val start = if (dir == 1) 0 else nums.size - 1
            var clue = 0
            var i = start
            while (i != end) {
                if (nums[i] > last) {
                    last = nums[i]
                    clue++
                }
                i += dir
            }
            return clue
        }

        fun calcMask(nums: IntArray): Mask {
            var mask: Long = 0
            for (i in nums.indices) {
                val bit = nums[i] - 1
                mask = mask shl nums.size or (1L shl bit)
            }
            return Mask(mask)
        }

        fun genAll(size: Int): Array<Permutation> {
            val all = arrayListOf<Permutation>()
            val nums = IntArray(size)
            val used = BooleanArray(size)
            fun search(depth: Int) {
                if (depth == size) {
                    all.add(Permutation(nums.clone()))
                    return
                }
                for (i in 0 until size) {
                    if (!used[i]) {
                        used[i] = true
                        nums[depth] = i + 1
                        search(depth + 1)
                        used[i] = false
                    }
                }
            }
            search(0)
            return all.toTypedArray()
        }
    }
}

internal class PermutationClues(all: Array<Permutation>) {
    val byClue = run {
        val index = hashMapOf<Pair<Int, Int>, Pair<Mask, ArrayList<Mask>>>()
        for (perm in all) {
            for (key in arrayOf(
                    Pair(perm.leftClue, perm.rightClue),
                    Pair(0, perm.rightClue),
                    Pair(perm.leftClue, 0),
                    Pair(0, 0)
            )) {
                val (bound, list) = index.getOrPut(key) { Pair(Mask.EMPTY, arrayListOf()) }
                list.add(perm.mask)
                index[key] = Pair(bound union perm.mask, list)
            }
        }
        index
    }

    inline fun getBound(leftClue: Int, rightClue: Int): Mask =
            byClue[Pair(leftClue, rightClue)]?.first ?: Mask.EMPTY

    inline fun getChoices(leftClue: Int, rightClue: Int): List<Mask>? =
            byClue[Pair(leftClue, rightClue)]?.second
}

object Skyscrapers {
    private var permutations = Permutation.genAll(SIZE)
    private var permByClues = PermutationClues(permutations)

    private fun search(
            depth: Int,
            rows: Array<Mask>, cols: Array<Mask>,
            rowBounds: Array<Mask>, colBounds: Array<Mask>,
            clues: IntArray
    ): Boolean {
        if (depth == 2 * SIZE) {
            return true
        }

        var rb = rowBounds.clone()
        var cb = colBounds.clone()

        do {
            var changed = false
            for (i in 0 until SIZE) {
                val leftClue = clues[4 * SIZE - i - 1]
                val rightClue = clues[SIZE + i]
                (rb[i] intersect permByClues.getBound(leftClue, rightClue)).let {
                    if (it != rb[i]) {
                        changed = true
                    }
                    rb[i] = it
                }

                val upClue = clues[i]
                val downClue = clues[3 * SIZE - i - 1]
                (cb[i] intersect permByClues.getBound(upClue, downClue)).let {
                    if (it != cb[i]) {
                        changed = true
                    }
                    cb[i] = it
                }
            }

            rb = cb.transpose().run { Array(SIZE) { i -> rb[i] intersect this[i] } }
            cb = rb.transpose()
        } while (changed)

        var bestRow = -1
        var bestCol = -1
        var bestChoices: List<Mask>? = null
        for (i in 0 until SIZE) {
            if (rows[i].isEmpty) {
                val leftClue = clues[4 * SIZE - i - 1]
                val rightClue = clues[SIZE + i]
                val choices = permByClues.getChoices(leftClue, rightClue)?.filter { it union rb[i] == rb[i] }
                if (bestChoices == null || choices != null && choices.size < bestChoices.size) {
                    bestRow = i
                    bestCol = -1
                    bestChoices = choices
                }
            }
            if (cols[i].isEmpty) {
                val upClue = clues[i]
                val downClue = clues[3 * SIZE - i - 1]
                val choices = permByClues.getChoices(upClue, downClue)?.filter { it union cb[i] == cb[i] }
                if (bestChoices == null || choices != null && choices.size < bestChoices.size) {
                    bestRow = -1
                    bestCol = i
                    bestChoices = choices
                }
            }
        }

        if (bestChoices == null) {
            return false
        }

        if (bestRow != -1) {
            for (mask in bestChoices) {
                rows[bestRow] = mask
                val newRowBounds = Array(SIZE) { i -> if (i == bestRow) mask else rb[i] diff mask }
                if (search(depth + 1, rows, cols, newRowBounds, cb, clues)) {
                    return true
                }
                rows[bestRow] = Mask.EMPTY
            }
        } else {
            for (mask in bestChoices) {
                cols[bestCol] = mask
                val newColBounds = Array(SIZE) { i -> if (i == bestCol) mask else cb[i] diff mask }
                if (search(depth + 1, rows, cols, rb, newColBounds, clues)) {
                    return true
                }
                cols[bestCol] = Mask.EMPTY
            }
        }
        return false
    }

    fun solvePuzzle(clues: IntArray): Array<IntArray> {
        val rows = Array(SIZE) { Mask.EMPTY }
        val cols = Array(SIZE) { Mask.EMPTY }
        assert(search(
                0,
                rows = rows,
                cols = cols,
                rowBounds = Array(SIZE) { Mask.FULL },
                colBounds = Array(SIZE) { Mask.FULL },
                clues = clues
        ))

        return Array(SIZE) { i -> rows[i].getPerm() }
    }
}
