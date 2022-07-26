595970246c9b8fa0a8000086


capitalizeWord = (word) ->
  word[0].toUpperCase() + word.substr(1)
______________________
capitalizeWord = (word) ->
  word[0].toUpperCase() + word.slice(1)
______________________
capitalizeWord = (word) ->
  word.replace(/^./, (x) -> x.toUpperCase())
