function smash(words)
  join(words, ' ')
end

_____________________________________
function smash(words)
str=string();
for i in 1:1:size(words)[1]
    if i==1
    str=words[i]
    else
    str=str*" "*words[i]
    end
end
return str
end

_____________________________________
function smash(words)
  if length(words) === 0
        ""
  else
      sent = words[1]
      for i in 2:length(words)
        sent = string(sent," ",words[i])
      end
      sent
  end
end
