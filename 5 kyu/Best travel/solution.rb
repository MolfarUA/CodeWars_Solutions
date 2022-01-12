def choose_best_sum(t, k, ls)
    ls.combination(k)
      .map{|path| path.inject(:+)}
      .select{|sum| sum <= t}
      .max
end
_______________________________________
def choose_best_sum(t, k, ls)
  ls.combination(k).collect { |ds| ds.inject(:+) }.reject { |d| d > t }.max
end
_______________________________________
def choose_best_sum(t, k, ls)
    possible_trips = ls.combination(k).to_a
    viable_trips = possible_trips.select { |subarr| subarr.inject(:+) <= t }
    sum_all = viable_trips.map { |trip| trip.inject(:+) }
    return sum_all.max
end
_______________________________________
def choose_best_sum(distance_limit, town_count, distance_list)
  distance_list.combination(town_count).map{ |c| c.inject(&:+) }.reject{ |sum| sum > distance_limit }.max
end
