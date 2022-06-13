def twoSum(numbers, target)
  numbers.each_with_index do |n1, i1|
    numbers.each_with_index do |n2, i2|
      return [i1, i2] if (n1 + n2) == target && i1 != i2
    end
  end
end
________________________________
def two_sum(numbers, target)
  pair = numbers.combination(2).find{ |(a,b)| a+b == target }
  [numbers.index(pair[0]), numbers.rindex(pair[1])]
end
________________________________
def two_sum(numbers, target)
  target_nums = []
  indexes = []
  numbers.each do |outer_loop_num|
    numbers.each do |inner_loop_num|
      if inner_loop_num + outer_loop_num == target
        target_nums << [inner_loop_num, outer_loop_num]
        break
      end
    end
  end
  target_nums = target_nums.max
  target_nums.each do |num|
    indexes << numbers.index(num)
    numbers[numbers.index(num)] = nil
  end
  indexes
end
________________________________
def two_sum(numbers, target)
  result = []
  numbers.each.with_index do |num_1, index_1|
    numbers.each.with_index do |num_2, index_2|
      if index_1 != index_2
        result << [index_1, index_2] if num_1 + num_2 == target
      end
    end
  end
  result[0]
end
