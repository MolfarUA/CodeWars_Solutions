56a1c63f3bc6827e13000006


def smaller(arr)
    result, dkey = [], arr.uniq.sort
    dcount = [0]*dkey.length
    arr.reverse_each do |last|
        result << ((i = dkey.bsearch_index {|x| x >= last }) != 0 ? dcount[0..i-1].sum : 0)
        dcount[i] += 1        
    end
    result.reverse
end
______________________________________
def smaller(arr)
  res = Array.new(arr.length) { 0 }
  sorted = [arr[-1]]
  (arr.length - 2).downto(0).each do |i|
    k = sorted.bsearch_index { |x| x >= arr[i] }
    res[i] = (k or sorted.length)
    sorted.insert (k or -1), arr[i]
  end
  res
end
______________________________________
def smaller(arr)
  result = []
	root = nil;
	i=i=arr.length-1
	while i>=0
	 root = insert_node(arr[i], root, result, i, 0);
	 i-=1
	end
	return result
end

def insert_node(num, node, ans, i, total)
 if node.nil?
 	node = {value: num, sum: 0, duplicate: 1, left: nil, right: nil}
 	ans[i] = total
 elsif node[:value]==num
 	node[:duplicate]+=1
 	ans[i] = total + node[:sum]
 elsif node[:value] > num
 	node[:sum]+=1
 	node[:left] = insert_node(num, node[:left], ans, i, total)
 else
 	node[:right] = insert_node(num, node[:right], ans, i, total + node[:duplicate] + node[:sum])
 end
 node
end
______________________________________
def smaller(arr)
  arr = arr.reverse
  
  occs = []
  
  arr.each_with_index.map do |cur, i|
    
    index = occs.bsearch_index { |x| x >= cur }
    
    if index
      occs.insert(index, cur)
    else
      occs.push(cur)
      index = i
    end

    index
  end.reverse
end
