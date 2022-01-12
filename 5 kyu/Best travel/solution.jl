module Travel 
  export choose_best_sum
  using IterTools

  function choose_best_sum(t, k, ls)
    subs = subsets(ls, k) |> collect
    subs = filter(<=(t), sum.(subs))
    return isempty(subs) ? -1 : maximum(subs)
  end

end
_______________________________________
module Travel 
    export choose_best_sum

    function choose_best_sum(t, k, ls)
        function chooseBestSumAux(t, k , ls, from) 
            if k == 0 
                if t >= 0 return 0
                else return t
                end
            else
                if t < k return -1 end
            end
            best = -1
            tmpBest = -1
            for i in from:length(ls)
                tmpBest = chooseBestSumAux(t - ls[i], k - 1, ls, i + 1)
                if tmpBest >= 0
                    best = max(best, ls[i] + tmpBest)
                end
            end
            best
        end
        chooseBestSumAux(t, k, ls, 1)
    end

end
_______________________________________
module Travel 
    export choose_best_sum

    function choose_best_sum(t, k, ls)
        function chooseBestSumAux(t, k , ls, from) 
            if k == 0 
                if t >= 0 return 0
                else return t
                end
            else
                if t < k return -1 end
            end
            best = -1
            tmpBest = -1
            for i in from:length(ls)
                tmpBest = chooseBestSumAux(t - ls[i], k - 1, ls, i + 1)
                if tmpBest >= 0
                    best = max(best, ls[i] + tmpBest)
                end
            end
            best
        end
        chooseBestSumAux(t, k, ls, 1)
    end

end
_______________________________________
module Travel 
export choose_best_sum
using IterTools

  function choose_best_sum(t, k, ls)
    test = []
    for n in collect(subsets(ls, k)) append!(test, sum(n)) end
    k > length(ls) || isempty(filter(x -> x <= t, test)) ? -1 : 
      maximum(filter(x -> x <= t, test))
  end

end
_______________________________________
module Travel 
export choose_best_sum

function choose_best_sum(t, k, ls)
  puppy = [n for n in 1:k]
  best = -1
  
  #filter out bad cases
  if k > length(ls)
    return best
  end
  
  while true
    
    #check if current combination is better than previous best
    temp = sum(ls[n] for n in puppy)
    if temp <= t && temp > best
      best = temp
    end
    
    #check if current combination is the last
    puppy != (length(ls) - k + 1):length(ls) || break
    
    #cycle through all possible combinations
    for n = 1:k
      if puppy[k - n + 1] == length(ls) - n + 1
        continue
      else
        puppy[k - n + 1] += 1
        for z = 2:n
          puppy[k - n + z] = puppy[k - n + 1] + z - 1
        end
        break
      end
    end
  end
  best
end
end
_______________________________________
module Travel 
    export choose_best_sum

    function choose_best_sum(t, k, ls)
        if k == 0
          return 0
        end
        if length(ls) < k
          return -1
        else 
          if length(ls) == k
            s = sum(ls)
            if s <= t
             return s
            else
             return -1
            end
          end
        end
        
        if t < ls[1]
          sum_with = -1
        else
          remaining = choose_best_sum(t-ls[1], k-1, ls[2:end])
          if remaining == -1
            sum_with = -1
          else
            sum_with = remaining + ls[1]
          end
        end
        sum_without = choose_best_sum(t,k,ls[2:end])
        max(sum_with, sum_without)
    end

end
_______________________________________
module Travel 
    export choose_best_sum

    function comb(t, k, ls, i)
      k == 0 && t >= 0 && return 0
      (k < 0 || i > length(ls)) && return -10000000
      max(comb(t, k, ls, i + 1), ls[i] + comb(t - ls[i], k - 1, ls, i + 1))
    end

    function choose_best_sum(t, k, ls)
      max(comb(t, k, ls, 1), -1)
    end

end
