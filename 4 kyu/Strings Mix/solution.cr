def mix(s1, s2)
  counts1, counts2 = [s1, s2].map { |s| s.chars.select(&.lowercase?).tally }
  mixed = counts1.merge(counts2) { |k, v1, v2| [v1, v2].max }
  mixed.select { |k, v| v > 1 }
       .map { |k, v|
         from = ['=', '1', '2'][counts1.fetch(k, 0) <=> counts2.fetch(k, 0)]
         "#{from}:#{k.to_s * v}"
       }
       .sort_by { |s| {-s.size, s} }
       .join('/')
end

__________________________________________________
def mix(s1, s2)
    c = Hash(Char, Array(Int32)).new { |h, k| h[k] = [0, 0] }
    s1.chars.each { |x| c[x][0] += 1 if x.ascii_lowercase? }
    s2.chars.each { |x| c[x][1] += 1 if x.ascii_lowercase? }
    c.to_a
      .select!{ |x| x[1].max > 1 }
      .map { |x|
        ch, occs = x
        occ = occs[0] == occs[1] ? '=' : (occs.index(occs.max).not_nil! + 1).to_s[0]
        {occ, ch.to_s * occs.max}
      }
      .sort_by!{ |x| {-x[1].size, x[0], x[1][0]} }
      .map { |x| "#{x[0]}:#{x[1]}"}
      .join("/")
end

__________________________________________________
def comp(a, b)
    if (a.size == b.size) 
      return a <=> b 
    end
    b.size < a.size ? -1 : 1
end
def mix(s1, s2)
    alpha_s1, alpha_s2 = [0] * 26, [0] * 26
    s1.each_char { |c| if ((c.ord >= 97) && (c.ord <= 122)) 
      alpha_s1[c.ord - 97] += 1 
    end }
    s2.each_char { |c| if ((c.ord >= 97) && (c.ord <= 122)) 
      alpha_s2[c.ord - 97] += 1 
    end }
    res = ""
    i = 0
    while (i < 26)
        sm = [alpha_s1[i], alpha_s2[i]].max
        if (sm > 1)
            if (sm > alpha_s1[i])
                res += 2.to_s + ":"
                res += (i + 97).chr.to_s * sm
                res += "/"
            elsif (sm > alpha_s2[i])
                res += 1.to_s + ":"
                res += (i + 97).chr.to_s * sm
                res += "/"
            elsif (alpha_s1[i] == alpha_s2[i])
                res += "=:"
                res += (i + 97).chr.to_s * sm
                res += "/"
            end
        end
        i += 1
    end   
    l = res[0..-2].split('/').sort { |x, y| comp(x, y) }.join("/")
end

__________________________________________________
P = ["=:%s", "1:%s", "2:%s"]
def mix(s1, s2)
  t1,t2 = [s1, s2].map(&.chars.select!('a'..'z').tally)
  (t1.keys | t2.keys).map do |c|
    d = ((v1 = t1[c]? || 0).<=>(v2 = t2[c]? || 0))
    next if (m = [v1,v2].max) < 2 
    P[d] % ("#{c}" * m) 
  end.
  compact.group_by{|s| -s.size}.to_a.sort.map{|g,s| s.sort}.flatten.join('/')
end

__________________________________________________
def mix(s1, s2)
  s1 = s1.split("").uniq.reduce(Hash(String, Int32).new) { |r, e| r[e] = s1.count(e) if e.match(/[a-z]/); r }
  s2 = s2.split("").uniq.reduce(Hash(String, Int32).new) { |r, e| r[e] = s2.count(e) if e.match(/[a-z]/); r }

  (s1.keys + s2.keys).uniq.reduce([] of String) do |res, i|
    c1 = s1[i]? || 0
    c2 = s2[i]? || 0
    res << (c1 == c2 ? "=:#{(i * c1)}" : c1 > c2 ? "1:#{i * c1}" : "2:#{i * c2}") if c1 > 1 || c2 > 1
    res
  end.sort_by { |w| {-w.size, w[0], w[-1]} }.join "/"
end
