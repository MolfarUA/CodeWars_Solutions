defmodule Kata do
  def list_position(word) do
    char_counts = get_char_counts(word)
    
    permutation_count(word, char_counts)
  end
  
  def permutation_count(<<char::binary-size(1)>>, _char_counts), do: 1
  def permutation_count(<<char::binary-size(1)>> <> rest, char_counts) do
    permutation_count =
      get_ordered_chars(char_counts)
      |> Enum.take_while(fn e -> e != char end)
      |> Enum.reduce(0, fn e, acc ->
        Map.update!(char_counts, e, &(&1 - 1))
        |> permutation_count()
        |> then(&(&1 + acc))
      end)
    new_char_counts = Map.update!(char_counts, char, &(&1 - 1))
    permutation_count + permutation_count(rest, new_char_counts)
  end
  def permutation_count(char_counts) do
    digits = Enum.reduce(char_counts, 0, fn {_, c}, acc -> acc + c end)
    full_factorial = factorial(digits)
    Enum.reduce(char_counts, full_factorial, fn {_, c}, acc -> div(acc, factorial(c)) end)
  end

  def get_char_counts(word) do
    String.graphemes(word)
    |> Enum.sort()
    |> Enum.reduce([], fn e, acc ->
      case acc do
        [{^e, count} | tail] -> [{e, count + 1} | tail]
        list -> [{e, 1} | list]
      end
    end)
    |> Map.new()
  end
  
  def get_ordered_chars(char_counts) do
    char_counts
    |> Enum.filter(fn {_, i} -> i != 0 end)
    |> Enum.map(&elem(&1, 0))
    |> Enum.sort()
  end
  
  def factorial(n), do: factorial(n, 1)
  defp factorial(0, acc), do: acc
  defp factorial(1, acc), do: acc
  defp factorial(n, acc), do: factorial(n - 1, acc * n)
  
  defp then(x, func), do: func.(x)
end

___________________________________________________
defmodule Kata do
    def position([]), do: 0
    def position(word) do
      [x|tail] = word
      freq = count(word)
      div(
        (tail |> Enum.filter(& &1 < x) |> Enum.count ) * factorial(Enum.sum(freq |> Map.values) - 1),
        freq |> Map.values |> Enum.map(&factorial/1) |> Enum.reduce(1, &*/2)
      ) + position(tail)
    end
    def count(xs) do
      xs |> Enum.reduce(%{}, fn x, acc -> Map.update(acc, x, 1, & &1+1) end)
    end
    def factorial(0), do: 1
    def factorial(n), do: n * factorial(n-1)
    def list_position(word) do
        (word |> to_charlist |> position) + 1
    end
end

___________________________________________________
defmodule Kata do
  @type word_gb :: :gb_trees.tree(char, integer)

  defp fact(0, ac), do: ac
  defp fact(n, ac), do: fact(n - 1, n * ac)

  @spec fact(non_neg_integer) :: non_neg_integer
  defp fact(n), do: fact(n, 1)

  @spec permutations(word_gb) :: integer
  defp permutations(word_gb) do
    multiplicities = :gb_trees.values(word_gb)
    length = multiplicities |> Enum.sum()
    numerator = fact(length)
    denominator = multiplicities |> Enum.map(&fact/1) |> Enum.reduce(1, &(&1 * &2))
    div(numerator, denominator)
  end

  @spec take_letter(word_gb, char) :: word_gb
  defp take_letter(word_gb, letter) do
    case :gb_trees.get(letter, word_gb) do
      1 -> :gb_trees.delete(letter, word_gb)
      c -> :gb_trees.update(letter, c - 1, word_gb)
    end
  end

  @spec list_position(charlist, charlist, word_gb, non_neg_integer) :: non_neg_integer
  defp list_position([], _, _, ac), do: ac

  defp list_position([c | cs], [c | _], word_gb, ac) do
    word_gb = take_letter(word_gb, c)
    letters = :gb_trees.keys(word_gb)
    list_position(cs, letters, word_gb, ac)
  end

  defp list_position(cs, [o | os], word_gb, ac) do
    list_position(cs, os, word_gb, ac + (word_gb |> take_letter(o) |> permutations()))
  end

  @spec list_position(String.t()) :: non_neg_integer
  def list_position(word) do
    cs = word |> String.to_charlist()
    word_gb = cs |> Enum.frequencies() |> Enum.sort_by(&elem(&1, 0)) |> :gb_trees.from_orddict()
    letters = :gb_trees.keys(word_gb)
    list_position(cs, letters, word_gb, 1)
  end
end

___________________________________________________
defmodule Kata do
    def list_position(""), do: 0
    def list_position(word) do
        # Return the anagram list position of the word
        # TODO:
        # For each character, return the number of permutations that would have characters less than
        # the character in that position, given fixed previous characters.
        # TODO: don't calculate counts/order every iteration
        if String.length(word) == 1 do
          1
        else
          counts = word
          |> String.graphemes
          |> Enum.frequencies
        
          # order is the alphabetical order of letters of the word
          order = word
          |> String.graphemes
          |> Enum.sort
          |> Enum.dedup
        
          f = String.first(word)
          rest = String.slice(word, 1..String.length(word))
          i = Enum.find_index(order, &(&1 == f)) # index of f in order
        
          # for each lesser character which could have been in position f,
          # calculate the total number of permutations
          permutations = if i == 0 do
            0
          else
            order
            |> Enum.slice(0..i-1) # all elements in order before f
            |> Enum.reduce(0, fn(x, acc) -> 
              n = String.length(word) - 1
              new_counts = Map.replace(counts, x, counts[x] - 1)
              # must use div rather than / operator to avoid inaccuracy:
              acc + div(factorial(n), (Map.values(new_counts) |> Enum.map(&factorial/1) |> Enum.reduce(1, &(&1 * &2))))
            end)
          end
          permutations + list_position(rest)
      end
    end
    
    def factorial(0), do: 1
    def factorial(n) when n > 0 do
      n * factorial(n - 1)
    end
end
