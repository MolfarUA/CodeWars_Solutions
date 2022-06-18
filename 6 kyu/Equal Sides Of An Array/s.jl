function findevenindex(arr)
  for i=1:length(arr)
    sum(arr[1:i-1]) == sum(arr[i+1:end]) && return i
  end
  -1
end
________________________
function findevenindex(arr)
  r = sum(arr)
  l = 0
  for i in eachindex(arr)
    r -= arr[i]
    if l == r
      return i
    end
    l += arr[i]
  end
  -1
end
________________________
findevenindex(arr) = something(findfirst(cumsum(arr) .== reverse(cumsum(reverse(arr)))), -1)
________________________
function findevenindex(arr)
 sumsides([], arr)
end

function sumsides(left, right)    
  if left == []
      left_sum = 0
  else
      left_sum = sum(left)
  end
  
  if right == []
      return -1
  elseif left_sum == sum(right[2:end])
      return length(left) + 1
  else
      return sumsides([left;right[1]], right[2:end])
  end
end
________________________
function findevenindex(arr)
  
  function move_and_test(left, right, i)
    if right==left
      return i
    end
    
    if i==length(arr)
      return -1
    end

    i += 1
    left += arr[i-1]
    right -= arr[i]
    return move_and_test(left, right, i)
  end
  
  move_and_test(0, sum(arr)-arr[1], 1)
end
________________________
function findevenindex(arr)
  ind = -1
    for i in 1:length(arr)
        if sum(arr[1:i-1])==sum(arr[i+1:length(arr)])
             ind = i
        end
    end
  return ind
  end
