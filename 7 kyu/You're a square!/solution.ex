defmodule Math do
  def square?(n) when n < 0, do: false
   
   def square?(n), do: :math.sqrt(n) == round(:math.sqrt(n))
end
__________________________________
defmodule Math do
  def square?(n) when n < 0, do: false
  def square?(n), do: trunc(:math.sqrt(n)) == :math.sqrt(n)
end
__________________________________
defmodule Math do
    def square?(n) when is_number(n) and n>=0 do
        Float.floor(:math.sqrt(n)) == :math.sqrt(n)
    end
    def square?(n), do: false
end
__________________________________
defmodule Math do
  def square?(n) do
      square?(n,0)
    end

    defp square?(n,i) when (i * i) == n, do: true

    defp square?(n,i) when (i * i) < n, do: square?(n,i+1)

    defp square?(n,i) when (i * i) > n, do: false
end
__________________________________
defmodule Math do
  def square?(n) when n < 0, do: false  
  def square?(n) do
    Enum.any?(1..n, fn x -> x * x == n end)
  end
end
