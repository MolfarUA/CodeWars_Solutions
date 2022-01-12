def choose_best_sum(t, k, ls)
  ls.combinations(k).map(&.sum).select { |d| d <= t }.max?
end

_______________________________________
def choose_best_sum(t, k, ls)
  ls.each_combination(k).map(&.sum).select(&.<=(t)).max?
end
_______________________________________
def choose_best_sum(t, k, ls)
  ls.combinations(k).map(&.sum).reject(&.>(t)).max?
end
_______________________________________
def choose_best_sum(t, k, ls)
    a = ls.combinations(k).to_a
    mx = -1
    res = [] of Int32
    a.each do |l|
        s = l.reduce(0){ |sum, x| sum + x }
        if ((s >= mx) && (s <= t))
            res = [l, s]
            mx = s
        end
    end
    if (res.size > 0)
      res[1]
    else nil end
end
_______________________________________
def choose_best_sum(t, k, ls)
  return if k > ls.size 
  ls.combinations(k).each.map(&.sum).select(&.<=(t)).max?
end
