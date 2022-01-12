defmodule BestSum do
  defp comb(0, _), do: [[]]
  defp comb(_, []), do: []
  defp comb(m, [h|t]) do
    (for l <- comb(m-1, t), do: [h|l]) ++ comb(m, t)
  end
  
  def best_sum(t, k, ls) do
    a = comb(k, ls) 
    |> Enum.map(fn x -> Enum.sum(x) end)
    |> Enum.filter(fn x -> x <= t end)
    if (a == []) do nil else Enum.max(a) end
  end
end
_______________________________________
defmodule BestSum do
  def comb(0, _), do: [[]]
  def comb(_, []), do: []
  def comb(m, [h|t]) do
    (for l <- comb(m-1, t), do: [h|l]) ++ comb(m, t)
  end

  def sum_list([]), do: 0
  def sum_list([hd | tl]) do
    hd + sum_list(tl)
  end
  
  def get_highest_possible_value(max, nil, v2) when v2 <= max, do: v2
  def get_highest_possible_value(max, v1, v2) when v2 <= max and  v2 > v1, do: v2
  def get_highest_possible_value(max, v1, v2), do: v1
  
  def best_sum(t, k, ls) do
    comb(k, ls) 
      |> Enum.map(fn l -> sum_list(l) end)
      |> Enum.reduce(nil, fn(item, acc) -> 
        acc = get_highest_possible_value(t, acc, item)
      end)
  end
end
_______________________________________
defmodule BestSum do
  
  def best_sum(max_travel_distance, number_of_cities, distances) do
    RC.comb(number_of_cities, distances)
    |> Enum.map(&Enum.sum/1)
    |> only_lte_than(max_travel_distance)
    |> max_or_nil()
  end
  
  defp only_lte_than(list, max) do
    Enum.filter(list, fn item -> item <= max end)
  end
  
  defp max_or_nil(list), do: Enum.max(list, fn -> nil end)
end

defmodule RC do
  def comb(0, _), do: [[]]
  def comb(_, []), do: []
  def comb(m, [h|t]) do
    (for l <- comb(m-1, t), do: [h|l]) ++ comb(m, t)
  end
end
_______________________________________
defmodule BestSum do
  
  def best_sum(max_dist_sum, num_towns, distances) do
    combs = combinations(distances, num_towns)
    final_list = combs
      |> Enum.map(fn x -> Enum.sum(x) end)
      |> Enum.filter(fn x -> x <= max_dist_sum end)
    if Enum.empty? final_list do nil else Enum.max(final_list) end
  end
  
  defp combinations(_, 0), do: [[]]
  defp combinations([], _), do: []
  defp combinations([head | tail], num_towns) do
    for x <- combinations(tail, num_towns - 1) do
      list = [head | x] 
      list
    end ++ combinations(tail, num_towns)
  end

end
_______________________________________
defmodule BestSum do
  
  def best_sum(t, k, ls) do
    create_paths(ls, k)
    |> Enum.map(& Enum.sum(&1))
    |> Enum.filter(& &1 <= t)
    |> case do
      [] -> nil
      scores -> Enum.max(scores)
    end
  end
  
  def create_paths(right, 1), do: Enum.map(right, & [&1])
  def create_paths([], _level), do: []
  def create_paths([item | right], level) do
    paths_starting_by_item = right
    |> create_paths(level - 1)
    |> Enum.map(& [item | &1])
    
    paths_starting_by_item ++ create_paths(right, level)
  end
end
