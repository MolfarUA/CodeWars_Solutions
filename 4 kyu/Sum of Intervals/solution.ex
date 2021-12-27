defmodule Kata do
  def sum_of_intervals(intervals) do
    intervals
      |> Enum.sort
      |> Stream.scan(fn {b, e}, {_, x} -> {max(b, x), max(e, x)} end)
      |> Stream.map(fn {b, e} -> e - b end)
      |> Enum.sum
  end
end
_______________________
defmodule Kata do
  def sum_of_intervals(a) do
    a
    |> Enum.map(&do_get_intervals(&1))
    |> List.flatten()
    |> Enum.uniq()
    |> length()
  end
  
  defp do_get_intervals({first, last}) do
    Enum.map(first..last-1, &(&1))
  end
end
______________________
defmodule Kata do
  def sum_of_intervals(xs), do: MapSet.size(walk(MapSet.new(), xs))
  defp walk(res, []), do: res
  defp walk(res, [x | xs]), do: walk(walk2(res, elem(x, 0), elem(x, 1)), xs)
  defp walk2(res, i, b) when i == b, do: res
  defp walk2(res, i, b), do: walk2(MapSet.put(res, i), i + 1, b)
end
___________________________
defmodule Kata do
  def sum_of_intervals(a) do
    Enum.reduce(a, MapSet.new, &add_range/2)
    |> MapSet.size
  end
  
  def add_range({x, y}, acc) when x == y, do: acc
  def add_range({x, y}, acc), do: add_range({x+1, y}, MapSet.put(acc, {x, x+1}))
end
_________________
defmodule Kata, do: def sum_of_intervals(a), do: a |> Enum.flat_map(fn x -> elem(x, 0)..elem(x, 1) - 1 end) |> Enum.uniq |> Enum.count
