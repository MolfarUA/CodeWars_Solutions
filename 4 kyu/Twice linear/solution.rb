def dbl_linear(n)
    h = 1; cnt = 0; q2, q3 = [], []
    while true do
        if (cnt >= n) then
            return h
        end
        q2.push(2 * h + 1)
        q3.push(3 * h + 1)
        h = [q2[0], q3[0]].min
        if h == q2[0] then h = q2.shift() end
        if h == q3[0] then h = q3.shift() end
        cnt += 1
    end
end
          
__________________________________________________
def dbl_linear(n)
    u=[1]
    (0..n*5).each { |i| u << u[i]*2 + 1 << u[i]*3 + 1}
    u.sort.uniq[n]
end

__________________________________________________
require 'set'

def dbl_linear(n)
  x = 0
  ni = 0
  u = Set.new([1.0])
  while x += 1 do
    if u.include?((x-1)/2.0) or u.include?((x-1)/3.0)
      u.add(x.to_f)
      ni += 1
      return x if ni == n
    end
  end
end
