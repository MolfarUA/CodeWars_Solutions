536a155256eb459b8700077e


defmodule Clockwise_spiral do
  @moduledoc """
  Given the dimension, return a square matrix of numbers in clockwise spiral order.
  """
  
  @spec create_spiral(dimension :: integer) :: list(list(integer))
  def create_spiral(n) when n <= 0, do: []
  def create_spiral(n), do: create_spiral([[n * n,]], n * n - 1)
  
  defp create_spiral(spiral, 0), do: spiral

  defp create_spiral(spiral, n) do
    spiral
    |> rotate_cw()
    |> add_row(n)
    |> create_spiral(n-length(spiral))
  end
  
  """
  [
  [9, 8]
  ] ->
  [
  [6, 7],
  [9, 8]
  ]
  """
  defp add_row([row | _] = spiral, n) do
    [n..0
      |> Stream.take(length(row))
      |> Enum.reverse()
      | spiral]
  end
  
  """
  [
  [6, 7],
  [9, 8]
  ] ->
  [
  [9, 6],
  [8, 7]
  ]
  """
  defp rotate_cw(spiral) do
    spiral
    |> Enum.zip()
    |> Enum.map(&(Tuple.to_list(&1) |> Enum.reverse()))
  end
  
end
_________________________
defmodule Clockwise_spiral do
    defp walk(1,1,x), do: [[x]]
    defp walk(n,0,x), do: walk(n,n,x)
    defp walk(n,m,x), do:
        [Enum.to_list(x..x+n-1) | walk(m-1,n,x+n)
                                |> Enum.reverse
                                |> Enum.zip
                                |> Enum.map(&Tuple.to_list/1)]

    def create_spiral(n) when is_integer(n) and n > 0, do: walk(n,0,1)
    def create_spiral(_n), do: []
end
_________________________
defmodule Clockwise_spiral do

  def step_spiral({dx, dy}, [{{x, y}, i}| tail]) do
    [{{x+dx, y+dy}, i+1}, {{x, y}, i}| tail]
  end

  def update_spiral({{x, y}, i}, xs) do
    List.replace_at(xs, y, List.replace_at(Enum.at(xs, y), x, i))
  end

  def create_spiral(n) when n < 1, do: []
  def create_spiral(1), do: [[1]]
  def create_spiral(n) do
    [n-1| Enum.reverse(Enum.flat_map(1..n-1, fn x -> [x, x] end))]
    |> Enum.zip(Stream.cycle([{1,0}, {0,1}, {-1,0}, {0,-1}]))
    |> Enum.map(fn {n, {dx, dy}} -> for _ <- 1..n, do: {dx, dy} end)
    |> List.flatten
    |> Enum.reduce([{{0, 0}, 1}], &step_spiral/2)
    |> Enum.reduce(for _ <- 1..n do for _ <- 1..n, do: 0 end, &update_spiral/2)
  end
  
end
