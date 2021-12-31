defmodule Elevator do
  defstruct floor: 0,
            next_floor: 0,
            direction: :up,
            capacity: 0,
            passengers: [],
            visited_floors: [],
            queues: [],
            top_floor: 0,
            idle: false
end

defmodule Kata do
  def the_lift(queues, capacity) do
    top_floor = Enum.count(queues) - 1
    elevator = %Elevator{queues: queues, top_floor: top_floor, capacity: capacity}
    work(elevator)
  end
  
  def work(%Elevator{idle: true, visited_floors: visited_floors}), do:
    Enum.reverse(visited_floors)
  def work(elevator) do
    elevator
    |> record_current_floor()
    |> let_out_passengers()
    |> check_if_elevator_idle()
    |> calculate_next_stop()
    |> take_in_passengers()
    |> work()
  end
  
  def record_current_floor(elevator) do
    %Elevator{next_floor: next_floor, visited_floors: visited_floors} = elevator
    %{ elevator | floor: next_floor, visited_floors: [next_floor | visited_floors] }
  end
  
  def let_out_passengers(elevator) do
    %Elevator{floor: floor, passengers: passengers} = elevator
    new_passengers = Enum.filter(passengers, fn passenger -> passenger != floor end)
    %{ elevator | passengers: new_passengers }
  end
  
  def take_in_passengers(elevator) do
    %Elevator{
      floor: floor,
      queues: queues,
      passengers: passengers,
      capacity: capacity,
      direction: direction
    } = elevator
    queue = Enum.at(queues, floor)
    remaining_capacity = capacity - Enum.count(passengers)
    {getting_on, staying} = get_passengers_from_queue(queue, floor, remaining_capacity, direction)
    new_passengers = passengers ++ getting_on
    new_queues = List.update_at(queues, floor, fn _ -> staying end)
    %{ elevator | queues: new_queues, passengers: new_passengers }
  end
  
  
  defp get_passengers_from_queue(queue, floor, capacity, direction, getting_on \\ [], staying \\ [])
  defp get_passengers_from_queue([], _floor, _capacity, _direction, getting_on, staying), do:
    {getting_on, Enum.reverse(staying)}
  defp get_passengers_from_queue(queue, _floor, 0, _direction, getting_on, staying), do:
    {getting_on, Enum.reverse(staying) ++ queue}
  defp get_passengers_from_queue([head | tail], floor, capacity, direction, getting_on, staying) do
    cond do
      direction == :up && head > floor ->
        get_passengers_from_queue(tail, floor, capacity - 1, direction, [head | getting_on], staying)
      direction == :down && head < floor ->
        get_passengers_from_queue(tail, floor, capacity - 1, direction, [head | getting_on], staying)
      true ->
        get_passengers_from_queue(tail, floor, capacity, direction, getting_on, [head | staying])
    end
  end
  
  def check_if_elevator_idle(elevator) do
    %Elevator{ queues: queues, floor: floor, passengers: passengers } = elevator
    queue_count = Enum.reduce(queues, 0, fn e, acc -> acc + Enum.count(e) end)
    passenger_count = Enum.count(passengers)
    idle = queue_count == 0 && floor == 0 && passenger_count == 0
    %{ elevator | idle: idle }
  end
  
  def calculate_next_stop(elevator) do
    %Elevator{
      passengers: passengers,
      queues: queues,
      top_floor: top_floor,
      floor: current_floor,
      direction: direction,
      capacity: capacity
    } = elevator
    queue = Enum.at(queues, current_floor)
    
    passengers_going_up   = Enum.filter(passengers ++ queue, fn passenger -> passenger >= current_floor end) |> Enum.take(capacity)
    passengers_going_down = Enum.filter(passengers ++ queue, fn passenger -> passenger <= current_floor end) |> Enum.take(capacity)
    
    queues_with_floors = Enum.with_index(queues)
    queuers_going_up   =
      Enum.drop(queues_with_floors, current_floor + 1)
      |> Enum.filter(fn {queue, floor} -> Enum.any?(queue, fn queuer -> queuer > floor end) end)
      |> Enum.map(fn {_queue, floor} -> floor end)
    queuers_going_down =
      Enum.take(queues_with_floors, current_floor)
      |> Enum.filter(fn {queue, floor} -> Enum.any?(queue, fn queuer -> queuer < floor end) end) 
      |> Enum.map(fn {_queue, floor} -> floor end)
    
    anyone_going_up?   = Enum.any?(passengers_going_up,   fn _ -> true end) || Enum.any?(queuers_going_up,   fn _ -> true end)
    anyone_going_down? = Enum.any?(passengers_going_down, fn _ -> true end) || Enum.any?(queuers_going_down, fn _ -> true end)
    
    bottom_floor_with_queuer =
      Enum.reduce_while(queues_with_floors, top_floor, fn {queue, floor}, acc ->
        if Enum.any?(queue, fn _ -> true end), do: {:halt, floor}, else: {:cont, acc}
      end)
    top_floor_with_queuer =
      Enum.reduce(queues_with_floors, 0, fn {queue, floor}, acc ->
        if Enum.any?(queue, fn _ -> true end), do: floor, else: acc
      end)
    
    cond do
      direction == :up && anyone_going_up? ->
        new_floor = Enum.min(passengers_going_up ++ queuers_going_up)
        %{ elevator | next_floor: new_floor, direction: :up }
      direction == :up && current_floor < top_floor_with_queuer ->
        %{ elevator | next_floor: top_floor_with_queuer, direction: :up }
      direction == :up && anyone_going_down? ->
        new_floor = Enum.max(passengers_going_down ++ queuers_going_down)
        %{ elevator | next_floor: new_floor, direction: :down }
      direction == :up && current_floor > bottom_floor_with_queuer ->
        %{ elevator | next_floor: bottom_floor_with_queuer, direction: :down }
      direction == :down && anyone_going_down? ->
        new_floor = Enum.max(passengers_going_down ++ queuers_going_down)
        %{ elevator | next_floor: new_floor, direction: :down }
      direction == :down && current_floor > bottom_floor_with_queuer ->
        %{ elevator | next_floor: bottom_floor_with_queuer, direction: :down }
      direction == :down && anyone_going_up? ->
        new_floor = Enum.min(passengers_going_up ++ queuers_going_up)
        %{ elevator | next_floor: new_floor, direction: :up }
      direction == :down && current_floor < top_floor_with_queuer ->
        %{ elevator | next_floor: top_floor_with_queuer, direction: :up }
      true ->
        %{ elevator | next_floor: 0, direction: :down }
    end
  end
end

___________________________________________________
defmodule Kata do
  def the_lift(queues, capacity) do
    queues
    |> init_state
    |> Map.put(:capacity, capacity)
    |> run_lift
  end
  
  def init_state(queues) do
    Enum.reduce(queues, %{todo: 0}, fn x, acc -> 
      acc
      |> Map.put(map_size(acc) - 1, x)
      |> Map.update!(:todo, &(&1 + length(x)))
    end)
    |> Map.put(:floor, 0)
    |> Map.put(:history, [0])
    |> Map.put(:riders, [])
    |> Map.put(:direction, "UP")
    |> Map.put(:height, length(queues) - 1)
  end
  
  def run_lift(%{:todo => 0} = state), do: state.history |> add_history(0) |> Enum.reverse
  def run_lift(state) do
    state
    |> validate_direction
    |> pick_up
    |> move
    |> drop_off
    |> run_lift
  end
  
  def validate_direction(%{:floor => a, :height => a} = state), do: Map.put(state, :direction, "DN")
  def validate_direction(%{:floor => 0} = state), do: Map.put(state, :direction, "UP")
  def validate_direction(state), do: state
  
  def pick_up(state) do
    {ready, not_ready} =
      Enum.split_with(state[state.floor], fn x -> 
        case state.direction do
          "UP" -> x > state.floor
          "DN" -> x < state.floor
        end
      end)
      
    {taken, cant_fit} = 
      Enum.split(ready, state.capacity - length(state.riders))
      
    state
    |> Map.update!(:riders, &(taken ++ &1))
    |> Map.put(state.floor, not_ready ++ cant_fit)
    |> Map.put(:history, if length(ready) > 0 do add_history(state.history, state.floor) else state.history end)
  end
    
  def move(%{:direction => "UP"} = state), do: Map.update!(state, :floor, &(&1 + 1))
  def move(%{:direction => "DN"} = state), do: Map.update!(state, :floor, &(&1 - 1))
  
  def drop_off(state) do
    {done, waiting} = Enum.split_with(state.riders, &(&1 == state.floor))
    done = length(done)
    
    state
    |> Map.update!(:todo, &(&1 - done))
    |> Map.put(:riders, waiting)
    |> Map.put(:history, if done > 0 do add_history(state.history, state.floor) else state.history end)
  end
  
  def add_history([h | t], h), do: [h | t]
  def add_history([h | t], a), do: [a | [h | t]]
end

___________________________________________________
defmodule Kata do
    def the_lift(queues, capacity) do
        lift(0,[],List.duplicate(0,length(queues)),split_queues(queues),capacity,length(queues),1) |> Enum.dedup
    end
    def lift(floor, stops, insiders, queues, capacity, num_floors, up_down) when floor == num_floors-1 and up_down == 1 do
        lift(floor, stops, insiders, queues, capacity, num_floors,-1)       
    end
    def lift(floor, stops, insiders, queues, capacity, num_floors, up_down) when floor < 0 and up_down == -1 do 
        lift(floor+1, stops, insiders, queues, capacity, num_floors, 1)
    end   
    def lift(floor, stops, insiders, queues, capacity, num_floors, up_down) do 
        if queue_size(queues) == 0 && Enum.sum(insiders) == 0 do
            if Enum.at(stops,-1) == 0, do: stops, else: stops ++ [0] 
        else
            out = Enum.at(insiders,floor) 
            n_insiders = ( if out > 0, do: List.update_at(insiders,floor,&(&1 - out)) ,else: insiders)               
            {passers,n_queues, stop} = get_passers(queues,floor,capacity-Enum.sum(n_insiders), up_down) 
            n_insiders = Enum.reduce(passers,n_insiders, fn el, insiders -> List.update_at(insiders,el,&(&1 + 1)) end)           
            n_stops = (if stop || out > 0 || length(passers)>0 || length(stops) == 0, do: stops ++ [floor], else: stops) 
            lift(floor+up_down, n_stops, n_insiders, n_queues, capacity, num_floors, up_down) 
        end
   end
    defp get_passers(queues, floor, max, up_down) when up_down == -1 do  
       {up,down} = Enum.at(queues,floor)  
       stop = (if length(down) > 0, do: true, else: false) 
       {n_down,down} = Enum.split(down,max)
       {n_down,List.replace_at(queues,floor,{up,down}), stop}
    end
    defp get_passers(queues, floor, max, up_down) when up_down == 1 do  
       {up,down} = Enum.at(queues,floor) 
       stop = (if length(up) > 0, do: true, else: false) 
       {n_up,up} = Enum.split(up,max)
       {n_up,List.replace_at(queues,floor,{up,down}), stop}
    end
    defp split_queues(queues), do: for {arr,ind} <- Enum.with_index(queues), do: Enum.split_with(arr, fn val -> val > ind end) 
    defp queue_size(queue), do: Enum.reduce(queue,0, fn {a1,a2}, acc -> acc + length(a1)+length(a2) end)
end

___________________________________________________
defmodule Kata do
  defmodule Lift do
    defstruct capacity: nil,
      passengers: [],
      floor: 0,
      action: :go_up,
      way: []

    def new(capacity) do
      %Lift{capacity: capacity}
    end

    def add_stop(%Lift{way: way} = lift, stop) do
      %Lift{lift | way: way ++ [stop]}
    end

    def move_up(%Lift{floor: floor} = lift), do: %Lift{lift | floor: floor + 1}
    def move_down(%Lift{floor: floor} = lift), do: %Lift{lift | floor: floor - 1}
    def set_action(%Lift{} = lift, action), do: %Lift{lift| action: action}
  end

  def the_lift(queues, capacity) do
    {lift, state} = init_state(queues, capacity)
    {lift, state} = stop_if_needed(lift, state) # stop at groun floor
    do_lift(Lift.add_stop(lift, 0), state)
  end

  defp init_state(queues, cap) do
    {state, _} =
      queues # [[1], [2]] => %{0 => [1], 1 => [2]}
      |> Enum.reduce({%{}, 0}, fn queue, {map, n} -> {Map.put(map, n, queue), n + 1} end)

    lift = Lift.new(cap)
    {lift, state}
  end

  defp do_lift(%Lift{action: :go_up} = lift, %{} = state) do
    lift = Lift.move_up(lift)
    {lift, state} = stop_if_needed(lift, state)
    process_direction(lift, state)
  end
  defp do_lift(%Lift{action: :go_down} = lift, %{} = state) do
    lift = Lift.move_down(lift)
    {lift, state} = stop_if_needed(lift, state)
    process_direction(lift, state)
  end

  defp process_direction(%Lift{floor: 0, action: :go_down, passengers: []} = lift, %{} = state) do
    if floors_with_folks(state) == [] do
      # end of the way
      Lift.add_stop(lift, 0).way
      |> reduce_list()
    else
      # turning back - and don't forget to make a stop!
      {lift, state} = stop_if_needed(Lift.set_action(lift, :go_up), state)
      do_lift(lift, state)
    end
  end
  defp process_direction(%Lift{action: :go_up, passengers: [], floor: floor} = lift, %{} = state) do
    higher_caller = floors_with_folks(state) |> List.last()
    cond do
      higher_caller == nil ->
        # there's no queues - so we haven't stop here
        do_lift(Lift.set_action(lift, :go_down), state)
      higher_caller <= floor ->
        # turning back - and don't forget to make a stop!
        {lift, state} = stop_if_needed(Lift.set_action(lift, :go_down), state)
        do_lift(lift, state)
      true ->
        do_lift(lift, state)
    end
  end
  defp process_direction(%Lift{} = lift, %{} = state) do
    do_lift(lift, state)
  end

  defp stop_if_needed(%Lift{floor: floor} = lift, %{} = state) do
    pipeline = [&drop_passengers/2, &take_passengers/2]

    pns = passengers_need_stop(lift, state)
    companions = companions(lift, state)

    if pns ++ companions == [] do
      # nobody need stop - just skipping the floor
      {lift, state}
    else
      # stop! (see the "pipeline" variable above)
      {lift, state} =
        Enum.reduce pipeline, {lift, state}, fn x, {l, s} -> apply(x, [l, s]) end
      {Lift.add_stop(lift, floor), state}
    end
  end

  defp passengers_need_stop(%Lift{floor: floor, passengers: passengers}, _) do
    Enum.filter(passengers, fn p -> p == floor end)
  end
  defp companions(%Lift{floor: floor, action: action}, %{} = state) do
    filter_f =
      fn folk ->
        case action do
          :go_up ->
            folk > floor
          :go_down ->
            folk < floor
        end
      end
    queue = state[floor]
    Enum.filter(queue, filter_f)
  end

  defp drop_passengers(%Lift{passengers: passengers, floor: floor} = lift, %{} = state) do
    {%Lift{lift | passengers: Enum.filter(passengers, fn x -> x != floor end)}, state}
  end
  defp take_passengers(%Lift{action: action, passengers: passengers, floor: floor} = lift, %{} = state) do
    queue = state[floor]
    filter_f =
      case action do
        :go_up -> &(&1 > floor)
        :go_down -> &(&1 < floor)
      end

    folks_to_take = Enum.filter(queue, filter_f) |> Enum.take(lift.capacity - length(passengers))
    {
      %Lift{lift | passengers: passengers ++ folks_to_take},
      Map.put(state, floor, queue -- folks_to_take)
    }
  end

  defp floors_with_folks(state) do
    state
    |> Enum.filter(fn {_k, v} -> v != [] end)
    |> Enum.map(fn {k, _} -> k end)
    |> Enum.sort()
  end

  # reducing the result
  # [0, 0, 1, 1, 0] => [0, 1, 0]
  defp reduce_list(list), do: do_reduce_list(list, [])
  defp do_reduce_list([one, two | remains], acc) when one == two do
    do_reduce_list([one] ++ remains, acc)
  end
  defp do_reduce_list([h|tail], acc), do: do_reduce_list(tail, acc ++ [h])
  defp do_reduce_list([], acc), do: acc
end
