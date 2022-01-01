function order(words)
  findnum(w) = match(r"\d", w).match
  join(sort(split(words, " "), lt = (a, b) -> findnum(a) < findnum(b)), " ")
end

_____________________________________________
function order(words)
  join(sort(split(words), by = x-> filter(isdigit, x)), " ")
end

_____________________________________________
function order(words)
    join(sort!(split(words), by=numberWord), " ")
end

function numberWord(word)
    for ch in word
        if isdigit(ch)
            return ch - '0'
        end
    end
    0
end

_____________________________________________
function order(words)
  join(map(((i, word),) -> word, sort(map(word -> (match(r"\d", word).match, word), split(words)))), " ")
end

_____________________________________________
function order(words)
  sorted = fill("", length(split(words)))
  for word in split(words)
    for i in word
      try 
        n = parse(Int, i)
        println(typeof(n))
        sorted[n] = word
      catch
        continue
      end
    end
  end
  return join(sorted, " ")
end
