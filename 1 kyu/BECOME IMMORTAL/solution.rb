59568be9cc15b57637000054

def elder_age(m,n,l,t)
  p = 0
  while 1 << p <= m || 1 << p <= n || 1 << p <= l do p += 1 end
  f = Array.new(p + 1) { Array.new(2) { Array.new(2) { Array.new(2, 0) } } }
  g = Array.new(p + 1) { Array.new(2) { Array.new(2) { Array.new(2, 0) } } }
  g[p][0][0][0] = 1
  (p-1).downto(0) do |i|
    (0..1).each do |a|
      (0..1).each do |b|
        (0..1).each do |c|
          next if g[i + 1][a][b][c] == 0 && f[i + 1][a][b][c] == 0
          nn = (n >> i) & 1
          mm = (m >> i) & 1
          ll = (l >> i) & 1
          (0..1).each do |x|
            next if a == 0 && x > nn
            (0..1).each do |y|
              next if b == 0 && y > mm
              z = x ^ y
              next if c == 0 && z < ll
              a1 = a == 0 && x == nn ? 0 : 1
              b1 = b == 0 && y == mm ? 0 : 1
              c1 = c == 0 && z == ll ? 0 : 1
              f[i][a1][b1][c1] = (f[i][a1][b1][c1] + f[i + 1][a][b][c] + (z << i) * g[i + 1][a][b][c]) % t
              g[i][a1][b1][c1] = (g[i][a1][b1][c1] + g[i + 1][a][b][c]) % t
            end
          end
        end
      end
    end
  end
  ((f[0][1][1][1] - g[0][1][1][1] * l) % t + t) % t
end
____________________________________
def elder_age(m, n, l, t, s = 0)             # -'s' represents a scaling number for the given square ( [[0, 1], [1, 0]] => [[s, s+1], [s+1, s]] )
  
  return 0 if m <= 0 || n <= 0               # - Sum of empty region is 0
  n, m = [m,n].minmax                        # - Ensure m is largest side for consistency
  
  d = 2**Math.log(m, 2).floor                # - Get length of the smallest square less than m
  min = [d, n].min                           # - Height of the valid portion of the region 
  i, j = [s+d-l-1, 0].max, [s-l-1, 0].max    # - Upper bnds of the sums from [1, i] and [1, j].
                                               
  x = min*( i*(i+1) - j*(j+1) )/2            # - sum(j+1, i) = sum(1, i) - sum(1, j)
                                             #   represents sum of the 'd x d' portion
  
  b = elder_age(   d, n-d, l, t, d+s)         # - sum of the region     'd x (n-d)' (bottom remainder)
  r = elder_age( m-d, min, l, t, d+s)         # - sum of the region   '(m-d) x min' (right  remainder)
  c = elder_age( m-d, n-d, l, t, s )          # - sum of the region '(m-d) x (n-d)' (corner remainder)
  
  return (x + c + b + r)%t
end
________________________________________________
def elder_age(m, n, l, t)
  
  def parse(rows, columns, loss, curr_time)
    min_side, max_side = [rows, columns].minmax
    loss = 0 if loss.negative?
    
    max_pow = 2 ** Math.log(max_side, 2).floor
    lim = [curr_time + max_pow - loss, 0].max
    
    int_sum = [lim - curr_time, 0].max * (lim + curr_time - 1) / 2
    
    max_pow == max_side ? int_sum * min_side : 
    max_pow > min_side ? int_sum * min_side + parse(max_side - max_pow, min_side, loss - max_pow, lim) : 
    int_sum * max_pow + parse(max_side - max_pow, min_side - max_pow, loss, curr_time) + 
      parse(max_side - max_pow, max_pow, loss - max_pow, lim) +
      parse(max_pow, min_side - max_pow, loss - max_pow, lim)
  end
  
  parse(m, n, l, 0) % t
end
