def loop_size(node)
  tortoise = hare = node
  cycle_found = false
  loop_count = 0
  while(tortoise.next != nil && hare.next != nil && hare.next.next != nil) do
    tortoise = tortoise.next
    hare = hare.next.next
    if(tortoise == hare && cycle_found)
      break
    end
    if(tortoise==hare)
      cycle_found=true
    end
    loop_count+=1 if cycle_found 
  end
  loop_count
end
_____________________________________________
class Node
  attr_accessor :mark 
end

def loop_size(node)
  index = 0
  while node.mark == nil
    node.mark = index
    index += 1
    node = node.next
  end  
  index - node.mark
end
_____________________________________________
def loop_size(node)
  nodes = [node]
  nodes << node = node.next until nodes.include? node.next
  nodes.count - nodes.index(node.next)
end
_____________________________________________
def loop_size(node)
  Node.class_eval do
    attr_accessor :position
  end

  index = 1
  while node.position.nil?
    node.position = index
    node = node.next
    index += 1
  end
  index - node.position
end
_____________________________________________
def loop_size n
  a = []
  while !a.include?(n)
    a << n
    n = n.next
  end
  a.length - a.index(n)
end
_____________________________________________
def loop_size(node)
  turtle = node
  rabbit = node
  while true
    turtle = turtle.next
    rabbit = rabbit.next.next
    break if turtle == rabbit
  end
  rabbit = rabbit.next
  count = 1
  while turtle != rabbit
    count += 1
    rabbit = rabbit.next
  end
  count
end
_____________________________________________
def loop_size(node)
  return 1 if node.next == node
  result_array = [node]
  until result_array.include?(node.next) do
    result_array << node.next
    node = node.next
  end
  result_array.size - result_array.find_index(result_array.last.next)
end
