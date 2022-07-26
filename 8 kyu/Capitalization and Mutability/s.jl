595970246c9b8fa0a8000086


function capitalizeword(word)
  uppercasefirst(word)
end
______________________
capitalizeword = uppercasefirst
______________________
function capitalizeword(word)
  uppercase(word[1]) * word[2:end]
end
