function formatduration(seconds)
  if seconds < 1
    return "now"
  end
  formatted = []
  times = [
    "year" => 31536000,
    "day" => 86400,
    "hour" => 3600,
    "minute" => 60,
    "second" => 1
  ]
  for t in times
    s = Int(floor(seconds / t[2]))
    if s >= 1
      push!(formatted, string(s) * " " * t[1] * (s > 1 ? "s" : ""))
      seconds %= t[2]
    end
  end
  return join(formatted, ", ", " and ")
end

__________________________________________________
function compose_sentence(arr)
    if length(arr) <= 1
        return join(arr)
    else
        start = join(arr[1:end-1], ", ")
        return "$(start) and $(arr[end])"
    end
end

function formatduration(s)
    if s == 0
        return "now"
    end
    NAMES = ["year", "day", "hour", "minute", "second"]
    y, s = fldmod(s, 31536000)
    d, s = fldmod(s, 86400)
    h, s = fldmod(s, 3600)
    m, s = fldmod(s, 60)
    res = ["$(num) $(st)$('s' ^ (num > 1))" for (num, st) in zip([y, d, h, m, s], NAMES) if num >= 1]
    return compose_sentence(res)
end

__________________________________________________
function formatduration(s)
  if s==0
    return "now"
  end
  v = [s÷31536000, s÷86400%365, s÷3600%24, s÷60%60, s%60]
  strs = ["$(v[1]) year", "$(v[2]) day", "$(v[3]) hour", "$(v[4]) minute", "$(v[5]) second"]
  join(collect(string(strs[i],v[i]!=1 ? "s" : "") for i in 1:5 if v[i]!=0), ", ", " and ")
end

__________________________________________________
function formatduration(t)
    iszero(t) && return "now"

    m, s = divrem(t, 60)
    h, m = divrem(m, 60)
    d, h = divrem(h, 24)
    y, d = divrem(d, 365)

    result = iszero(s) ? "" : "-$(s) second$(s > 1 ? "s" : "")"
    result *= iszero(m) ? "" : "-$(m) minute$(m > 1 ? "s" : "")"
    result *= iszero(h) ? "" : "-$(h) hour$(h > 1 ? "s" : "")"
    result *= iszero(d) ? "" : "-$(d) day$(d > 1 ? "s" : "")"
    result *= iszero(y) ? "" : "-$(y) year$(y > 1 ? "s" : "")"
    
    return(join(reverse(split(result, '-')[2:end]), ", ", " and "))
end

__________________________________________________
function formatduration(time)
    time == 0 && return "now"

    minutes, seconds = divrem(time, 60)
    hours, minutes = divrem(minutes, 60)
    days, hours = divrem(hours, 24)
    years, days = divrem(days, 365)

    t = (y=years, d=days, h=hours, m=minutes, s=seconds)

    result = iszero(t.s) ? "" : "-$(t.s) second$(t.s > 1 ? "s" : "")"
    result *= iszero(t.m) ? "" : "-$(t.m) minute$(t.m > 1 ? "s" : "")"
    result *= iszero(t.h) ? "" : "-$(t.h) hour$(t.h > 1 ? "s" : "")"
    result *= iszero(t.d) ? "" : "-$(t.d) day$(t.d > 1 ? "s" : "")"
    result *= iszero(t.y) ? "" : "-$(t.y) year$(t.y > 1 ? "s" : "")"
    
    return(join(reverse(split(result, '-')[2:end]), ", ", " and "))
end

__________________________________________________
function formatduration(seconds)
    if iszero(seconds)
        return "now"
    end
    format = ["year", "day", "hour", "minute", "second"]
    y, s = divrem(seconds, 31536000)
    d, s = divrem(s, 86400)
    h, s = divrem(s, 3600)
    m, s = divrem(s, 60)
    date = (y, d, h, m, s)
    nvalid = count(!iszero, date)
    str = ""
    for (i, x) in enumerate(date)
        if iszero(x)
            continue
        end
        str *= string(x, " ", format[i], !isone(x) ? "s" : "")
        nvalid -= 1
        if nvalid > 1
            str *= ", "
        elseif nvalid == 1
            str *= " and "
        end
    end
    str
end
