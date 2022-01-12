import java.util.*

fun loopSize(n: Node): Int {
  // floyd's
  var tortoise = n.next
  var hare = n.next?.next
  
  while (hare != tortoise) {
    tortoise = tortoise?.next
    hare = hare?.next?.next
  }
  
  var lamda = 1
  hare = tortoise?.next
  while (tortoise != hare) {
    hare = hare?.next
    lamda = lamda + 1
  }
  
    return lamda
}

_____________________________________________
import java.util.*

fun loopSize(n: Node): Int {
    var node = n
    val nodes = HashMap<Node, Int>()
    var count = 0
    while (!nodes.contains(node)) {
        nodes.put(node, count)
        count = count + 1
        node = node.next as Node
    }
    return count - (nodes.get(node) ?: 0) // do it!
}
_____________________________________________
import java.util.*
import java.io.*

fun loopSize(node: Node?) = with(LinkedHashSet<Node?>()) {
    var n = node
    while (add(n)) n = n?.next
    size - takeWhile { it != n }.count()
}
_____________________________________________
import java.util.*

fun loopSize(n: Node?): Int {
    val list = ArrayList<Node?>()
    var n = n
    while(!list.contains(n)){
        list.add(n)
        n = n?.next
    }
    return list.size-list.indexOf(n)
}
_____________________________________________
import java.util.*


fun loopSize(node: Node): Int {
    val startOfLoop = findStartOfLoop(node)
    var sizeOfLoop = 1
    var current = startOfLoop

    while (current != null && startOfLoop != current.next) {
        current = current.next
        sizeOfLoop++
    }

    return sizeOfLoop
}

fun findStartOfLoop(node: Node): Node? {
    val visited = mutableSetOf<Node>(node)
    var current = node.next

    while (current != null && !visited.contains(current)) {
        visited.add(current)
        current = current.next
    }
    return current
}
_____________________________________________
import java.util.*

fun loopSize(n: Node): Int {
    var slow = n
    var fast = n.next!!
    var firstCollision = true
    var count = 0
    while(true){
        slow = slow.next!!
        fast = fast.next!!.next!!
        if(!firstCollision){
            count ++
        }
        if( slow == fast){
            if(!firstCollision) break
            firstCollision = false
        }
    }
    
    return count   // do it!
}
