595970246c9b8fa0a8000086


defmodule Solution do
  def solve(w) do
    String.capitalize(w)
  end
end
______________________
defmodule Solution do
  def solve(w) do
    
    with [head | tail] <- String.codepoints(w) do
    [String.capitalize(head) | tail] |> Enum.join()
    end
  end
end
______________________
defmodule Solution do
  def solve(w) do
    (String.first(w) |> String.upcase) <> String.slice(w, 1..-1)
  end
end
