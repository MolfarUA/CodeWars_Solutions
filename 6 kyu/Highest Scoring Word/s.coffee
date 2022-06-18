57eb8fcdf670e99d9b000272


high = (x) ->
  scores = x.split(" ").map((a) -> [""+a...].reduce(((y, z) -> y + z.charCodeAt() - 96), 0))
  x.split(" ")[scores.indexOf(Math.max(scores...))]
_____________________________________________
high = (x) -> x.split(" ").sort((a,b)->f(a) - f(b)||1).pop()
f = (s) -> s.split('').reduce(((acc, c) ->  acc + c.charCodeAt() - 96), 0)
_____________________________________________
high = (s) ->
  as = s.split(' ').map((s)-> [s...].map(((e)=>x+=e.charCodeAt()-96),x=0).pop())
  s.split(' ')[as.indexOf(Math.max(as...))]
