57cfdf34902f6ba3d300001e


twosort(array) = join(minimum(array), "***")
___________________________
twosort(array) = join(split(sort!(array)[1], ""), "***")
___________________________
function twosort(array)
  join(minimum(array), "***")
end
