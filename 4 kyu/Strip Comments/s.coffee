51c8e37cee245da6b40000bd


solution = (input, markers) ->
  r = new RegExp "\\s*([#{markers.join ''}].*)?$", "gm"
  input.replace r, ''
__________________________________
solution = (string, markers) ->
  string.replace new RegExp("\\s*[#{markers.join""}].*", "g"), ""
__________________________________
solution = (input, markers) ->
  reg = ///(#{('\\'+m for m in markers).join('|')})[^\n]+///g
  input.replace(reg, '').replace(/[ ]$/, '').replace ' \n', '\n'
__________________________________
solution = (input, markers) ->
    removeComment = (line) ->
        for each in markers
            line = line.split(each)[0].trim()
        line
    input.split('\n').map(removeComment).join('\n')
