55fab1ffda3e2e44f00000c6


defmodule Solution do
  def solve(s) do
    trunc(s / 0.036)
  end
end
__________________________
defmodule Solution do
  def solve(s) do
    s 
    |> cockroach_speed
    |> trunc()
  end
  
  def cockroach_speed(speed), do: speed * 27.778
end
__________________________
defmodule Solution, do: def solve(s), do: (&(&1 / 0.036 )).(s) |> floor
__________________________
defmodule Solution do
  def solve(s), do: trunc(s * 27.7778)
end
__________________________
defmodule Solution do
  def solve(s) do
    floor((s / 60 / 60) * 100_000)
  end
end
__________________________
defmodule Solution do
  def solve(s) do
     s * :math.pow(10,5) / 3600 |> trunc
  end
end
