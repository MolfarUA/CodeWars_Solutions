defmodule Bus do
  def number([]), do: 0
  def number([{add, sub} | stops]) do
    add - sub + number(stops)
  end
end
_____________________________________
defmodule Bus do
  def number(stops) do
    Enum.reduce(stops, 0, fn({get_on, get_off}, total) ->
      total + get_on - get_off
    end)
  end
end
_____________________________________
defmodule Bus do

  @doc """
  Find the final number of people on the bus after given the amount of
  riders getting on and off the bus at each stop.
  """
  @spec number([{non_neg_integer, non_neg_integer}]) :: non_neg_integer
  def number(stops) do
    Enum.reduce(stops, 0, fn
      {a, b}, acc ->
        acc + a - b
    end)
  end
end
_____________________________________
defmodule Bus do
  def number(stops) do
    {on, off} = Enum.unzip(stops)
    Enum.sum(on) - Enum.sum(off)
  end
end
