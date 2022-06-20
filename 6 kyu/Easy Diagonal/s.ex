559b8e46fa060b2c6a0000bf


defmodule Easydiagonal do

  def diagonal(n, p) do
    # your code
    binomial(n + 1, p + 1)
  end

  @spec binomial(integer(), integer()) :: integer()
  def binomial(_n, 0) do
    1
  end

  def binomial(n, x) when (n - x) >= x and x <= n do
    div(Enum.reduce((n - x + 1)..n, 1, fn x, acc -> x * acc end), Enum.reduce(1..x, 1, fn x, acc -> x * acc end))
    #Enum.product is a simpler way to do this than Enum.reduce but CW only supports Elixir 1.11 and Enum.product is available 1.12 onwards
  end

  def binomial(n, x) when x<=n do
    div(Enum.reduce((x + 1)..n, 1, fn x, acc -> x * acc end), Enum.reduce(1..(n - x), 1, fn x, acc -> x * acc end))
  end

end
_____________________________
defmodule Easydiagonal do

  def diagonal(n, p), do: get_diagonal(n, p)

  defp get_diagonal(n, 0), do: n + 1
  defp get_diagonal(n, p), do: get_diagonal(n, p, 0)
  defp get_diagonal(0, _, acc), do: acc
  defp get_diagonal(n, p, acc), do: get_diagonal(n - 1, p, acc + choose(n, p))

  defp choose(n, k), do: div(mul(n - k + 1, n), mul(1, k))

  defp mul(a, b), do: Enum.reduce(a..b, 1, & &1 * &2)

end
_____________________________
defmodule Easydiagonal do
  
  def aux(n, k, i, r) do
    cond do
      i == k + 1  -> r
      true        -> r = div(r * (n - i + 1), i)
                     i = i + 1
                     aux(n, k, i, r)
    end
  end

  def diagonal(n, p) do
    aux(n + 1, p + 1, 1, 1)
  end
  
end
