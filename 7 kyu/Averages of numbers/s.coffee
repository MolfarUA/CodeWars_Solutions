averages = (numbers) ->
  if numbers then numbers.map((_, i) -> (numbers[i] + numbers[i + 1]) / 2).slice(0, -1) else []
____________________________
averages = (a) ->
  if a then a.map(((e, i) ->
    if i > 0 then (a[i - 1] + e) / 2 else e
  )).slice(1) else []
____________________________
averages = (a) -> if a == null || a.length < 2 then [] else Array(a.length - 1).fill(0).map((_, i) -> (a[i] + a[i + 1]) / 2)
____________________________
averages = (numbers) -> if numbers then numbers.slice(1).map (v, i) -> (v + numbers[i]) / 2 else []
____________________________
averages = (numbers) -> 
  return [] if numbers==null || !Array.isArray(numbers)
  numbers.slice(1).map((x,i)=>(x+numbers[i])/2)
____________________________
averages = (numbers) ->
  if numbers == null || numbers.length < 2
    return []
  results = []
  current = 1
  while current < numbers.length
    results.push (numbers[current - 1] + numbers[current]) / 2
    current++
  results
