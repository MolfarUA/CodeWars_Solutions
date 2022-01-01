function humanreadable(seconds)
  h,s = divrem(seconds, 3600)
  m,s = divrem(s, 60)
  join((lpad(h, 2, "0"), lpad(m, 2, "0"), lpad(s, 2, "0")), ":")
end

_____________________________________
using Printf

function humanreadable(seconds)
    hours = seconds ÷ 3600
    minutes = (seconds % 3600) ÷ 60
    seconds = seconds % 60
    @sprintf "%02d:%02d:%02d" hours minutes seconds
end

_____________________________________
function humanreadable(seconds)
  temp = seconds

  hrs = temp ÷ 3600
  min = temp % 3600 ÷ 60
  sec = temp % 3600 % 60

  if hrs < 10
    hrs = "0" * string(hrs)
  end
  if min < 10
    min = "0" * string(min)
  end
  if sec < 10
    sec = "0" * string(sec)
  end

  string(hrs) * ":" * string(min) * ":" * string(sec)
end

_____________________________________
function humanreadable(seconds)
  m, s = divrem(seconds, 60)
  h, m = divrem(m, 60)
  join(string.((h,m,s), pad=2), ":")
end

_____________________________________
function humanreadable(seconds)
   m, s = divrem(seconds, 60)
   h, m = divrem(m, 60)
   h, m, s = map(i->(string(i, pad=2)), [h, m, s])
   return "$h:$m:$s"
end
