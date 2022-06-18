544675c6f971f7399a000e79


defmodule Numerify do
  def string_to_number(str), do: String.to_integer(str)
end
_______________________
defmodule Numerify do
  defdelegate string_to_number(s), to: String, as: :to_integer
end
_______________________
defmodule Numerify do
  def string_to_number(str) do
    String.to_integer str
  end
end
_______________________
defmodule Numerify do
  def string_to_number(str) do
    str |> String.to_integer
  end
end
_______________________
defmodule Numerify do
  @number_map %{
    "0" => 0,
    "1" => 1,
    "2" => 2,
    "3" => 3,
    "4" => 4,
    "5" => 5,
    "6" => 6,
    "7" => 7,
    "8" => 8,
    "9" => 9
  }
  def string_to_number(str) do
    str
      |> String.graphemes
      |> Enum.reverse
      |> Stream.with_index
      |> Enum.reduce(0, fn {char, index}, acc ->
        if (char == "-") do
          acc * -1
        else
          number = @number_map |> Map.get(char)
          number = number * :math.pow(10, index)
          acc + number
        end
      end)
  end
end
