53ee5429ba190077850011d4


defmodule SimpleMath, do: def double_integer(x), do: x * 2
__________________________
defmodule SimpleMath do
  def double_integer(x) do
    x * 2
  end
end
__________________________
defmodule SimpleMath, do: def double_integer(x), do: 2*x
__________________________
defmodule SimpleMath do
  def double_integer(x), do: x * 2
end
