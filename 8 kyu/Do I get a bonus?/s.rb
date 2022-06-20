56f6ad906b88de513f000d96


def bonus_time(salary, bonus)
  "$#{bonus ? salary * 10 : salary}"
end
__________________________
def bonus_time(salary, bonus)
  "$#{salary * (bonus ? 10 : 1)}"
end
__________________________
def bonus_time(salary, bonus)
  bonus ? "$#{(salary*10).to_s}" : "$#{salary.to_s}"
end
