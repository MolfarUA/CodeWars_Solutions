using System.Collections.Generic;

public class Kata{
  public static int getLoopSize(LoopDetector.Node startNode){
    var dict = new Dictionary<LoopDetector.Node, int>();
    int index = 0;
    while (true)
    {
      if (dict.ContainsKey(startNode))
        return index - dict[startNode];
      dict[startNode] = index++;
      startNode = startNode.next;
    }
    return 0;
  }
}
_____________________________________________
public class Kata{
  public static int getLoopSize(LoopDetector.Node node){
    LoopDetector.Node slow = node;
    LoopDetector.Node fast = node.next;
        
    while(fast != slow){
        slow = slow.next;
        fast = fast.next.next;
    }
    
    fast = fast.next;
    int steps = 1;
    while(fast != slow){
        fast = fast.next;
        steps += 1;
    }
    
    return steps;
  
  }
  
}
_____________________________________________
using System.Collections.Generic;
public class Kata{
public static int getLoopSize(LoopDetector.Node startNode)
  {
    int lenght = 1;
    LoopDetector.Node tortoise = startNode.next; 
    LoopDetector.Node hare = startNode.next.next; 
    
    // Find the cycle, the hare and the tortoise will encouter at the cycle start
    while(tortoise != hare)
    {
      tortoise = tortoise.next;
      hare = hare.next.next;
    }
    
    // Find the lenght of the cycle - count the number of step to return at the cycle beginning
    hare = tortoise.next;
    while(tortoise != hare)
    {
      hare = hare.next;
      lenght++;
    }
    return lenght;
  }
}
_____________________________________________
using System;
using System.Collections.Generic;

public class Kata{
  public static int getLoopSize(LoopDetector.Node startNode){
    var nodes = new List<LoopDetector.Node>();
    var currentNode = startNode;
    var nextNode = startNode.next;
    while (nextNode != null)
    {
        nodes.Add(currentNode);
        currentNode = nextNode;
        nextNode = currentNode.next;
        currentNode.next = null;
    }
    return nodes.Count - nodes.IndexOf(currentNode);
  }
}
