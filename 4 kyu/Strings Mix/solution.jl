module Mix
  export mix
  
  const lwrcase = "abcdefghijklmnopqrstuvwxyz"

  function mix(s1, s2)
    maxcount = []
    for c in lwrcase
      c1 = count(x->(x==c),s1)
      c2 = count(x->(x==c),s2)
      if c1>1 || c2>1
        if c1>c2
          push!(maxcount, "1:"*string(c)^c1)
        elseif c2>c1
          push!(maxcount, "2:"*string(c)^c2)
        elseif c1==c2 
          push!(maxcount, "=:"*string(c)^c2)
        end
      end
    end
    return join(sort(maxcount, by=x->(-length(x),x) ),'/')
  end

end

__________________________________________________
module Mix
export mix

function mix(s1, s2)
  s1 = filter(i -> islowercase(i[1]) && count(j -> j == i, split(s1, "")) > 1, split(s1, ""))
  s2 = filter(i -> islowercase(i[1]) && count(j -> j == i, split(s2, "")) > 1, split(s2, ""))
  s = unique(vcat(s1, s2))
  function lt(a, b)
    if (length(a) > length(b)) return true
    elseif (length(a) < length(b)) return false
    else
      x = 1
      while try a[x] == b[x] catch e false end x += 1 end
      return a[x] < b[x]
    end
  end

  join(sort(map(i -> (count(j -> j == i, s1) > count(j -> j == i, s2) ? "1" : (count(j -> j == i, s1) == count(j -> j == i, s2) ? "=" : "2")) * ":" * repeat(i, max(count(j -> j == i, s1), count(j -> j == i, s2))), s), lt=lt), "/")
end

end

__________________________________________________
module Mix
  export mix

  function mix(s1, s2)
    q1 = filter(islowercase, s1) |> collect |> sort |> s -> [(c => count(==(c), s)) for c in unique(s)] |> s -> sort(s, by=x->-x[2])
    q2 = filter(islowercase, s2) |> collect |> sort |> s -> [(c => count(==(c), s)) for c in unique(s)] |> s -> sort(s, by=x->-x[2])
    
    res = []
  
    while true
      if !isempty(q1) && !isempty(q2)
        if q1[1][2] == q2[1][2]
          n = q1[1][2]
          if n == 1
            break
          end
        
          arr1 = []
          arr2 = []
        
          while !isempty(q1) && (q1[1][2] == n)
            push!(arr1, popfirst!(q1)[1])
          end
        
          while !isempty(q2) && (q2[1][2] == n)
            push!(arr2, popfirst!(q2)[1])
          end
        
          u12 = intersect(Set(arr1), Set(arr2))
          arr12 = sort(collect(u12), by=ii->ii[1])
        
          for k in arr1
            if k ∉ u12
              push!(res, "1:$(repeat(k, n))")
              filter!(ii -> ii[1] != k[1], q2)
            end
          end
        
          for k in arr2
            if k ∉ u12
              push!(res, "2:$(repeat(k, n))")
              filter!(ii -> ii[1] != k[1], q1)
            end
          end
        
          for k in arr12
            push!(res, "=:$(repeat(k, n))")
          end
        elseif q1[1][2] > q2[1][2]
          item = popfirst!(q1)
          push!(res, "1:$(repeat(item[1], item[2]))")
          filter!(ii -> ii[1] != item[1], q2)
        else
          item = popfirst!(q2)
          push!(res, "2:$(repeat(item[1], item[2]))")
          filter!(ii -> ii[1] != item[1], q1)
        end
      elseif isempty(q1) && !isempty(q2) && q2[1][2] > 1
          item = popfirst!(q2)
          push!(res, "2:$(repeat(item[1], item[2]))")
      elseif isempty(q2) && !isempty(q1) && q1[1][2] > 1
          item = popfirst!(q1)
          push!(res, "1:$(repeat(item[1], item[2]))")
      else
        break
      end
    end
  
    join(res, "/")
  end

end

__________________________________________________
module Mix
  export mix

    function mix(s1, s2)
        dic1, let1 = dicprep(s1,'1')
        dic2, let2 = dicprep(s2,'2')
        letters = union(let1,let2)
        isempty(letters) && return ""
        arr = arrayprep(dic1,dic2,letters)
        srtd1 = sort(arr, rev=true)
        srtd2 = []
        for i in srtd1[1][1]:-1:2
            srt = sort(srtd1[findall(x->x[1]==i, srtd1)])
            if srt != [] append!(srtd2,srt) end
        end
        chop(join("$(item[2]):$(item[3]^item[1])/" for item in srtd2))
    end

    function dicprep(str, n)
        one = join(sort(collect(join([x.match for x in eachmatch(r"[a-z]+", str)]))))
        two = Dict([(x.match[1],[length(x.match),n]) for x in eachmatch(r"(.)\1+", one)])
        three = Set(keys(two))
        return two, three
    end
  
    function arrayprep(dic1,dic2,letters)
        arr = []
        for l in letters
            if haskey(dic1,l) && haskey(dic2,l)
                if dic1[l][1] < dic2[l][1]
                    push!(arr, push!(dic2[l],l))
                elseif dic1[l][1] > dic2[l][1]
                    push!(arr, push!(dic1[l],l))
                else
                    new = dic1[l]
                    new[2] = '='
                    push!(arr, push!(new,l))
                end
            elseif haskey(dic1,l)
                push!(arr, push!(dic1[l],l))
            else
                push!(arr, push!(dic2[l],l))
            end
        end
        arr
    end

end
    
__________________________________________________
module Mix
  export mix

  function mix(s1, s2)
    
    if s1=="" || s2==""
      return ""
    end
    
    tmp1=[]
    tmp2=[]
    eq=[]
    res=[]

    for char in 'a':'z'
        allin1=findall(it->it==char,s1)
        allin2=findall(it->it==char,s2)

            if length(allin1) < 2 && length(allin2) < 2
                continue
            elseif length(allin1) < 2 && length(allin2) > 1
                push!(tmp2,string("2:",repeat(char,length(allin2)),"/"))
            elseif length(allin2) < 2 && length(allin1) > 1
                push!(tmp1,string("1:",repeat(char,length(allin1)),"/"))
            elseif length(allin2) <  length(allin1)
                push!(tmp1,string("1:",repeat(char,length(allin1)),"/"))
            elseif length(allin1) < length(allin2)
                push!(tmp2,string("2:",repeat(char,length(allin2)),"/"))
            elseif length(allin1)==length(allin2)
                push!(eq,string("=:",repeat(char,length(allin1)),"/"))
            end
    end

    tmp1=sort(tmp1,by=it->length(it),rev=true)
    tmp2=sort(tmp2,by=it->length(it),rev=true)
    eq=sort(eq,by=it->length(it),rev=true)
  
    if length(eq)==0 && length(eq) == length(tmp1) && length(tmp1) == length(tmp2)
      return ""
    end

    maxlength=max([length(it) for it in [tmp1...,tmp2...,eq...]]...)

    for m in reverse(1:maxlength)
        for it in [tmp1,tmp2,eq]
            (length(filter(x->length(x)==m,it)) > 0) ? push!(res,filter(x->length(x)==m,it)...) : continue
        end
    end

    string(res...)[1:end-1]
  end

end
    
__________________________________________________
module Mix
  export mix
  using DataStructures
  function lower_counts(s)
    lower_only = filter(islowercase, s)
    lower_only_sorted = join(sort(collect(lower_only)))
    println(lower_only_sorted)
    groups = (match.match for match in eachmatch(r"(.)\1+", lower_only_sorted))
    count_dict = Dict{Char, Vector{Int64}}((first(group) => [length(group)] for group in groups))
    #sort(collect(count_dict), by = x -> x[2], rev = true)
  end
  function combine_counts(c1, c2)
    for key in union(keys(c1), keys(c2))
      haskey(c1, key) || (c1[key] = [0])
      haskey(c2, key) || (c2[key] = [0])
    end
    merged = merge(vcat, c1, c2)
    mix_dict = Dict{Char, String}()
    for (letter, counts) in merged
      if counts[1] == counts[2]
        mix_dict[letter] = "=:$(repeat(letter, counts[1]))"
      else
        (val, s) = findmax(counts)
        mix_dict[letter] = "$s:$(repeat(letter, val))"
      end
    
    end
    return mix_dict
  end
  function sorting_isless(a, b)
    length(a) < length(b) && return true
    length(a) > length(b) && return false
    a > b
  end
  function mix(s1, s2)
    mix_dict = combine_counts(lower_counts(s1), lower_counts(s2))
    sorted = sort(collect(mix_dict), by = x -> (-length(x[2]), x[2]))
    join([entry[2] for entry in sorted], "/")
  end

end
