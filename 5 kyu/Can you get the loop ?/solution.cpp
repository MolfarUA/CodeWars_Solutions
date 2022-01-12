int getLoopSize(Node* startNode)
{
  Node* turtle = startNode;
  Node* rabbit = startNode->getNext();
  while(turtle != rabbit) {
    turtle = turtle->getNext();
    rabbit = rabbit->getNext()->getNext();
  }
  turtle = turtle->getNext();
  int count = 1;
  while(turtle != rabbit) {
    turtle = turtle->getNext();
    count++;
  }
  return count;
}
_____________________________________________
#include <vector>
#include <algorithm>
#include <iterator>
#include <type_traits>

int getLoopSize(Node *startNode)
{
  std::vector<Node *> addrs;
  while (std::find(addrs.begin(), addrs.end(), startNode) == addrs.end())
  {
    addrs.push_back(startNode);
    startNode = startNode->getNext();
  }
  return addrs.size() - std::distance(addrs.begin(), std::find(addrs.begin(), addrs.end(), startNode));
}
_____________________________________________
int getLoopSize(Node* startNode)
{
  
  Node* t = startNode;
  Node* h = startNode;
  
  do {
    t = t->getNext();
    h = h->getNext()->getNext();
  } while(t != h);
  
  int looplen = 0;
  do {
    h = h->getNext();
    ++looplen;
  } while(h != t);
  
  return looplen;
}
_____________________________________________
#include <map>

int getLoopSize(Node* startNode)
{
    std::map<const int* const, const int> nodes;
    int i = 0;
    while (startNode)
    {
        const auto item = nodes.find((const int*)&(*startNode));
        if (item == nodes.end())
        {
            nodes.insert({ (const int*)&(*startNode), i });
        }
        else
        {
            return nodes.size() - item->second;
        }

        startNode = startNode->getNext();
        ++i;
    }
    return 0;
}
_____________________________________________
#include <unordered_map>

int getLoopSize(Node* startNode) {
// Determines the length of the loop.
  
  std::unordered_map<Node*,int> nodes;
  int nodes_counter = 0;
  
  while (startNode != NULL) {
    if (nodes.count(startNode) != 0) return nodes_counter-nodes[startNode];
    nodes.insert({startNode,nodes_counter});
    nodes_counter++;
    startNode = startNode->getNext();
  }
  
  return -1;
}
