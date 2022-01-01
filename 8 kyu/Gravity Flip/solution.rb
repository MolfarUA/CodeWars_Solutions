def flip(dir, boxes)
  dir == "R" ? boxes.sort : boxes.sort.reverse
end

____________________________
def flip(dir, boxes)
  boxes.sort_by(&(dir == 'R' ? :+@ : :-@))
end

____________________________
def flip(dir, boxes)
  eval("boxes.sort#{dir == 'L' ? '.reverse' : ''}")
end

____________________________
def flip(dir, boxes) # declare function taking dir and boxes arguments
  if dir == 'R' # test dir input against the entered input'R'
    boxes.sort # to represent the movement of highest magnitude columns to the right
  elsif dir == 'L' # elsif not else, because an input could be entered other than 'L'
    boxes.sort.reverse # to represent the movement of highest magnitude columns to the left
  end # end 'if elsif' statement
end # end function declaration
