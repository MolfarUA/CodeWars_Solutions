55aa075506463dac6600010d


defmodule RecreationOne do
  def list_squared(m, n) do
    m..n
    |> Enum.map(&({&1, getSumOfSquaresOfFactors(&1)}))
    |> Enum.filter(fn {_, sos} -> 
        r = :math.sqrt(sos)
        r - trunc(r) == 0
      end)
  end

  def getSumOfSquaresOfFactors(num) do
    1..(:math.sqrt(num) |> trunc)
    |> Enum.filter(&(rem(num, &1) == 0))
    |> Enum.reduce(0, fn x, acc -> 
        r = div(num, x)
        if x == r, do: acc + x*x, else: acc + x*x + r*r
    end)
  end
end
________________________________
defmodule RecreationOne do
  def list_squared(m, n) do
    m..n
    |> Enum.map(&process_factors/1)
        |> Enum.filter(fn {_,v} -> :math.sqrt(v) |> trunc == :math.sqrt(v) end)
  end

  def process_factors(int) do
   r=  1..floor(:math.sqrt(int))
    |> Enum.reduce([], fn x, acc -> logic(x, int) ++ acc end)
    |> Enum.dedup
    |> Enum.map(&(&1 * &1))
    |> Enum.sum
   {int, r}
  end

  def logic(factor, int) when rem(int, factor) == 0, do: [factor, div(int, factor)]
  def logic(_, _), do: []
end
________________________________
defmodule RecreationOne do

  def list_squared(m, n) do
    factors = m..n |> Enum.map(&process_factors/1)

    m..n
    |> Enum.zip(factors)
    |> Enum.filter(fn {_, r} -> square?(r) end)
  end

  defp process_factors(int) do
    1..floor(:math.sqrt(int))
    |> Enum.reduce([], fn x, acc -> logic(x, int) ++ acc end)
    |> Enum.dedup
    |> Enum.sort
    |> Enum.map(&(&1 * &1))
    |> Enum.sum
  end
  
  defp logic(factor, int) when rem(int, factor) == 0, do: [factor, div(int, factor)]
  defp logic(_, _), do: []
  
  defp square?(int), do: :math.sqrt(int) == round(:math.sqrt(int))
  
end
