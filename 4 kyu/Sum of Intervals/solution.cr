def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
  intervals.flat_map do |a, b| (a...b).to_a end.uniq.size
end

____________________
def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
  res = ([] of Int32).to_set
  intervals.each{|t|
    a,b = t
    (a...b).each{|i|
      res.add(i)
    }
  }
  res.size
end

____________________
def sum_of_intervals(i : Array(Tuple(Int32, Int32)))
  i.transpose.map(&.sort).transpose.chunk_while{|p,n| p[-1] > n[0] }.map(&.flatten.minmax).sum{|f,l| l-f}
end

__________________
def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
   intervals.map{|x| (x.min...x.max).to_a}.flatten.uniq.size
end

__________________

class Intervals
  def initialize
    @a = Array(Set(Int32)).new
  end

  def add(t : Tuple(Int32, Int32))
    s = Set(Int32).new
    t[0].upto t[1] - 1 do |n|
      s.add(n)
    end
    @a << s
  end

  def sum
    superset = Set(Int32).new
    @a.each do |s|
      superset += s
    end
    superset.size
  end
end

def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
  x = Intervals.new
  intervals.each do |i|
    x.add i
  end
  x.sum
end


_______________________________
def insert_interval(intervals, i)
  intervals.size.times do |x|
    l, h = intervals[x]
    if (i[0] <= h && i[1] >= l)
      intervals.delete_at(x)
      insert_interval(intervals, {Math.min(i[0], l), Math.max(i[1], h)})
      return
    end
  end
  intervals << i
end

def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
  r = [intervals.shift]
  intervals.each do |i|
    insert_interval(r, i)
  end
  r.sum {|i| i[1]-i[0]}
end

___________________________________
class Intv
    property lson, rson, lt, rt
    def initialize(@lt : Int32, @rt : Int32)
        @lson = nil.as Intv?
        @rson = nil.as Intv?
    end

    def disjoint_rt(other : Intv)
        if other.rt <= @rt
            nil
        else
            Intv.new(max(@rt, other.lt), other.rt)
        end
    end

    def disjoint_lt(other : Intv)
        if other.lt >= @lt
            nil
        else
            Intv.new(other.lt, min(@lt, other.rt))
        end
    end

    def include(other : Intv)
        r = disjoint_rt(other)
        l = disjoint_lt(other)
        unless r.nil?
            if @rson.nil?
                @rson = r
            else
                @rson.not_nil!.include(r)
            end
        end
        unless l.nil?
            if @lson.nil?
                @lson = l
            else
                @lson.not_nil!.include(l)
            end
        end
    end

    def size
        @rt - @lt + (@lson.nil? ? 0 : @lson.not_nil!.size) + (@rson.nil? ? 0 : @rson.not_nil!.size)
    end
end

def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
    tree = Intv.new(0, 0)
    intervals.each do |x|
        a, b = x
        tree.include(Intv.new(a, b))
    end
    tree.size
end

def max(a, b)
    a >= b ? a : b
end

def min(a, b)
    a >= b ? b : a
end

______________________________________
alias Interval = Tuple(Int32, Int32)
def sum_of_intervals(intervals : Array(Interval))
  max = intervals.max_of(&.last)
  min = intervals.min_of(&.first)
  ranges = intervals.map { |(a, b)| Range.new(a, b, true) }
  (min..max).count { |i| ranges.any?(&.covers?(i)) }
end

_______________________________
def sum_of_intervals(intervals : Array(Tuple(Int32, Int32)))
  intervals.flat_map do |a, b| (a..b - 1).to_a end.uniq.size
end

___________________________
def sum_of_intervals(intervals : Iterable({T, T})) : T forall T
  intervals = intervals.sort
  s = 0
  x = intervals[0][0]
  intervals.each do |(b, e)|
    case
      when x < b then s += e - b
      when x < e then s += e - x
    end
    x = {x, e}.max
  end
  s
end

____________________________
def sum_of_intervals(intervals : Iterable({T, T})) : T forall T
  intervals = intervals.sort
  intervals.reduce({0, intervals[0][0]}){ |(s, x), (b, e)|
    {s + ({x, e}.max - {x, b}.max), {x, e}.max}
  }[0]
end
