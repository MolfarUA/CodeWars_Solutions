56a1c63f3bc6827e13000006


def smaller(arr)
  ns = Array(Int32).new(arr.size, 0)
  node = nil
  i = arr.size-1
  while i >= 0
    node = Node.add(node, arr[i], ns, i, 0)
    i -= 1
  end
  ns
end

class Node
  property :n, :acc, :count, :left, :right
  @right : Node | Nil
  @left : Node | Nil
  def initialize(n : Int32, acc : Int32) 
    @n = n
    @acc = acc
    @count = 1
    @left = nil
    @right = nil
  end
  def self.add(node, n, ns, i, acc)
    if node.nil?
      node = Node.new(n, 0)
      ns[i] = acc
    else
      if node.n > n
        node.acc += 1
        node.left = Node.add(node.left, n, ns, i, acc)
      elsif node.n < n
        node.right = Node.add(node.right, n, ns, i, acc + node.acc + node.count)
      else
        node.count += 1
        ns[i] = acc + node.acc
      end
    end
    node
  end
end
______________________________________
def smaller(arr)
  result_array = Array(Int32).new(arr.size, 0)
  
  root_node = Node.new(1000, 0)

  (arr.size - 1).downto(0).each do | i |
    current_num = arr[i]
    root_node = root_node.add_node(current_num, root_node, result_array, i, 0)
  end
  
  result_array
end

class Node
  property :val, :total, :freq, :right, :left
  
  @right : Node | Nil
  @left : Node | Nil
    
  def initialize(val : Int32, total : Int32)
    @val = val
    @total = total
    @freq = 1
    @right = nil
    @left = nil
  end
  
  def add_node(current_num, root_node, result_array, idx, smaller)
    if root_node.nil?
      root_node = Node.new(current_num, 0)
      result_array[idx] = smaller
    elsif root_node.val == current_num
      root_node.freq += 1
      result_array[idx] = smaller + root_node.total
    elsif root_node.val > current_num
      root_node.total += 1
      root_node.left = root_node.add_node(current_num, root_node.left, result_array, idx, smaller)
    else
      smaller += root_node.freq + root_node.total
      root_node.right = root_node.add_node(current_num, root_node.right, result_array, idx, smaller)
    end
    root_node
  end
  
end
