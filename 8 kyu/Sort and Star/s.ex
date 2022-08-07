57cfdf34902f6ba3d300001e


defmodule SortAndStar do
  def two_sort(s) do
    Enum.min(s)
    |> String.graphemes()
    |> Enum.join("***")
  end
end
___________________________
defmodule SortAndStar do
  def two_sort(ss) do
    ss |> Enum.min |> String.codepoints |> Enum.join("***")
  end 
end
___________________________
defmodule SortAndStar do
  def two_sort(s), do: s |> Enum.sort |> List.first() |> String.replace("", "***") |> String.slice(3..-4)
end
