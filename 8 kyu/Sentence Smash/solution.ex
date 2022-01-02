defmodule SentenceSmasher do
  def smash(words), do: Enum.join(words, " ")
end

_____________________________________
defmodule SentenceSmasher do
  def smash(words) do
    Enum.join(words, " ")
  end
end

_____________________________________
defmodule SentenceSmasher do
  def smash(words) do
    Enum.reduce(words, "", fn
      x, "" -> x
      x, acc -> acc <> " " <> x
    end)
  end
end

_____________________________________
defmodule SentenceSmasher do  
  def smash(words, acc \\ "")
  def smash([], acc), do: acc
  def smash([head | tail], ""), do: smash(tail, head) 
  def smash([head | tail], acc), do: smash(tail, "#{acc} #{head}")
end

