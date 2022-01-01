defmodule HumanReadable do
    def format(secs) do
        pad2 = fn n -> n |> Integer.to_string |> String.pad_leading(2, "0") end
        Enum.map_join([div(secs, 3600), div(rem(secs, 3600), 60), rem(secs, 60)], ":", pad2)
    end
end

_____________________________________
defmodule HumanReadable do
  def format(seconds) do
    {hrs, rem} = divmod(seconds, 3600)
    {min, sec} = divmod(rem, 60)
    [hrs, min, sec]
    |> Enum.map(fn(s) -> String.pad_leading(Integer.to_string(s), 2, "0") end)
    |> Enum.join(":")
  end
  
  defp divmod(a, b), do: {div(a, b), rem(a, b)}
end

_____________________________________
defmodule HumanReadable do
  def format(seconds) do
    hh = seconds / 3600 |> trunc
    mm = seconds / 60 |> trunc |> rem(60)
    ss = seconds |> rem(60)
    pad(hh) <> ":" <> pad(mm) <> ":" <> pad(ss)
  end
  
  def pad(number) do
    number
    |> Integer.to_string
    |> String.pad_leading(2, "0")
  end
end

_____________________________________
defmodule HumanReadable do
  def format(seconds) do
    hours = div(seconds, 3600)
    minutes = rem(seconds, 3600) |> div(60)
    seconds = rem(seconds, 60)
    
    [hours, minutes, seconds]
    |> Stream.map(&Integer.to_string/1)
    |> Stream.map(&String.pad_leading(&1, 2, "0"))
    |> Enum.join(":")
  end
end

_____________________________________
defmodule HumanReadable do
  def format(seconds) when seconds == 0, do: "00:00:00"

  def format(seconds) do
    if seconds > 36399 do
      rem = floor(seconds / 86400)

      Time.add(~T[00:00:00], seconds)
      |> Time.to_iso8601()
      |> time
      |> final(rem)
    else
      Time.add(~T[00:00:00], seconds)
      |> Time.to_iso8601()
      |> time
    end
  end

  defp final(time, rem) do
    [head | tail] = String.split(time, ":")
    val = String.to_integer(head)
    val1 = val + rem * 24
    str = Integer.to_string(val1)
    str1 = [str] ++ tail
    Enum.join(str1, ":")
  end

  defp time(string) do
    [head | _tail] = String.split(string, ".")
    head
  end
end
