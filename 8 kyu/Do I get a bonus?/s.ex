56f6ad906b88de513f000d96


defmodule Codewars.Reward do
  def bonus_time(salary, false), do: "$#{salary}"
  def bonus_time(salary, true), do: "$#{salary * 10}"
end
__________________________
defmodule Codewars.Reward do
  def bonus_time(salary, true), do: "$#{salary*10}"
  def bonus_time(salary, false), do: "$#{salary}"
end
__________________________
defmodule Codewars.Reward do
  def bonus_time(salary, bonus) do
    if bonus do
      "$" <> "" <> Integer.to_string(salary * 10)  
    else
      "$" <> "" <> Integer.to_string(salary)
    end  
  end
end
