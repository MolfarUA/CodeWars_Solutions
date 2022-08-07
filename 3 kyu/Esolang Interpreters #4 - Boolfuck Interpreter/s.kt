5861487fdb20cff3ab000030


import java.util.*

fun interpret(code: String, inputs: String) = WhatTheBoolfuck().apply {
    val stack = LinkedList<Int>()
    for (i in code.indices) when {
        code[i] == '[' -> stack.push(i)
        code[i] == ']' -> stack.pop().also { put(i, it); put(it, i) }
    }
    input = inputs.flatMap { Iterable { WhatTheBoolfuck(it.toInt()) } }.iterator()
    output = StringBuilder()

    val data = WhatTheBoolfuck()
    var ptr = 0

    var i = 0
    while (i < code.length) {
        when (code[i]) {
            '+' -> data[ptr] = data[ptr] xor 1
            ',' -> data[ptr] = read()
            ';' -> write(data[ptr])
            '>' -> ptr++
            '<' -> ptr--
            '[' -> if (data[ptr] == 0) i = this[i]
            ']' -> if (data[ptr] != 0) i = this[i]
        }
        i++
    }
}.toString()

private class WhatTheBoolfuck(var char: Int = 0, var i: Int = 0) : HashMap<Int, Int>(), Iterator<Int> {
    lateinit var output: StringBuilder
    lateinit var input: Iterator<Int>
    override fun hasNext() = i < 8
    override fun next() = char shr i++ and 1
    override fun get(key: Int) = super.get(key) ?: 0
    override fun toString() = (if (i == 0) output else output.append(char.toChar())).toString()
    fun read() = if (input.hasNext()) input.next() else 0
    fun write(bit: Int) {
        char = char or bit.shl(i++)
        if (!hasNext()) output.append(char.toChar()).also { char = 0;i = 0 }
    }
}
_____________________________
const val INDEX_TO_PAGE_SHIFT = 10
const val PAGE_SIZE = 1 shl INDEX_TO_PAGE_SHIFT
const val PAGE_MASK = PAGE_SIZE - 1

const val COMMAND_FLIP = '+'
const val COMMAND_INPUT = ','
const val COMMAND_OUTPUT = ';'
const val COMMAND_LEFT = '<'
const val COMMAND_RIGHT = '>'
const val COMMAND_BEGIN_BLOCK = '['
const val COMMAND_END_BLOCK = ']'

fun interpret(code: String, input: String): String {
    val codeData = CharData(code)
    val outputData = BitwiseData()
    val inputData = BitwiseData(input)
    val data = BrainData()

    while (codeData.hasNext()) {
        when (codeData.next()) {
            COMMAND_FLIP -> data.flip()
            COMMAND_INPUT -> data.put(inputData.getBit())
            COMMAND_OUTPUT -> outputData.putBit(data.get())
            COMMAND_LEFT -> data.previous()
            COMMAND_RIGHT -> data.next()
            COMMAND_BEGIN_BLOCK -> if (data.isZero()) codeData.seekMatchingBracket(1)
            COMMAND_END_BLOCK -> if (data.isNotZero()) codeData.seekMatchingBracket(-1)
        }
    }
    return outputData.asString()
}

class CharData(private val charArray: CharArray) {
    var index = 0

    constructor(charDataAsString: String) : this(charDataAsString.toCharArray())

    fun next() = charArray[index++]
    fun hasNext() = index < charArray.size

    fun seekMatchingBracket(direction: Int) {
        var nestLevel = 0
        var c = charArray[--index]
        while (true) {
            if (c == COMMAND_END_BLOCK) {
                if (--nestLevel == 0) {
                    return
                }
            } else if (c == COMMAND_BEGIN_BLOCK) {
                if (++nestLevel == 0) {
                    return
                }
            }
            index += direction
            c = charArray[index]
        }
    }

}

class BitwiseData(input: String = "") {
    val listOfBytes = input.indices.map { input.codePointAt(it).toByte() }.toMutableList()
    var bitData = 0
    var bitIndex = 0

    fun putBit(bit: Int) {
        bitData = bitData.or(bit.and(1).shl(bitIndex))
        ++bitIndex
        if (bitIndex.equals(Byte.SIZE_BITS)) {
            listOfBytes.add(bitData.toByte())
            bitData = 0
            bitIndex = 0
        }
    }

    fun getBit(): Int {
        if (bitIndex == 0) {
            bitData = listOfBytes.removeFirstOrNull()?.toInt() ?: 0
        }
        val returnBit = bitData.shr(bitIndex).and(1)
        bitIndex = (bitIndex + 1) % Byte.SIZE_BITS
        return returnBit
    }

    fun asString(): String = mutableListOf<Byte>().apply {
        addAll(listOfBytes)
        if (bitIndex > 0) add(bitData.toByte())
    }.map { Character.toChars((if (it < 0) (256 + it) else it.toInt()))[0] }.joinToString(separator = "")

}

class BrainData {
    private val data = ArrayList<IntArray>(1)
    var lastPageExclusive = 0
    private var dataIndex = 0
    private var bitIndex = 0

    init {
        data.add(IntArray(PAGE_SIZE))
    }

    operator fun next() {
        bitIndex = (bitIndex + 1) % Int.SIZE_BITS
        if (bitIndex % Int.SIZE_BITS == 0) dataIndex++
        if (dataIndex shr INDEX_TO_PAGE_SHIFT >= lastPageExclusive) appendPage()
    }

    fun previous() {
        if (bitIndex % Int.SIZE_BITS == 0) {
            if (dataIndex == 0) prependPage()
            dataIndex--
        }
        bitIndex = (bitIndex - 1 + Int.SIZE_BITS) % Int.SIZE_BITS
    }

    fun flip() {
        data[dataIndex shr INDEX_TO_PAGE_SHIFT][dataIndex and PAGE_MASK] =
            data[dataIndex shr INDEX_TO_PAGE_SHIFT][dataIndex and PAGE_MASK].xor(1 shl bitIndex)
    }

    fun get(): Int {
        return data[dataIndex shr INDEX_TO_PAGE_SHIFT][dataIndex and PAGE_MASK].shr(bitIndex).and(1)
    }

    fun put(i: Int) {
        if (i.and(1) != get()) flip()
    }

    fun isZero() = get() == 0
    fun isNotZero() = !isZero()

    private fun appendPage() {
        data.add(IntArray(PAGE_SIZE))
        lastPageExclusive++
    }

    private fun prependPage() {
        data.add(0, IntArray(PAGE_SIZE))
        lastPageExclusive++
        dataIndex = PAGE_SIZE
    }

}
_____________________________
fun interpret(code: String, inputS: String): String {
    val bitMasks = listOf(0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01).reversed()

    val input = inputS.flatMap { c ->
        bitMasks.map { c.code.and(it) > 0 }
    }

    val matchingBrackets = mutableListOf<Pair<Int, Int>>()
    val jPositions = mutableListOf<Int>()
    for (j in code.indices) {
        if (code[j] == '[') {
            jPositions.add(j)
        }
        if (code[j] == ']') {
            matchingBrackets.add(jPositions.removeLast() to j)
        }
    }

    var (memoryPointer, inputIndex, programIndex) = Triple(0, 0, 0)
    val memory = mutableMapOf<Int, Boolean>()
    val output = mutableListOf<Boolean>()

    while (programIndex < code.length) {
        val c = code[programIndex]
        when (c) {
            '+' -> memory[memoryPointer] = !memory.getOrDefault(memoryPointer, false)
            ',' -> {
                memory[memoryPointer] = if (inputIndex < input.size) {
                    input[inputIndex]
                } else {
                    false
                }
                ++inputIndex
            }
            ';' -> output.add(memory.getOrDefault(memoryPointer, false))
            '<' -> memoryPointer--
            '>' -> memoryPointer++
            '[' -> if (!memory.getOrDefault(memoryPointer, false)) {
                programIndex = matchingBrackets.single { it.first == programIndex }.second
            }
            ']' -> if (memory.getOrDefault(memoryPointer, false)) {
                programIndex = matchingBrackets.single { it.second == programIndex }.first
            }
            else -> {
            }
        }
        ++programIndex
    }

    val padding = if (output.size % 8 != 0) {
        (0 until (8 - (output.size % 8))).map { false }
    } else {
        listOf()
    }
    output.addAll(padding)

    val result = StringBuilder()
    output.chunked(8).forEachIndexed { index , eightBits ->
        val q = eightBits.zip(bitMasks).sumOf { (bit, v) ->
            if (bit) {
                v
            } else {
                0
            }
        }
        result.append(q.toChar())
    }
    return result.toString()
}
