5993c1d917bc97d05d000068



import java.util.HashMap
import java.util.HashSet

private fun generateRegex(n: Int): String {
    if (n == 1) return "1[01]*"
    val states = HashSet<Int>()
    states += 0 until n
    val dfa = DFA(states, 0, arrayOf(0))
    for (i in 0 until n) {
        dfa.addTransition(i, i * 2 % n, "0")
        dfa.addTransition(i, (i * 2 + 1) % n, "1")
    }
    return dfa.reduce()
}

fun regexDivisibleBy(n: Int): String {
    var n = n
    val start = "^(0|"
    var end = ")$"
    while (n % 2 == 0) {
        end = "0" + end
        n /= 2
    }
    return String.format("%s%s%s", start, generateRegex(n), end)
}

internal class Transition(var from: Int, var to: Int) : Comparable<Transition> {
    override fun equals(other: Any?): Boolean {
        if (other is Transition) {
            val otherTrans = other as Transition?
            return this.from == otherTrans!!.from && this.to == otherTrans.to
        }
        return false
    }

    override operator fun compareTo(other: Transition): Int {
        val compare = this.from.compareTo(other.from)
        return if (compare == 0) this.to.compareTo(other.to) else compare
    }

    override fun toString(): String {
        return String.format("(from: %d, to: %d)", this.from, this.to)
    }
}

internal class DFA(private val states: HashSet<Int>, startState: Int, acceptedStates: Array<Int>) {
    private val START_STATE = -1
    private val END_STATE = -2
    private val transitions: HashMap<Transition, String> = hashMapOf()

    init {
        this.addTransition(START_STATE, startState, "")
        for (acceptedState in acceptedStates) {
            this.addTransition(acceptedState, END_STATE, "")
        }
    }

    fun addTransition(from: Int, to: Int, transition: String) {
        this.transitions.put(Transition(from, to), transition)
    }

    private fun selectState(): Int {
        val fromCount = HashMap<Int, Int>()
        val toCount = HashMap<Int, Int>()
        for (transition in this.transitions.keys) {
            if (transition.from != transition.to) {
                var currentCount = (fromCount as MutableMap<Int, Int>).getOrDefault(transition.from, 0)
                fromCount.put(transition.from, currentCount + 1)
                currentCount = (toCount as MutableMap<Int, Int>).getOrDefault(transition.to, 0)
                toCount.put(transition.to, currentCount + 1)
            }
        }
        var minState = 0
        var minBranches = 999
        for (state in this.states) {
            val from = (fromCount as MutableMap<Int, Int>).getOrDefault(state, 0)
            val to = (toCount as MutableMap<Int, Int>).getOrDefault(state, 0)
            val branches = from * to
            if (branches < minBranches) {
                minState = state
                minBranches = branches
            }
        }
        return minState
    }

    private fun removeState(state: Int?) {
        val enteringTrans = HashMap<Int, String>()
        val exitingTrans = HashMap<Int, String>()
        var loop = ""
        var hasLoop = false
        var keys = HashSet(this.transitions.keys)
        for (trans in keys) {
            if (trans.from == trans.to && trans.from == state) {
                loop = this.transitions[trans]!!
                hasLoop = true
            } else if (trans.from == state) {
                exitingTrans.put(trans.to, this.transitions[trans]!!)
            } else if (trans.to == state) {
                enteringTrans.put(trans.from, this.transitions[trans]!!)
            }
            if (trans.from == state || trans.to == state) {
                this.transitions.remove(trans)
            }
        }
        if (hasLoop) {
            loop = String.format("(%s)*", loop)
        }
        for (enterState in enteringTrans.keys) {
            val enteringString = enteringTrans[enterState]
            for (exitState in exitingTrans.keys) {
                val exitingString = exitingTrans[exitState]

                var existingTrans: String? = null
                var hasExistingTrans = false
                keys = HashSet(this.transitions.keys)
                for (trans in keys) {
                    if (trans.from == enterState && trans.to == exitState) {
                        existingTrans = this.transitions[trans]
                        hasExistingTrans = true
                        this.transitions.remove(trans)
                    }
                }

                var newTrans = String.format("%s%s%s", enteringString, loop, exitingString)
                if (hasExistingTrans) {
                    newTrans = String.format("(%s|%s)", existingTrans, newTrans)
                }
                this.addTransition(enterState, exitState, newTrans)
            }
        }
        this.states.remove(state)
    }

    fun reduce(): String {
        while (this.states.size > 0) {
            val state = this.selectState()
            this.removeState(state)
        }
        var result = ""
        for (trans in this.transitions.keys) {
            result = this.transitions[trans]!!
        }
        return result
    }
}
_____________________________________________
fun String?.star() = if (this === null) "" else "($this)*"
infix fun String?.and(x: String?) = this ?.let { a -> x?.let { "($a)($it)" }}
infix fun String?.or(x: String?) =
    when {
        this === null -> x
        x === null -> this
        else -> "($this)|($x)"
    }

fun regexDivisibleBy(m: Int): String {
    if (m == 1) return "[01]*"
    val b = Array<String?>(m) { null }
    val a = Array<String?>(m * m) { null }

    operator fun Array<String?>.get(a: Int, b: Int) = this[a * m + b]
    operator fun Array<String?>.set(a: Int, b: Int, s: String?) { this[a * m + b] = s }

    b[0] = ""

    for (i in 0..(m-1)) {
        a[i, i * 2 % m] = "0"
        a[i, (i * 2 + 1) % m] = "1"
    }

    for (n in (m - 1) downTo 0) {
        b[n] = a[n, n].star() and b[n]
        for (j in 0..n) {
            a[n, j] = a[n, n].star() and a[n, j]
        }
        for (i in 0..n) {
            b[i] = b[i] or (a[i, n] and b[n])
            for (j in 0..n) {
                a[i, j] = a[i, j] or (a[i, n] and a[n, j])
            }
        }
    }

    return b[0]!!
}
_____________________________________________
fun regexDivisibleBy(n: Int): String 
{
    if (n == 1) return "^[01]*$";
    var graphs = Array(n, {i -> Array(n, {j -> "-1"})});
    for (i in 0..(n - 1))
    {
        graphs[i][(2 * i) % n] = "0";
        graphs[i][(2 * i + 1) % n] = "1";
    }
    for (k in (n - 1) downTo 0)
    {
        val loop = if (graphs[k][k] == "-1" ) "" else (graphs[k][k] + "*");
        for (i in 0..(k - 1))
        {
            if (graphs[i][k] == "-1") continue;
            for (j in 0..(k - 1))
            {
                if (graphs[k][j] == "-1") continue;
                val s = if (graphs[i][j] == "-1" ) "" else (graphs[i][j] + "|");
                graphs[i][j] = "(?:" + s + graphs[i][k] + loop + graphs[k][j] + ")";
            }
        }
    }
    return "^" + graphs[0][0] + "*$";
}
_____________________________________________
sealed class RE
data class Lit(var lit: Any): RE() { override fun toString() = "$lit" }
data class Alter(var res: MutableSet<RE> = mutableSetOf()): RE() {
    override fun toString() = res.joinToString("|", "(", ")")
    fun add(re: RE) { if (re is Alter) res.addAll(re.res) else res.add(re) }
}
data class Concat(var res: MutableList<RE> = mutableListOf()): RE() {
    override fun toString() = res.joinToString("", "(", ")")
    fun add(re: RE) {
        when (re) {
            is Concat -> res.addAll(re.res)
            is Epsilon -> {}
            else -> res.add(re)
        }
    }
}
data class Star(var re: RE): RE() { override fun toString() = "$re*" }
object Epsilon : RE() { override fun toString() = "" }  // a.k.a OneRE
fun makeConcat(vararg res: RE): Concat = Concat().apply { res.forEach { add(it) } }
fun makeAlter(vararg res: RE): Alter = Alter().apply { res.forEach { add(it) } }
fun makeStar(re: RE): RE = if (re is Epsilon || re is Star) re else Star(re)

class GeneralizedNFA(val nState: Int, val starts: Collection<Int>, val accepts: Collection<Int>) {
    private var matrix = MutableList(nState + 1) { MutableList<RE?>(nState + 1) { null } }
    init { // Rows: [0 1 2 .. n_state-1 START], Cols: [0 1 2 .. n_state-1 END]
        starts.forEach  { addTrans(nState, it, Epsilon) }
        accepts.forEach { addTrans(it, nState, Epsilon) }
    }

    fun addTrans(src: Int, dst: Int, re: RE) {
        when (val oldR = matrix[src][dst]) {
            null -> matrix[src][dst] = re
            is Alter -> oldR.add(re)
            else -> matrix[src][dst] = makeAlter(oldR, re)
        }
    }

    fun toRe(): RE {
        for (state in 0 until nState) { /* We want to delete the state `state` here */
            val loopRe = makeStar(matrix[state][state] ?: Epsilon)
            for (src in state+1 .. nState) {
                val srcRe = matrix[src][state] ?: continue
                for (dst in state+1 .. nState) {
                    val dstRe = matrix[state][dst] ?: continue
                    addTrans(src, dst, makeConcat(srcRe, loopRe, dstRe))
                }
            }
        }
        return matrix[nState][nState]!!
    }
}

fun regexDivisibleBy(n: Int): String {
    val m = GeneralizedNFA(n, starts = listOf(0), accepts = listOf(0))
    for (src in 0 until n)
        (0..1).forEach { m.addTrans(src, (src*2 + it) % n, Lit(it.toString(2))) }
    return m.toRe().toString()
}
_____________________________________________
fun regexDivisibleBy(n: Int): String {
  val result = regDivisibleByBasic(n)
  println(result)
  return "^0+|$result$"
}

fun regDivisibleByBasic(n: Int): String {
    // Obvious base case
    if (n == 1) return "[01]*"
    // Obvious recursive case
    if (n % 2 == 0) return "${regDivisibleByBasic(n/2)}0"
    // Non-trivial base case.
    // We construct a Finite State Machine to match binary numbers divisible by n, then convert it to a regular expression.
    // If the FSM is in state S, then that means value of the input so far is equivalent to S mod n.
    // When we munch a new bit, the value of the input so far doubles and increases by the value of the bit.
    // The FSM starts in state 0, and accepts the input if it is in state 0 when the input ends.
    val trans = Array(n) {
        arrayListOf(
            Pair("0", (2*it) % n),
            Pair("1", (2*it+1) % n)
        )
    }
    while (trans[0].size > 1 || trans[0][0].second != 0) {
        if (tryAlternationReduction(trans)) continue
        if (tryLoopReduction(trans)) continue
        removeLastStateConnection(trans)
    }
    return "(${trans[0][0].first})*"
}

// Reduce a pair of transition rules x => s, y => s to a single rule x|y => s
fun tryAlternationReduction(trans: Array<ArrayList<Pair<String, Int>>>): Boolean {
    for (i in 0 until trans.size) {
        val list = trans[i]
        for (j in 0 until list.size) {
            for (k in 0 until list.size) {
                if (j != k && list[j].second == list[k].second) {
                    val (a, to) = list[j]
                    val b = list[k].first
                    list.removeAt(k)
                    list[j] = Pair("($a|$b)", to)
                    return true
                }
            }
        }
    }
    return false
}

// In state s, remove a rule x => s by altering all other rules y => s' to x*y => s'
fun tryLoopReduction(trans: Array<ArrayList<Pair<String, Int>>>): Boolean {
    // skip 0 since that one has the loop we want
    for (i in 1 until trans.size) {
        val list = trans[i]
        for (j in 0 until list.size) {
            val (reg, to) = list[j]
            if (to == i) {
                val reg = if (reg.length == 1) reg else "($reg)"
                list.removeAt(j)
                for (j in 0 until list.size) {
                    val (a, b) = list[j]
                    list[j] = Pair("$reg*$a", b)
                }
                return true
            }
        }
    }
    return false
}

// Removes a transition to the last state somewhere in the FSM.
// Also clears the transitions from unreachable states to avoid unneccessary work
fun removeLastStateConnection(trans: Array<ArrayList<Pair<String, Int>>>) {
    var lastFrom = 0
    var lastIndex= 0
    var lastTo = 0
    for (i in 0 until trans.size) {
        for (j in 0 until trans[i].size) {
            if (trans[i][j].second > lastTo) {
                lastTo = trans[i][j].second
                lastFrom = i
                lastIndex = j
            }
        }
    }
    for (i in lastTo+1 until trans.size)
        trans[i].clear()
    val new = ArrayList<Pair<String, Int>>()
    val reg = trans[lastFrom][lastIndex].first
    for ((a, b) in trans[lastTo]) {
        new.add(Pair("$reg$a", b))
    }
    trans[lastFrom].removeAt(lastIndex)
    trans[lastFrom].addAll(new)
}
