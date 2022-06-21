5254ca2719453dcc0b00027d


defmodule Kata do
  def permutations(s), do: s |> String.graphemes |> run |> join |> Enum.uniq
  
  defp run([]), do: [[]]
  defp run(s) do
    for x <- s,
        y <- run(s -- [x]) do
        [x | y]
    end
  end
  
  defp join(ss), do: Enum.map(ss, &Enum.join/1)
end
______________________________
defmodule Kata do
  def permutations(<<_>> = s), do: [s]

  def permutations(s) do
    for {c, i} <- String.codepoints(s) |> Enum.with_index(), reduce: MapSet.new() do
      a ->
        {h, <<_, t::binary>>} = String.split_at(s, i)

        for s <- permutations(h <> t), reduce: MapSet.new() do
          b -> MapSet.put(b, c <> s)
        end
        |> MapSet.union(a)
    end
    |> MapSet.to_list()
  end
end
______________________________
defmodule Kata do
  def stuff([]) do
    [[]]
  end

  def stuff(list) do
    for h <- list, t <- stuff(list -- [h]), do: [h | t]
  end

  def permutations(s) do
      s
      |> String.split("", trim: true)
      |> stuff()
      |> Enum.uniq()
      |> Enum.map(
        fn i ->
          i |> Enum.join("")
        end
      )
  end


end
