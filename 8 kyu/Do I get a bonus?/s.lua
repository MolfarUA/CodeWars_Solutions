56f6ad906b88de513f000d96



local solution = {}

function solution.bonus_time(salary, bonus)
    return bonus and "$"..salary * 10 or "$"..salary
end

return solution
__________________________
local solution = {}

function solution.bonus_time(salary, bonus)
  if bonus then
    return '$' .. salary * 10
  end
  return '$' .. salary
end

return solution
__________________________
local solution = {}

function solution.bonus_time(s, b)
 return '$'..s..(b and '0' or "")
end

return solution
__________________________
local solution = {}

function solution.bonus_time(salary, bonus)
    if bonus then
        salary = salary * 10;
    end
    return "$" .. salary;
end

return solution
__________________________
local solution = {}

function solution.bonus_time(salary, bonus)
  return "$" .. salary * (bonus and 10 or 1)
end

return solution
