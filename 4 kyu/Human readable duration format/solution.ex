52742f58faf5485cae000b9a


defmodule DurationFormatter do
  @units [
    year: 31536000,
    day: 86400,
    hour: 3600,
    minute: 60,
    second: 1
  ]
  
  def format_duration(0), do: "now"
  def format_duration(seconds) do
    @units
    |> Enum.map_reduce(seconds, fn {unit, n}, s -> {{unit, div(s, n)}, rem(s, n)} end)
    |> elem(0)
    |> Enum.filter(fn {_, n} -> n > 0 end)
    |> Enum.map(fn {unit, 1} -> "1 #{unit}"
                   {unit, n} -> "#{n} #{unit}s" end)
    |> Enum.intersperse(", ")
    |> List.replace_at(-2, " and ")
    |> Enum.join()
  end
end

__________________________________________________
defmodule DurationFormatter do
  @time_units [
    year:   60 * 60 * 24 * 365,
    day:    60 * 60 * 24,
    hour:   60 * 60,
    minute: 60,
    second: 1
  ]
  
  def format_duration(0), do: "now"
  def format_duration(s) do
    @time_units
    |> Enum.map_reduce(s, fn {unit, v}, s -> {{unit, div(s, v)}, rem(s, v)} end)
    |> elem(0)
    |> Enum.filter(fn {_unit, n} -> n > 0 end)
    |> Enum.map_join(", ", &pluralize/1)
    |> String.replace(~r/, (?!.*, )/, " and ")
  end

  defp pluralize({unit, 1}), do: "1 #{unit}"
  defp pluralize({unit, n}), do: "#{n} #{unit}s"
end

__________________________________________________
defmodule DurationFormatter do
  @time_units [
    year:   60 * 60 * 24 * 365,
    day:    60 * 60 * 24,
    hour:   60 * 60,
    minute: 60,
    second: 1
  ]
  
  def format_duration(0), do: "now"
  def format_duration(s) do
    @time_units
    |> Enum.map_reduce(s, fn {unit, v}, s -> {{unit, div(s, v)}, rem(s, v)} end)
    |> elem(0)
    |> Enum.filter(fn {_unit, n} -> n > 0 end)
    |> Enum.map_join(", ", fn {unit, 1} -> "1 #{unit}"
                              {unit, n} -> "#{n} #{unit}s" end)
    |> String.replace(~r/, (?!.*, )/, " and ")
  end
end

__________________________________________________
defmodule CommaString do
    @doc """
    Creates a comma seperated string from a list.

    ## Examples
      iex> CommaString.from_list(["a", "b", "c", "d"])
      "a, b, c and d"
    """
    @spec from_list([String.t]) :: String.t
    def from_list(list) do
        list
        |> Enum.intersperse(", ")
        |> List.replace_at(-2, " and ")
        |> Enum.join
    end
end

defmodule DurationFormatter do
  @doc """
  Formats a number of seconds into a human readable format.

  ## Examples
    iex> DurationFromatter.format_duration(120)
    "2 minutes"
    iex> DurationFromatter.format_duration(500)
    "8 minutes and 20 seconds"
    iex> format_duration(3662)
    "1 hour, 1 minute and 2 seconds"
  """
  @spec format_duration(seconds :: integer) :: String.t
  def format_duration(0), do: "now"
  def format_duration(seconds) do
    seconds
    |> durations_from_seconds
    |> Enum.map(&time_string_part/1)
    |> Enum.filter(&(&1))
    |> CommaString.from_list
  end

  @doc """
  Generates a keyword list of durations from seconds

  return keyword contains:
    - year
    - day
    - hour
    - minute
    - second

  ## Examples
    iex> DurationFormatter.durations_from_seconds(936351)
    [year: 0, day: 10, hour: 20, minute: 5, second: 51]
  """
  @spec durations_from_seconds(seconds :: integer) :: [key: integer]
  def durations_from_seconds(seconds) do
    {d, {h, m, s}} = :calendar.seconds_to_daystime(seconds)
    y = div(d, 365)
    d = rem(d, 365)
    [year: y, day: d, hour: h, minute: m, second: s]
  end

  defp time_string_part({_name, 0}), do: nil
  defp time_string_part({name, 1}), do: "1 #{name}"
  defp time_string_part({name, value}), do: "#{value} #{name}s"
end
