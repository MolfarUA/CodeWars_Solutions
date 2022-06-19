56f173a35b91399a05000cb7


findLongest = (str) ->
  spl = str.split(' ')
  longest = 0
  for i in [0...spl.length]
    if spl[i].length > longest
      longest = spl[i].length
    i++
  longest
__________________________
findLongest = (str) -> 
  spl = str.split(' ')
  longest = 0
  
  for v, _ in spl
    if (v.length > longest)
      longest = v.length;
    
  longest
__________________________
findLongest = (str) ->
  Math.max(str.split(" ").map((x) -> x.length)...)
