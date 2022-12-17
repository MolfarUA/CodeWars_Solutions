5786f8404c4709148f0006bf


startingMark = (bodyHeight) ->
   Math.round((bodyHeight * 3.9354 + 3.4681) * 100) / 100
____________________________________
startingMark = (bodyHeight) ->
    a = {x: 1.52, y: 9.45}
    b = {x: 1.83, y: 10.67}
    m = (b.y - a.y) / (b.x - a.x)
    Math.round((m * bodyHeight + b.y - m * b.x) * 100) / 100
____________________________________
startingMark = (bodyHeight) ->
  guideline1 = 
    height: 1.52
    start: 9.45
  guideline2 = 
    height: 1.83
    start: 10.67
  mark = (guideline2.start - (guideline1.start)) / (guideline2.height - (guideline1.height))
  Math.round((mark * bodyHeight + guideline2.start - (mark * guideline2.height)) * 100) / 100
