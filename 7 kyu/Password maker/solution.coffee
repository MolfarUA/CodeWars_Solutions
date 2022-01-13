makePassword = (phrase) ->
  passwd = (item.charAt(0) for item in phrase.split(' ')).join('')
  passwd.replace(/i/gi, '1').replace(/o/gi, '0').replace(/s/gi, '5')
__________________________________
makePassword = (phrase) ->
  phrase.replace(/(\w)\S+\s?/g,"$1").replace(/i/gi,'1').replace(/o/ig,'0').replace(/s/gi,'5')
__________________________________
makePassword = (phrase) ->
  x = {i:1,o:0,s:5}
  (v[0] for v in phrase.split ' ').join('').replace /i|o|s/gi, (m)->x[m.toLowerCase()]
__________________________________
makePassword = (phrase) ->
  return phrase.split(' ')
               .map( (x)->x=x[0])
               .join('')
               .replace(/i/gi,"1")
               .replace(/o/gi,"0")
               .replace(/s/gi,"5");
__________________________________
makePassword = (phrase) ->
  letters = "i1I1o0O0s5S5"
  return phrase.split(" ").map((x) -> x[0]).join("").replace(/[ios]/ig, (y) -> letters[letters.indexOf(y) + 1])
__________________________________
makePassword = (phrase) ->
  arr = phrase.split(" ")
  pw = ""
  for i in [0..arr.length-1]
    if arr[i][0] is 'O' or arr[i][0] is 'o' then pw = pw.concat('0') else if arr[i][0] is 'I' or arr[i][0] is 'i' then pw = pw.concat('1') else if arr[i][0] is 'S' or arr[i][0] is 's' then pw = pw.concat('5') else pw = pw.concat(arr[i][0])
  pw
