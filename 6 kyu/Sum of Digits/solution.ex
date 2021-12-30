defmodule Kata do
    def digital_root(n) when n < 10, do: n
    def digital_root(n), do: Integer.digits(n) |> Enum.sum |> digital_root
end

________________________________
defmodule Kata do
  def digital_root(n), do: rem(n - 1, 9) + 1
end

________________________________
defmodule Kata do
  def digital_root(n) do
    to_charlist(n)
      |> Enum.map(fn i -> i - 48 end)
      |> Enum.sum
      |> recurse
  end
  
  defp recurse(n) when n > 9 do
    digital_root n
  end
  defp recurse(n), do: n
end

________________________________
defmodule Kata do
    def digital_root(n) do
        String.codepoints("#{n}")
        |>sum
    end
    def sum([a]), do: String.to_integer(a)
    def sum(l)do
      Enum.map(l, &String.to_integer/1)
      |> Enum.sum
      |> inspect
      |> String.codepoints
      |> sum
    end
end

________________________________
defmodule Kata do
    def digital_root(n) do
        # Recursion limit check
        if n < 10 do
            n
        else
            # Recursive call
            curr_sum = n |> Integer.digits |> Enum.sum
            digital_root(curr_sum)
        end
    end
end

________________________________
defmodule Kata do
    def digital_root(n) when n < 10 do
      n
    end

    def digital_root(n) do
      digital_root(Integer.to_string(n)
      |> String.split("")
      |> Enum.filter(fn x -> x != "" end)
      |> Enum.map(fn x -> String.to_integer(x) end)
      |> Enum.sum)
    end
end
