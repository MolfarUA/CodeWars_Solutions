544675c6f971f7399a000e79


function stringtonumber(str)
  parse(Int, str)
end
_______________________
function stringtonumber(str)
  Meta.parse(str)
end
_______________________
stringtonumber(str) = parse(Int64, str)
_______________________
function stringtonumber(string)
  try
    parse(Int64, string)
  catch
    string
  end
end
_______________________
function stringtonumber(string)
  try
    parse(Int64, string)
  catch
    string
  end
end
