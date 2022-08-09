568d0dd208ee69389d000016


defmodule Rent do
  def rental_car_cost(d) when d >= 7, do: d * 40 - 50
  def rental_car_cost(d) when d >= 3, do: d * 40 - 20
  def rental_car_cost(d), do: d * 40
end
__________________________
defmodule Rent do
  @base_amount 40
  def rental_car_cost(d) when d in 3..6, do: d * @base_amount - 20
  def rental_car_cost(d) when d >= 7, do: d * @base_amount - 50  
  def rental_car_cost(d), do: d * @base_amount  
end
__________________________
defmodule Rent do
  def rental_car_cost(days), do: 40 * days - discount(days)
  
  defp discount(days) when days >= 7, do: 50
  defp discount(days) when days >= 3, do: 20
  defp discount(_days), do: 0
end
__________________________
defmodule Rent do
  def rental_car_cost(d) do
    base = d * 40
    
    discount =
      cond do
        d >= 7 -> 50
        d >= 3 -> 20
        true -> 0
      end

    base - discount
  end
end
