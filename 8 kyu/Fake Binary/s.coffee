fakeBin = (x) ->
  x.replace(/[0-4]/g, '0').replace(/[5-9]/g, '1')
__________________________________
fakeBin = (x) ->
  result = ''
  for c in x
    result += '0' if Number(c) < 5
    result += '1' if Number(c) >= 5
  result
__________________________________
fakeBin = (x) -> x.split("").map((c) -> c // 5).join("")
__________________________________
fakeBin = (x) ->
  x.replace(/[0,1,2,3,4]/gi, "0").replace(/[5,6,7,8,9]/gi, "1"); 
