defmodule Plural do
  def plural?(n), do: n != 1
end
__________________
defmodule Plural do
  @spec plural?(String.t) :: boolean
  def plural?(0), do: true
  def plural?(n) when n == 1, do: false
  def plural?(n) when is_number(n), do: true
end
__________________
defmodule Plural do
  def plural?(n) do
    if n == 1 do
      false
    else
      true
    end
  end
end
__________________
defmodule Plural do
  def plural?(n) do
    cond do
      n == 0 -> true
      0 < n && n < 1 -> true
      n == 1 -> false
      n > 1 -> true
    end
  end
end
__________________
defmodule Plural do
  def plural?(number), do: number != 1
end
__________________
defmodule Plural do
  def plural?(n) when n == 1, do: false  
  def plural?(n), do: true
end
