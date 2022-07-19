51c8e37cee245da6b40000bd


stripcomments(input, markers) = rstrip(replace(input, Regex("[\\s]*[" * join(markers) * "][^\n]*") => ""))
__________________________________
stripcomments(input, markers) = replace(input, Regex("\\s*((\\" * join(markers, "|\\") * ").*)?\$", "m")=>"")
__________________________________
# Note: Treatment of empty lines is apparently weird, and I found no obvious rule. 
# Tests pass under the following conditions
#   "\n" should be kept if it ends the 1st line.
#   "\n" should be removed if it ends the last line.
#   "\n\n" should be replaced by "\n" --> no empty lines inside the string. 

function stripcomments(input, markers)
  lines = split(input,"\n")
  
  stripped_lines = [strip_line(line, markers) for line in lines]

  reassembled_string = join(stripped_lines,"\n")
  
  return rstrip( replace(reassembled_string, r"\n\n" => "\n"), '\n')
end

function strip_line(line, markers::Array{String})
  for m in markers
    line = keep_until_marker(line, m)
  end
  return rstrip(line) #remove whitespace
end

function keep_until_marker(line, marker)
  return split(line, marker)[1]
end
__________________________________
function stripcomments(input, markers)
    output = []
    for s in split(input, "\n")
        [s = rstrip(split(s, m)[1]) for m in markers]
        (output == [] && s == "" || s != "") && push!(output, s)
    end
    join(output, "\n")   
end
