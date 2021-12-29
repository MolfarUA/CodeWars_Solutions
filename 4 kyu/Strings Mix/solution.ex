defmodule StringMix do
  def mix(s1, s2) do
    cf1 = s1 |> get_chars_frequency
    cf2 = s2 |> get_chars_frequency

    (cf1 ++ cf2)
    |> Keyword.keys()
    |> Enum.reduce([], fn k, acc ->
      [compare_chars_frequency(k, Keyword.get(cf1, k, 1), Keyword.get(cf2, k, 1)) | acc]
    end)
    |> Enum.filter(fn {_, f, _} -> f > 1 end)
    |> Enum.uniq()
    |> Enum.sort_by(fn {comp, freq, ch} -> {-freq, comp, ch} end)
    |> Enum.map(&format_frequencies/1)
    |> Enum.join("/")
  end

  defp get_chars_frequency(str) do
    str
    |> String.replace(~r/[^a-z]/, "")
    |> String.codepoints()
    |> Enum.group_by(& &1)
    |> Enum.map(fn {k, v} -> {String.to_atom(k), Enum.count(v)} end)
  end

  defp compare_chars_frequency(ch, f1, f2) do
    cond do
      f1 == f2 -> {'=', f1, ch}
      f1 > f2 -> {'1', f1, ch}
      f1 < f2 -> {'2', f2, ch}
    end
  end

  defp format_frequencies({comp, freq, ch}) do
    seq = String.duplicate(Atom.to_string(ch), freq)

    "#{comp}:#{seq}"
  end
end

__________________________________________________
defmodule StringMix do
  @alphabet "abcdefghijklmnopqrstuvwxyz"
  
  def mix(s1, s2) do
    [s1, s2]
    |> Stream.map(&String.graphemes/1)
    |> Enum.map(&count_lowercase/1)
    |> make_result
  end
  
  def make_result([map1, map2]) do
    @alphabet
    |> String.graphemes
    |> check_each_letter(map1, map2)
    |> Enum.sort_by(&{-String.length(&1), String.at(&1, 0), String.at(&1, 2)})
    |> Enum.join("/")
  end
  
  # Creates the appropriate output substring (if any) for each
  # letter of the alphabet
  def check_each_letter(alpha_list, map1, map2) do
    Enum.reduce(alpha_list, [], fn letter, acc ->
      case {map1[letter], map2[letter]} do
        {a, a} when a > 1 ->
          ["=:" <> String.duplicate(letter, a) | acc]
        {a, b} when a <= 1 and b <= 1 ->
          acc
        {a, b} when a > b ->
          ["1:" <> String.duplicate(letter, a) | acc]
        {a, b} when a < b ->
          ["2:" <> String.duplicate(letter, b) | acc]
      end
    end)
  end
  
  # Creates a map of character frequency, only considers lowercase letters
  def count_lowercase(enumerable) do
    Enum.reduce(enumerable, alpha_map(), fn key, acc ->
      case acc do
        %{^key => value} -> %{acc | key => value + 1}
        %{} -> acc
      end
    end)
  end
  
  # Initializes a map of zeroes for each lowercase letter
  defp alpha_map do
    @alphabet
    |> String.graphemes
    |> Enum.reduce(%{}, &Map.put(&2, &1, 0))
  end
end

__________________________________________________
defmodule StringMix do

  def mix(s1, s2) do
   comparator = fn s1,s2 -> if String.length(s1)==String.length(s2),
                           do:   s1 <= s2,
                          else: String.length(s1) >= String.length(s2)
                          end
    Enum.uniq(String.codepoints(s1 <> s2))
    |> Enum.filter(fn x -> x =~ ~r/^\p{Ll}$/u end)
    |> Enum.map(fn x ->
     ns1 = Enum.count(String.codepoints(s1), fn y -> x==y end)
     ns2 = Enum.count(String.codepoints(s2), fn y -> x==y end)
     cond do
      (ns1 == 1 or ns1 == 0) and (ns2 == 1 or ns2 == 0) ->
       "r"
      ns1 > ns2 ->
       {ns1, {"1", x}}
      ns1 < ns2 ->
       {ns2, {"2", x}}
      true ->
       {ns1, {"=", x}}
     end
    end)
    |> Enum.filter(fn x-> x != "r" end)
    |> Enum.map(fn x -> elem(elem(x, 1), 0) <> ":" <> String.duplicate(elem(elem(x, 1), 1), elem(x, 0)) <>  "/" end)
    |> Enum.sort(comparator)
    |> List.to_string()
    |> String.trim_trailing("/")
  end

end

__________________________________________________
defmodule StringMix do
  
  def mix(s1, s2) do
    counts_s1 = count_downcases(s1)
    counts_s2 = count_downcases(s2)
    
    Enum.concat(Map.keys(counts_s1), Map.keys(counts_s2)) 
    |> Stream.uniq
    |> Stream.map(&pick_max(&1, counts_s1, counts_s2))
    |> Stream.reject(fn {_,_,1} -> true; _ -> false end)
    |> Enum.sort_by(&(&1), &comparator/2)
    |> Enum.map(&to_str/1)
    |> Enum.join("/")
  end

  def count_downcases(str) do
    str
    |> String.graphemes
    |> Enum.group_by(&Regex.run(~r/[a-z]/, &1))
    |> Map.delete(nil)
  end
  
  def pick_max(key = [char], counts_s1, counts_s2) do
    count_s1 = counts_s1 |> Map.get(key, []) |> Enum.count
    count_s2 = counts_s2 |> Map.get(key, []) |> Enum.count
    
    cond do
      count_s1 == count_s2  -> {char, "=", count_s1}
      count_s1 > count_s2   -> {char, "1", count_s1}
      true                  -> {char, "2", count_s2}
    end
  end
  
  defp comparator({chr1, pre, cnt}, {chr2, pre, cnt}), do: chr1 <= chr2
  defp comparator({_, pre1, cnt}, {_, pre2, cnt}),     do: pre1 <= pre2
  defp comparator({_, _, cnt1}, {_, _, cnt2}),         do: cnt1 >  cnt2
  
  defp to_str({char, prefix, count}) do
    "#{prefix}:#{String.duplicate(char, count)}"
  end
end

__________________________________________________
defmodule StringMix do
  @alphabet for n <- ?a..?z, do: <<n>>

  def mix(s1, s2) do
    @alphabet
    |> Enum.filter(fn letter -> count(s1, letter) > 1 || count(s2, letter) > 1 end)
    |> Enum.map(fn letter -> build_string(letter, s1, s2) end)
    |> Enum.sort_by(
      fn string -> {-String.length(string), String.at(string, 0), String.at(string, 2)} end,
      &<=/2
    )
    |> Enum.join("/")
  end

  defp build_string(letter, s1, s2) do
    count1 = count(s1, letter)
    count2 = count(s2, letter)

    cond do
      count1 > count2 -> "1:#{String.duplicate(letter, count1)}"
      count1 < count2 -> "2:#{String.duplicate(letter, count2)}"
      count1 = count2 -> "=:#{String.duplicate(letter, count1)}"
    end
  end

  defp count(word, letter) do
    word
    |> String.graphemes()
    |> Enum.count(&(&1 == letter))
  end
end


__________________________________________________
defmodule StringMix do
  @alphabet for n <- ?a..?z, do: <<n>>

  def mix(s1, s2) do
    @alphabet
    |> Enum.filter(fn letter -> count(s1, letter) > 1 || count(s2, letter) > 1 end)
    |> Enum.map(fn letter -> build_string(letter, s1, s2) end)
    |> Enum.sort_by(
      fn string -> {-String.length(string), String.at(string, 0), String.at(string, 2)} end,
      &<=/2
    )
    |> Enum.join("/")
  end

  defp build_string(letter, s1, s2) do
    count1 = count(s1, letter)
    count2 = count(s2, letter)

    cond do
      count1 > count2 -> "1:#{String.duplicate(letter, count1)}"
      count1 < count2 -> "2:#{String.duplicate(letter, count2)}"
      count1 = count2 -> "=:#{String.duplicate(letter, count1)}"
    end
  end

  defp count(word, letter) do
    word
    |> String.graphemes()
    |> Enum.count(&(&1 == letter))
  end
end

StringMix.mix("looping is fun but dangerous", "less dangerous than coding")
