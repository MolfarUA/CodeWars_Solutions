class Lift
  attr_reader :movement, :direction
  def initialize(fl, cap)
    @floors = fl
    @capacity = cap
    @level = 0
    @direction = 1
    @movement = [0]
    @passengers = []
  end
  def empty?
    @passengers.empty?
  end
  def up?
    @direction == 1
  end
  def down?
    @direction == -1
  end
  def turn!
    @direction = -@direction
    nil
  end

  def same_direction?(pep)
    pep.up? == up? or pep.down? == down?
  end
     
  def min_p_up
    @passengers.select{|p| p.up?}.min{|p1, p2| p1.destination <=> p2.destination}.destination
  end
  def max_p_down
    @passengers.select{|p| p.down?}.max{|p1, p2| p1.destination <=> p2.destination}.destination
  end
  def min_up
    idx = @floors[@level + 1, @floors.size - @level - 1].index{|f| f.people.any?{|p| p.up?}}
    idx += @level + 1 if idx
  end  
  def top_down
    idx = @floors[@level + 1, @floors.size - @level - 1].rindex{|f| f.people.any?{|p| p.down?}}
    idx += @level + 1 if idx
  end  
  def bottom_up
    @floors[0, @level].index{|f| f.people.any?{|p| p.up?}}
  end  
  def max_down
    @floors[0, @level].rindex{|f| f.people.any?{|p| p.down?}}
  end
  def after_turn
    @floors[@level].people.any?{|p| same_direction?(p)} ? @level : nil
  end
  def move_bottom
    @movement << 0 unless @level == 0
    nil
  end  

  def next_floor()
    next_level = nil
    if empty?
      calls = {
        true =>  [ method(:min_up), method(:top_down), method(:turn!), method(:after_turn), method(:max_down), method(:bottom_up), method(:move_bottom)],
        false => [ method(:max_down), method(:bottom_up), method(:turn!), method(:after_turn), method(:min_up), method(:top_down), method(:move_bottom)]
      }
      calls[up?].each do |c|
        next_level = c.call()
        break if next_level
      end
    else
      if up?
        next_p_level = min_p_up
        next_level = min_up
        next_level = next_p_level if next_level.nil? or next_p_level < next_level
      else
        next_p_level = max_p_down
        next_level = max_down
        next_level = next_p_level if next_level.nil? or next_p_level > next_level
      end
    end
    next_level
  end

  def stop(stop_level)
    @movement << stop_level if stop_level != @level
    @level = stop_level
    @passengers.reject!{|p| p.destination == stop_level}
    rest_people = []
    @floors[stop_level].people.each_with_index do |p, idx|
      if(same_direction?(p) and @passengers.size < @capacity)
        @passengers << p
      else
        rest_people << p
      end
    end
    @floors[stop_level].people = rest_people
  end
end

class People
attr_accessor :level, :destination
  def initialize(lev, dest)
    @destination = dest
    @level = lev
  end
  def up?
    @destination > level
  end  
  def down?
    @destination < level
  end  
end

class Floor
attr_accessor :people
  def initialize(pep, level)
    @people = pep.map{|dest| People.new(level, dest)}
  end
end  

class Building
attr_reader :lift
  def initialize(queues, cap)
    floors = queues.each_with_index.map{|q, level| Floor.new(q, level)}
    @lift = Lift.new(floors, cap)
  end
  def move
    next_level = 0
    while(next_level)
      lift.stop(next_level) 
      next_level = lift.next_floor()
    end
  end

  def result
    @lift.movement
  end  
end

def the_lift(queues, capacity)
  b = Building.new(queues, capacity)
  b.move
  b.result
end

___________________________________________________
def the_lift(queues, capacity)
  @direction = "up"
  @current_floor = 0
  @visited_floors = [0]
  @capacity = capacity
  @passengers = []
  @queues = []
  queues.each_with_index do |queue, index|
    @queues << [index, queue]
  end
  drop_and_take_people
  until finished?
    @current_floor = nearest_floor_to_go
    @visited_floors << @current_floor
    drop_and_take_people
    check_if_switch_direction
  end
  @visited_floors << 0 unless @visited_floors.last == 0
  return @visited_floors
end

def nearest_floor_to_go
  if (@current_floor - nearest_people_waiting_floor).abs < (@current_floor - nearest_people_to_drop_floor).abs
    nearest_people_waiting_floor
  else
    nearest_people_to_drop_floor
  end
end

def nearest_people_waiting_floor
  if @direction == "up"
    floors = @queues[@current_floor+1..].select { |queue| queue[1] && !queue[1].empty? }
    people_going_up_floor = floors&.find { |floor| floor[1].any? { |waiting_person| waiting_person > floor[0] } }
    floor = people_going_up_floor.nil? && nearest_people_to_drop_floor == 1000 ? floors&.last : people_going_up_floor
    floor.nil? ? 1000 : floor[0]
  else
    floors = @queues[...@current_floor].select { |queue| queue[1] && !queue[1].empty? }
    people_going_down_floor = floors&.select { |floor| floor[1].any? { |waiting_person| waiting_person < floor[0] } }&.last
    floor = people_going_down_floor.nil? && nearest_people_to_drop_floor == 1000 ? floors&.first : people_going_down_floor
    floor.nil? ? 1000 : floor[0]
  end
end

def nearest_people_to_drop_floor
  if @direction == "up"
    floor = @passengers.select { |passenger| passenger > @current_floor }.min
    floor = 1000 if floor.nil?
  else
    floor = @passengers.select { |passenger| passenger < @current_floor }.max
    floor = 1000 if floor.nil?
  end
  floor
end

def drop_and_take_people
  @passengers.each { |passenger| @passengers.delete(passenger) if @current_floor == passenger }
  @queues[@current_floor][1] = @queues[@current_floor][1]&.map do |waiting_person| 
    drop_actions(waiting_person)
  end.compact
end

def drop_actions(waiting_person)
  if @direction == "up"
    if waiting_person > @current_floor && @passengers.count < @capacity
      waiting_person = remove_person(waiting_person)
    elsif up_floors_empty? && no_up_going_person? && @passengers.count < @capacity
      waiting_person = remove_person(waiting_person)
    end
  else
    if waiting_person < @current_floor && @passengers.count < @capacity
      waiting_person = remove_person(waiting_person)
    elsif down_floors_empty? && no_down_going_person? && @passengers.count < @capacity
      waiting_person = remove_person(waiting_person)
    end
  end
  waiting_person
end

def switch_direction
  @direction = @direction == "up" ? "down" : "up"
end

def remove_person(waiting_person)
  @passengers&.<<(waiting_person)
  nil
end

def check_if_switch_direction
  if @direction == "up"
    switch_direction unless !up_floors_empty? || @passengers.any? { |passenger| passenger > @current_floor }
  else
    switch_direction unless !down_floors_empty? || @passengers.any? { |passenger| passenger < @current_floor }
  end
end

def up_floors_empty?
  !@queues[@current_floor+1..].any? { |queue| queue[1] && !queue[1].empty? }
end

def no_up_going_person?
  !@passengers.any? { |passenger| passenger > @current_floor } && !@queues[@current_floor][1].any? { |waiting_person| waiting_person > @current_floor }
end

def down_floors_empty?
  !@queues[...@current_floor].any? { |queue| queue[1] && !queue[1].empty? }
end

def no_down_going_person?
  !@passengers.any? { |passenger| passenger < @current_floor } && !@queues[@current_floor][1].any? { |waiting_person| waiting_person < @current_floor }
end

def finished?
  @queues.map(&:last).flatten.empty? && @passengers.empty?
end

___________________________________________________
INITIAL_FLOOR = 0
UP = 1
DOWN = -1

def the_lift(queues, capacity)
  floor = INITIAL_FLOOR
  direction = UP
  lift_members = []
  result = []

  while queues.any?(&:any?) || lift_members.any?
    people_going_wanting_to_come_in = queues[floor].select do |destination|
      (destination - floor) * direction > 0
    end
    # The instructions say it, we stop if someone wants
    # to come in, even if there is no capacity
    if lift_members.any? { |x| x == floor } || people_going_wanting_to_come_in.any?
      result << floor unless result.last == floor
    end

    lift_members.reject! { |x| x == floor }
    while lift_members.size < capacity && people_going_wanting_to_come_in.any?
      # We take the next person in line
      next_person_in_line = people_going_wanting_to_come_in.delete_at(0)
      # We remove him from the floor
      index = queues[floor].find_index(next_person_in_line)
      queues[floor].delete_at(index)
      # We add him to our lift
      lift_members << next_person_in_line
    end
    
    someone_to_drop_later = begin
      lift_members.any? { |destination| (destination - floor) * direction > 0 }
    end
    
    someone_to_take_later = begin
      if direction == UP
        queues[(floor + 1)..-1].any?(&:any?)
      else
         floor == 0 ? false : queues[0..(floor-1)].any?(&:any?)
      end
    end
    
    if someone_to_drop_later || someone_to_take_later
      # We keep going
      floor += direction
    else
      # We change direction
      direction *= -1
    end
    
  end
  
  result << 0 unless result.last == 0
  result.unshift(0) unless result.first == 0
  result
end

___________________________________________________
INITIAL_FLOOR = 0
UP = 1
DOWN = -1
DEBUG = true

def the_lift(queues, capacity)
  floor = INITIAL_FLOOR
  direction = UP
  lift_members = []
  result = [0]
  
  step = 0
  puts "queues, #{queues}"
  puts "capacity, #{capacity}"
  while queues.any?(&:any?) || lift_members.any?
    step += 1
    puts "STEP #{step} - floor #{floor}" if DEBUG
    puts "lift_members, #{lift_members}" if DEBUG
    puts "floor, #{queues[floor]}" if DEBUG
    puts "result, #{result}" if DEBUG
    
    proper = queues[floor].select do |destination|
      (destination - floor) * direction > 0
    end
    if lift_members.any? { |x| x == floor } || proper.any?
      result << floor unless result.last == floor
    end

    lift_members.reject! { |x| x == floor }
    while (lift_members.size < capacity && proper.any?)
      c = proper.delete_at(0)
      queues[floor].delete_at(queues[floor].find_index(c))
      # puts "c, #{c}" if DEBUG
      lift_members << c
    end
    
    someone_to_drop_later = begin
      # lift_members.any? { (destination - floor) * direction > 0 }
      if direction == UP
        lift_members.any? { |destination| destination > floor }
      else
        lift_members.any? { |destination| destination < floor }
      end
    end
    
    someone_to_take_later = begin
      if direction == UP
        queues[(floor + 1)..-1].any?(&:any?)
      else
         floor == 0 ? false : queues[0..(floor-1)].any?(&:any?)
      end
    end
    
    puts "someone_to_drop_later, #{someone_to_drop_later}" if DEBUG
    puts "someone_to_take_later, #{someone_to_take_later}" if DEBUG
    
    if someone_to_drop_later || someone_to_take_later
      floor += direction
    else
      direction *= -1
    end
    
    puts "\n" if DEBUG
  end
  
  result << 0 unless result.last == 0
  
  result
end

def drop_arrivals
  lift_members.reject! { |x| x == floor }
end

def get_new_members
  while (lift_members.size < capacity && queues[floor].any?)
    lift_members << queues[floor].delete_at(0)
  end
end

def someone_to_drop_later
  if direction == UP
    lift_members.any? { |destination| destination > floor }
  else
    lift_members.any? { |destination| destination < floor }
  end
end

def someone_to_take_later
  if direction == UP
    queues[(floor + 1)..-1].any?(&:any?)
  else
    queues[0..(floor-1)].any?(&:any?)
  end
end

def keep_going
  if direction == UP
    floor += 1
  else
    floor -=1
  end
end

def change_direction
  if direction == UP
    direction = DOWN
    floor -= 1
  else
    direction = UP
    floor +=1
  end
end

def act
  drop_arrivals
  get_new_members
  if someone_to_drop_later || someone_to_take_later
    keep_going
  else
    change_direction
  end
end
