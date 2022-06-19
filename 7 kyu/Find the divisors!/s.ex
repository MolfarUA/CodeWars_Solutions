544aed4c4a30184e960010f4


defmodule FindTheDivisors do
  def divisors(integer) do
    divs = for n <- 2..integer-1, rem(integer, n) == 0, do: n
    case divs do
      [] -> "#{integer} is prime"
      _ -> divs
    end
  end
end
__________________________________
defmodule FindTheDivisors do
  def divisors(integer) do
    2..(integer - 1)
    |> Enum.filter(&(rem(integer, &1) == 0))
    |> render_divisors(integer)
  end
  
  defp render_divisors([], integer), do: "#{integer} is prime"
  defp render_divisors(divisors, _), do: divisors
end
__________________________________
defmodule FindTheDivisors do
  def divisors(i), do: (for x <- 2..div(i,2)+1, rem(i,x) == 0, do: x) |> prime?(i)
  
  defp prime?([],i), do: "#{i} is prime"
  defp prime?(ls,_), do: ls
end
__________________________________
defmodule FindTheDivisors do
  def divisors(integer) do
    range = 2..(integer - 1)
    divisors = Enum.filter(range, &(rem(integer, &1) == 0))

    case divisors do
      [] -> "#{integer} is prime"
      _ -> divisors
    end
  end
end
__________________________________
defmodule FindTheDivisors do
  def divisors(integer) do
    divisors = (integer - 1)..2
    |> Enum.filter(fn n -> Integer.mod(integer, n) == 0 end)
    |> Enum.sort()

    if(Enum.count(divisors) == 0, do: "#{integer} is prime", else: divisors)
  
  end
end
