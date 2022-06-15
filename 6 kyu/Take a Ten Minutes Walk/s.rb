def isValidWalk(walk)
  walk.count('w') == walk.count('e') and
  walk.count('n') == walk.count('s') and
  walk.count == 10
end
__________________________________________
def is_valid_walk(walk)
  walk.size == 10 && ( walk.count('n') == walk.count('s') && walk.count('w') == walk.count('e') ) ? true : false
end
__________________________________________
def is_valid_walk(walk)
  return false if walk.size != 10
  walk_coordinates = {:x=> 0, :y=> 0}
  walk.each do |dir|
    case dir
      when "n"
      walk_coordinates[:y] += 1
      when "s"
      walk_coordinates[:y] -= 1
      when "e"
      walk_coordinates[:x] += 1
      when "w"
      walk_coordinates[:x] -= 1
    end
  end
  walk_coordinates[:x] == 0 && walk_coordinates[:y] == 0
end
__________________________________________
def is_valid_walk(walk)
  #your code here
  if walk.length != 10
    return false
  end
  
  count_hash = Hash.new(0)
  
  walk.each do |direction|
    count_hash[direction] += 1
  end
  
  return count_hash["n"] == count_hash["s"] && count_hash["w"] == count_hash["e"]
end

=begin
  Notes: 1 block = 1 min
          must be eaxtly 10 min long
  take in an array
  
  if length of array does not equal 10 return false
  
  count how many times we go each direction
    set empty hash
    loop over given array counting each time a letter appears
  
  return true if counts n==s e==w
=end
__________________________________________
def is_valid_walk(walk)
  return false if walk.size <= 2
  
  walk = walk[0..10]

  directions = { 'n' => [0, 1], 's' => [0, -1], 'e' => [1, 0], 'w' => [-1, 0] }
  origin = [0, 0]
  position = [0, 0]

  walk.each do |direction|
    position[0] += directions[direction][0]
    position[1] += directions[direction][1]
  end
  position == origin
end
