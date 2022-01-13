defmodule Piapprox do

  def iter_pi(epsilon), do: iter_pi(epsilon, 1, 1, 0, 0)
  
  @pi :math.pi
  
  defp iter_pi(epsilon, _num, _den, acc, n) 
    when abs(@pi - 4*acc) <= epsilon, do: [n, trunc10(acc*4)]
  defp iter_pi(epsilon, num, den, acc, n),
    do: iter_pi(epsilon, -num, den + 2, acc + num/den, n + 1)
  
  defp trunc10(x), do: trunc(x*1.0e10)/1.0e10
  
end
________________________________________
defmodule Piapprox do
  # Cache π to save some keystrokes.
  @pi :math.pi()
  
  # The default values for the first iteration.
  def iter_pi(epsilon, pi_4 \\ 0, diff \\ nil, iter \\ 0)
  
  # Returns the current iteration and the calculated value of π when the difference
  # between π/4 and π is smaller than `epsilon`.
  def iter_pi(epsilon, pi_4, diff, iter) when not is_nil(diff) and diff < epsilon do
    [iter, truncate(pi_4 * 4)]
  end
  
  # Calculates the next iteration of π when the difference between π/4 and π is higher
  # than `epsilon`.
  def iter_pi(epsilon, pi_4, _diff, iter) do
    pi_4 = iter_leibniz(pi_4, iter)
    diff = diff(pi_4)
    
    iter_pi(epsilon, pi_4, diff, iter + 1)
  end
  
  # Calculates the `n` iteration of the Leibniz number, provided the given π/4
  # is the value of the `n-1` previous iterations.
  def iter_leibniz(acc_pi_4, n) do
    acc_pi_4 + :math.pow(-1, n) / (2 * n + 1)
  end
  
  # Truncates the value of `n` to 10 digits.
  def truncate(n) do
    trunc(n * :math.pow(10, 10)) / :math.pow(10, 10)
  end
  
  # Calculates the difference between the given π/4 and the actual π.
  def diff(pi_4) do
    abs(pi_4 * 4 - @pi)
  end
end
________________________________________
defmodule Piapprox do

  defp iter_pi_aux(epsilon, cnt, som) do 
    sign = :math.pow(-1, cnt)
    s = som + sign / (2 * cnt + 1)
    r = abs(:math.pi - 4 * s)
    if (r < epsilon) do
      d = (trunc 4 * s * :math.pow(10, 10)) / :math.pow(10, 10)
      [cnt + 1, d]
    else
      iter_pi_aux(epsilon, cnt + 1, s)
    end
  end
  
  def iter_pi(epsilon) do
   iter_pi_aux(epsilon, 0, 0)
  end
  
end
________________________________________
defmodule Piapprox do

  defp iter_pi_aux(epsilon, cnt, som) do 
    sign = :math.pow(-1, cnt)
    s = som + sign / (2 * cnt + 1)
    r = abs(:math.pi - 4 * s)
    if (r < epsilon) do
      d = (trunc 4 * s * :math.pow(10, 10)) / :math.pow(10, 10)
      [cnt + 1, d]
    else
      iter_pi_aux(epsilon, cnt + 1, s)
    end
  end
  
  def iter_pi(epsilon) do
   iter_pi_aux(epsilon, 0, 0)
  end
  
end
________________________________________
defmodule Piapprox do
  @pi :math.pi
  
  def iter_pi(epsilon) do
    upper = @pi + epsilon
    lower = @pi - epsilon
        
    approximate_pi(upper, lower, 0, 1, :plus, 0)
  end
  
  def approximate_pi(upper, lower, candidate, _, _, iteration) when candidate * 4 >= lower and candidate * 4 <= upper do
    [iteration, to_ten_decimal_places(candidate * 4)]
  end
  
  def approximate_pi(upper, lower, candidate, sequence_denom, :minus, iteration) do
    approximate_pi(upper, lower, candidate - (1 / sequence_denom), sequence_denom + 2, :plus, iteration + 1)
  end
  
  def approximate_pi(upper, lower, candidate, sequence_denom, :plus, iteration) do
    approximate_pi(upper, lower, candidate + (1 / sequence_denom), sequence_denom + 2, :minus, iteration + 1)
  end

  def to_ten_decimal_places(n), do: n |> Float.to_string() |> String.slice(0..11) |> String.to_float()
end
