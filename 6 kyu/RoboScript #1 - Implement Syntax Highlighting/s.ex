58708934a44cfccca60000c4


defmodule RoboscriptOne do
  def highlight(code) do
    Regex.replace(~r/F+|L+|R+|\d+/, code, &colorize/1)
  end

  defp colorize(x), do: "<span style=\"color: #{color(x)}\">#{x}</span>"

  defp color("F" <> _rest), do: "pink"
  defp color("L" <> _rest), do: "red"
  defp color("R" <> _rest), do: "green"
  defp color(<<n>> <> _rest) when n in ?0..?9, do: "orange"
end
__________________________
defmodule RoboscriptOne do
  def highlight(code) do
    String.replace(code, ~r/[0-9]+/, "<span style=\"color: orange\">\\0</span>")
    |> String.replace(~r/[F]+/, "<span style=\"color: pink\">\\0</span>")
    |> String.replace(~r/[L]+/, "<span style=\"color: red\">\\0</span>")
    |> String.replace(~r/[R]+/, "<span style=\"color: green\">\\0</span>")
  end
end
__________________________
defmodule RoboscriptOne do
  def highlight(code) do
    code
    |> String.replace(~r/F+/, "<span style=\"color: pink\">\\0</span>")
    |> String.replace(~r/L+/, "<span style=\"color: red\">\\0</span>")
    |> String.replace(~r/R+/, "<span style=\"color: green\">\\0</span>")
    |> String.replace(~r/\d+/, "<span style=\"color: orange\">\\0</span>")
  end
end
