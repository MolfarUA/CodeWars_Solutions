57873ab5e55533a2890000c7


def time_correct(t)
  return t if t.nil? || t.empty?
  if /\A\d\d:\d\d:\d\d\z/ === t
    h, m, s = t.split(":").map(&.to_i)    
    m += s / 60
    h += m / 60
    [h % 24, m % 60, s % 60].map{|x| x.to_s.rjust(2, '0')}.join(":")
  end
end
_________________________________
def time_correct(t)
  return t if t.nil? || t.empty?
  if t =~ /\A\d\d:\d\d:\d\d\z/
    h, m, s = t.split(":").map(&.to_i)
    if s >= 60
      m += 1
      s -= 60
    end
    if m >= 60
      h += 1
      m -= 60
    end
    h %= 24
    "%02d:%02d:%02d" % [h,m,s]
  else
    nil
  end
end
_________________________________
def time_correct(t) return nil if t.nil?; return "" if t == ""; return nil if !(t && /\d\d:\d\d:\d\d/=~t); s=(t.split(":").reduce(0){|a,b| a*60+b.to_i}); [s / 3600 % 24,s / 60 %60,s%60].map{|a| ("0"+a.to_s)[-2..-1]}.join(":") end
