defmodule Finder do
  def find_needle(haystack) do
    index =  Enum.find_index(haystack, fn(x) -> x == "needle" end)
    "found the needle at position #{index}"
  end
end
________________________
defmodule Finder do
  def find_needle(haystack) do
    "found the needle at position #{haystack |> Enum.find_index(& &1 == "needle")}"
  end
end
________________________
defmodule Finder do
  @msg "found the needle at position "
  def find_needle(haystack) do
    haystack 
    |> Enum.find_index(&(&1 == "needle"))
    |> convert_to_message
  end
  
  defp convert_to_message(nil), do: @msg <> "0"
  defp convert_to_message(n), do: @msg <> Integer.to_string(n)
end
________________________
defmodule Finder do
  def find_needle(haystack) do
    haystack
    |> Enum.find_index(&(&1 == "needle"))
    |> say_position
  end
  
  defp say_position(position) do
    "found the needle at position " <> to_string(position)
  end
end
________________________
defmodule Finder do
  def find_needle(haystack) do
    i = Enum.find_index(haystack, &(&1 == "needle"))
    "found the needle at position #{i}"
  end
end
