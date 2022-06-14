persistence = (number) ->
  count = 0
  while number > 9
    number = ["#{number}"...].reduce (prod, num) -> prod * num
    count++
  count
________________________________________
persistence = (n) ->
  count = 0
  while n > 9
    n = [n+""...].reduce(((a, b) -> a * +b), 1)
    count++
  count
________________________________________
persistence = (n) ->
  sd = (n) -> n.toString().split('').map(Number).reduce (a, b) -> a * b
  
  """ recursion doesn't work for very large numbers
      return 0 if n <= 9
      return 1 + persistence sd n
  """
  
  i = 0
  while n > 9
    n = sd n
    i += 1
    
  i
________________________________________
persistence = (n) ->
  i = 0
  while n > 9
    mul = 1
    while n > 0
      mul *= n % 10
      n = Math.floor(n / 10)
    n = mul
    i++
  i
________________________________________

persistence = (n,i=0)-> if n>9 then persistence(eval([n+''...].join('*')),i+=1) else i
