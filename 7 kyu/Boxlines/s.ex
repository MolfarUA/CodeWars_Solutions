defmodule Kata do
  @spec f(pos_integer(), pos_integer(), pos_integer()) :: pos_integer()
  def f(x, y, z) do
    x * (y + 1) * (z + 1) + y * (z + 1) * (x + 1) + z * (x + 1) * (y + 1)
  end
end
_____________________________________
defmodule Kata do

  def f(x, y, z), do: (x * (y + 1) + y * (x + 1)) * (z + 1) + z * (x + 1) * (y + 1)
  
end
_____________________________________
defmodule Kata do

  def f(x, y, z) do
      z*(3*x*y+1+2*(x+y))+2*x*y+x+y
  end
  
end
_____________________________________
defmodule Kata do
  def f(x, 1, 1), do: 4 + 8 * x
  def f(x, y, 1), do: f(x, 1, 1) + (2 * (x + 1) + 2 * x + x + 1) * (y - 1)
  def f(x, y, z), do: f(x, y, 1) + ((x + 1) * (y + 1) + x * (y + 1) + y * (x + 1)) * (z - 1)
end
_____________________________________
defmodule Kata, do: def f(x, y, z), do: x * (y * (3 * z + 2) + 2 * z + 1) + y * (2 * z + 1) + z
