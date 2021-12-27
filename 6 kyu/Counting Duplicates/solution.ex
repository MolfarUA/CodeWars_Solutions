defmodule DuplicateCount do

  def count(str) do
    str
    |> String.downcase
    |> String.graphemes
    |> Enum.group_by(fn char -> char end)
    |> Enum.count(fn {_, char_group} -> Enum.count(char_group) > 1 end)
  end

end
____________________________
defmodule DuplicateCount do

  def count(str) do
    str 
    |> String.downcase
    |> String.codepoints
    |> Enum.sort
    |> Enum.chunk_by(&(&1))
    |> Enum.filter(&(Enum.count(&1) >1))
    |> Enum.count
  end

end
_______________________
defmodule DuplicateCount do
  def count(str) do
    str
    |> String.downcase()
    |> String.split("", trim: true)
    |> Enum.frequencies()
    |> Enum.filter(fn {_, v} -> v >= 2 end)
    |> Enum.count()
  end
end
_______________
defmodule DuplicateCount do

  def count(str) do
    str
    |> String.downcase()
    |> String.graphemes()
    |> Enum.reduce(%{}, fn ltr, counts -> Map.update(counts, ltr, 1, fn val -> val + 1 end) end) # map like %{"a" => 2, "b" => 1}
    |> Enum.reduce(0, fn {_,count}, dups -> if count > 1, do: dups+1, else: dups end)
  end

end

______________________
defmodule DuplicateCount do

  def count(str) do
    value = str |> String.downcase 
                |> String.graphemes
                |> Enum.reduce(%{}, fn char, acc ->
                     Map.put(acc, char, (acc[char] || 0) + 1)
                   end)
    Map.keys(value) 
    |> Enum.reduce(0, fn char, acc ->
      if value[char] > 1, do: 1 + acc, else: acc
    end)

  end

end
