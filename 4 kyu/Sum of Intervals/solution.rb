def sum_of_intervals(intervals)
  intervals.flat_map { |x, y| [*x...y] }.uniq.size
end

_______________________
def sum_of_intervals(intervals)
  intervals.map{|a| (a[0]...a[1]).to_a }.flatten.uniq.size
end

______________________
def sum_of_intervals(arr)
    s,top = 0, nil
    for a,b in arr.sort do
        top = a if top.nil? || top < a
        if b > top
            s  += b-top
            top = b
        end
    end
    return s
end

_____________________
def sum_of_intervals(intervals)
  intervals.map { |start, stop| (start...stop).to_set } .reduce(&:merge) .size
end

____________________
def sum_of_intervals(intervals)
  intervals.flat_map{|i| (i[0]+1..i[1]).to_a}.uniq.length
end

______________________
def sum_of_intervals(intervals)
  intervals.map { |a, b| (a...b).to_a }.flatten.uniq.count
end

_____________________
def sum_of_intervals(intervals)
  intervals.reduce([]) { |acc, interval| acc | (interval.first...interval.last).to_a }.size
end

______________________
def sum_of_intervals(intervals)
  intervals.sort! { |a, b| a[0] <=>  b[0] }
  top = intervals.first.first
  intervals.reduce(0) do |range, item|
    first, second = item
    if top > first && top < second
      range = range + (second - top)
      top = second
    elsif top <= first
      range = range + (second - first)
      top = second
    end
    range
  end
end
