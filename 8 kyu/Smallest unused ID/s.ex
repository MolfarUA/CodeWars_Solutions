55eea63119278d571d00006a


defmodule Order do
  def next_id(ids) do
    Stream.iterate(0, &(&1+1))
    |> Enum.find(fn id -> not id in ids end)
  end
end
______________________
defmodule Order do
  def next_id(ids) do
    ids |> Enum.sort |> Enum.dedup |> Enum.reduce_while(0, fn
      n, n -> {:cont, n + 1}
      _, i -> {:halt, i}
    end)
  end
end
______________________
defmodule Order do
  def next_id(ids) do
    max_val = Enum.max(ids) + 1
    lst = Enum.to_list 0..max_val
    Enum.min(lst -- ids)
  end
end
______________________
defmodule Order do
  def next_id(ids) do
    Enum.find(0..Enum.max(ids)+1, fn id -> not id in ids end)
  end
end
