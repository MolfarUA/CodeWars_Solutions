class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.queues = [list(queue) for queue in queues]
        self.capacity = capacity
        self.floor = 0
        self.direction = "up"
        self.lift = []
        print(self.queues)
        print(self.capacity)

    def is_empty(self):
        return sum(map(len, self.queues)) == 0

    @property
    def top_floor(self):
        return len(self.queues)-1

    def get_off(self):
        # print("get_off", self.floor, list(filter(lambda p: p == self.floor, self.lift)))
        self.lift = list(filter(lambda p: p != self.floor, self.lift))

    def get_on(self):
        if self.direction == "up":
            get_on_list = list(filter(lambda p: p > self.floor, self.queues[self.floor]))[:self.capacity-len(self.lift)]
        else:
            get_on_list = list(filter(lambda p: p < self.floor, self.queues[self.floor]))[:self.capacity-len(self.lift)]
        # print("get_on", self.floor, get_on_list)
        self.lift += get_on_list
        for p in get_on_list:
            self.queues[self.floor].pop(self.queues[self.floor].index(p))

    def up_pushed_floors(self, floor_range):
        '''
            return the list of floors whose up button is pushed
        '''
        return set(floor for floor, queue in enumerate(self.queues) if queue and max(queue) > floor) & set(floor_range)

    def down_pushed_floors(self, floor_range):
        '''
            return the list of floors whose down button is pushed
        '''
        return set(floor for floor, queue in enumerate(self.queues) if queue and min(queue) < floor) & set(floor_range)

    @property
    def upward_floors(self):
        return range(self.floor+1, self.top_floor+1)

    @property
    def downward_floors(self):
        return range(0, self.floor)

    def move(self):
        '''
            move the lift
            return:
                True (if the lift moves), False (otherwise)
        '''
        current_floor = self.floor
        if self.lift:
            if self.direction == "up":
                next_get_on = min(self.up_pushed_floors(self.upward_floors), default=self.top_floor+1)
                next_get_off = min(self.lift)
                self.floor = min(next_get_on, next_get_off)
            else:
                next_get_on = max(self.down_pushed_floors(self.downward_floors), default=-1)
                next_get_off = max(self.lift)
                self.floor = max(next_get_on, next_get_off)
        elif not self.is_empty():
            if self.direction == "up":
                up = min(self.up_pushed_floors(self.upward_floors), default=self.top_floor+1)
                down = max(self.down_pushed_floors(range(self.floor, self.top_floor+1)), default=-1)
                if up <= self.top_floor:
                    self.floor = up
                elif down >= 0:
                    self.floor = down
                    self.direction = "down"
                else:
                    self.direction = "down"
                    return self.move()
            else:
                up = min(self.up_pushed_floors(range(0, self.floor+1)), default=self.top_floor+1)
                down = max(self.down_pushed_floors(self.downward_floors), default=-1)
                if down >= 0:
                    self.floor = down
                elif up <= self.top_floor:
                    self.floor = up
                    self.direction = "up"
                else:
                    self.direction = "up"
                    return self.move()
        else:
            self.floor = 0
        return self.floor != current_floor

    def theLift(self):
        floors = [self.floor]
        while not self.is_empty() or self.lift:
            self.get_off()
            self.get_on()
            if self.move():
                # print("move to", self.floor, self.queues, self.lift, self.direction)
                floors.append(self.floor)
        return floors

tests = [
    [ ( (),   (),    (5,5,5), (),   (),    (),    () ),     [0, 2, 5, 0]          ],
    [ ( (),   (),    (1,1),   (),   (),    (),    () ),     [0, 2, 1, 0]          ],
    [ ( (),   (3,),  (4,),    (),   (5,),  (),    () ),     [0, 1, 2, 3, 4, 5, 0] ],
    [ ( (),   (0,),  (),      (),   (2,),  (3,),  () ),     [0, 5, 4, 3, 2, 1, 0] ],
]

for queues, answer in tests:
    lift = Dinglemouse(queues, 5)
    result = lift.theLift()
    print(result)
    print(answer)
    print(result == answer)
    if result != answer:
        break
        
___________________________________________________
from enum import Enum
from functools import total_ordering


class Dinglemouse(object):

    def __init__(self, queues, capacity):
        print(queues, capacity)
        self.lift = Lift(capacity)
        self.floors = [Floor(i, q) for i, q in enumerate(queues)]

    def theLift(self):
        if not self.floors[0].fill_lift(self.lift):
            self.lift.stopped_at(0)

        # return
        self.print_passengers()

        next_destination = self.get_furthest_destination(self.lift)
        i = 0
        while next_destination is not None:
            self.move_lift_to_floor(next_destination)
            if self.lift.has_passengers():
                next_destination = self.get_furthest_passenger_destination(self.lift)
                continue

            furthest_destination = self.get_furthest_destination(self.lift)
            if next_destination == furthest_destination:
                next_destination = self.get_furthest_floor_destination(self.lift, self.floors[next_destination])
            else:
                next_destination = furthest_destination

            i += 1
            if i > 20:
                print("endless")
                break

        self.move_lift_to_floor(0)
        self.lift.stopped_at(0)

        return self.lift.history

    def move_lift_to_floor(self, floornumber):
        direction = self.lift.set_destination(floornumber)

        step = 1 if direction == Direction.UP else -1
        for i in range(self.lift.current_floor, floornumber + step, step):
            if self.floors[i].fill_lift(self.lift):
                self.print_passengers()

    def get_highest_floor_passengers(self):
        f = max(([f for f in self.floors if f.has_passengers()]), default=None)
        return f.floornumber if f else None

    def get_lowest_floor_passengers(self):
        f = min(([f for f in self.floors if f.has_passengers()]), default=None)
        return f.floornumber if f else None

    def get_furthest_destination(self, lift):
        possible_floornumbers = [self.get_highest_floor_passengers(),
                                 self.get_lowest_floor_passengers(),
                                 self.lift.get_highest_floornumber_passengers(),
                                 self.lift.get_lowest_floornumber_passengers()]
        possible_floornumbers[:] = [f for f in possible_floornumbers if f is not None]

        if not possible_floornumbers:
            return None

        distances = [abs(f - lift.current_floor) for f in possible_floornumbers]
        index_max_distance = distances.index(max(distances))
        return possible_floornumbers[index_max_distance]

    def get_furthest_passenger_destination(self, lift):
        if self.lift.direction == Direction.UP:
            return self.lift.get_highest_floornumber_passengers()
        else:
            return self.lift.get_lowest_floornumber_passengers()

    def get_furthest_floor_destination(self, lift, floor):
        same_direction_passengers = [p for p in floor.passengers if p.direction == lift.direction]
        if same_direction_passengers:
            p = max(same_direction_passengers) if lift.direction == Direction.UP else min(same_direction_passengers)
            return p.destination

        diff_direction_passengers = [p for p in floor.passengers if p.direction != lift.direction]
        if diff_direction_passengers:
            p = min(diff_direction_passengers) if lift.direction == Direction.UP else max(diff_direction_passengers)
            return p.destination

        return None

    def print_passengers(self):
        for f in self.floors:
            print(f.floornumber, len(f.passengers))
            if len(f.passengers) == 1:
                print(f.passengers[0].destination)
        print(self.lift)
        print("")


@total_ordering
class Floor(object):

    def __init__(self, floornumber, queue):
        self.floornumber = floornumber
        self.passengers = []
        for d in queue:
            direction = Direction.UP if d > floornumber else Direction.DOWN
            self.passengers.append(Passenger(d, direction))

    def fill_lift(self, lift):
        lift.set_current_floor(self.floornumber)
        stop_needed = lift.passenger_exit(self.floornumber)

        old_amount = len(self.passengers)
        self.passengers[:] = [p for p in self.passengers if not p.can_enter(lift)]
        stop_needed |= old_amount != len(self.passengers)

        stop_needed |= next((True for p in self.passengers if p.wants_to_enter(lift)), False)

        if stop_needed:
            lift.stopped_at(self.floornumber)
        return stop_needed

    def has_passengers(self):
        return len(self.passengers) > 0

    def __eq__(self, other):
        return self.floornumber == other.floornumber

    def __lt__(self, other):
        return self.floornumber < other.floornumber


class Lift(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []
        self._direction = Direction.UP
        self.history = [0]
        self.current_floor = 0
        self.destination = 0

    def __str__(self):
        return f"Lift @{self.current_floor} -> {self.destination} {self._direction}. P: {len(self.passengers)} {[p.destination for p in self.passengers]}"

    def add_passenger(self, passenger):
        if len(self.passengers) == self.capacity:
            return False
        self.passengers.append(passenger)
        return True

    def passenger_exit(self, floornumber):
        old_amount = len(self.passengers)
        self.passengers[:] = [p for p in self.passengers if not p.is_at_destination(floornumber)]
        return old_amount != len(self.passengers)

    def stopped_at(self, floornumber):
        if self.history[-1] != floornumber:
            self.history.append(floornumber)

    def has_passengers(self):
        return len(self.passengers) > 0

    def set_destination(self, floornumber):
        self._direction = Direction.UP if self.current_floor == 0 or self.current_floor < floornumber else Direction.DOWN
        self.destination = floornumber
        return self._direction

    def set_current_floor(self, floornumber):
        self.current_floor = floornumber

    def get_highest_floornumber_passengers(self):
        p = max(self.passengers, default=None)
        return p.destination if p else None

    def get_lowest_floornumber_passengers(self):
        p = min(self.passengers, default=None)
        return p.destination if p else None

    @property
    def direction(self):
        return self._direction


@total_ordering
class Passenger(object):

    def __init__(self, destination, direction):
        self.destination = destination
        self.direction = direction

    def can_enter(self, lift):
        return self.wants_to_enter(lift) and lift.add_passenger(self)

    def wants_to_enter(self, lift):
        return self.direction == lift.direction

    def is_at_destination(self, floornumber):
        return self.destination == floornumber

    def __eq__(self, other):
        return self.destination == other.destination

    def __lt__(self, other):
        return self.destination < other.destination


class Direction(Enum):
    UP = 1
    DOWN = 2

___________________________________________________
class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = [list(queue) for queue in queues]
        self.nb_stairs = len(queues)
        self.capacity = capacity
        print(capacity)
        self.stair = 0
        self.cab = []
        self.dir = "up"
        self.temp_up = [True if True in [True if p > index else False for p in stair] else False for index, stair in
                        enumerate(self.queues)]
        self.temp_down = [True if True in [True if p < index else False for p in stair] else False for index, stair in
                          enumerate(self.queues)]

    def theLift(self):
        result = []
        print(self.temp_up)
        print(self.temp_down)
        while (self.queues != [[]] * self.nb_stairs or self.cab!=[]):
            result.append(self.stair)
            print("\n")
            print('actual stair', self.stair, '')
            print('queue', self.queues)

            print('cabine avant descente des gens', self.cab)
            for p in list(self.cab):
                if p == self.stair:
                    self.cab.remove(p)
            print('cabine après descente des gens', self.cab)

            self.__next_dir()


            if self.dir == "up":
                for p in list(self.queues[self.stair]):
                    if p > self.stair and len(self.cab) < self.capacity:
                        self.cab.append(p)
                        self.queues[self.stair].remove(p)

            if self.dir == "down":
                for p in list(self.queues[self.stair]):
                    if p < self.stair and len(self.cab) < self.capacity:
                        self.cab.append(p)
                        self.queues[self.stair].remove(p)
            print("cabine après monté",self.cab)

            self.temp_up = [True if True in [True if p > index else False for p in stair] else False for
                            index, stair in enumerate(self.queues)]
            self.temp_down = [True if True in [True if p < index else False for p in stair] else False for
                              index, stair in enumerate(self.queues)]
            self.__next_step()

        if len(result)>0 and result[-1]!=0 :
            result.append(0)
        if len(result)==0:
            return [0]
                
        return result

    def __next_dir(self):
        if self.dir == "up":
            if self.cab == []:
                if not True in self.temp_up[self.stair:] and not True in self.temp_down[self.stair+1:]:
                    self.dir = "down"
        if self.dir == "down":
            if self.cab == []:
                if not True in self.temp_down[:self.stair + 1] and not True in self.temp_up[:self.stair]:
                    self.dir = "up"

    def __next_step(self):
        if self.dir == "up":
            if self.cab == []:
                if True in self.temp_up[self.stair:]:
                    self.stair = self.temp_up.index(True, self.stair)
                elif True in self.temp_down[::-1]:
                    self.stair = self.nb_stairs - self.temp_down[::-1].index(True) - 1
                else:
                    self.stair = 0

            else:
                if True in self.temp_up[self.stair+1:] :
                    self.stair = min(min(self.cab), self.temp_up.index(True, self.stair+1))
                else:
                    self.stair = min(self.cab)

        if self.dir == "down":
            if self.cab == []:
                if True in self.temp_down[:self.stair + 1]:
                    self.stair = self.nb_stairs - 1 - self.temp_down[::-1].index(True)
                else:
                    self.stair = self.temp_up.index(True)

            else:
                if True in self.temp_down[:self.stair] :
                    self.stair = max(max(self.cab),self.stair-self.temp_down[:self.stair][::-1].index(True)-1)
                else:
                    self.stair = max(self.cab)
                    
___________________________________________________
class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = [list(tup) for tup in queues]
        self.capacity = capacity
        
    def theLift(self):
        #print(self.queues, self.capacity)
        floor = 0                   # Current floor
        people = 0                  # Current number of people inside
        speed = 1                   # Equal 1 if direction is up, -1 if down
        in_tasks = [fl for fl in range(len(self.queues)) if self.queues[fl]]
                                    # Floors, where anyone wants to get in
        out_tasks = []              # Floors, where anyone wants to get out
        result = [0]                # Stops
        moving = []                 # People moving in/out the lift on current floor
        
        while in_tasks or out_tasks:
            
            # exit condition
            if floor in out_tasks:
                result.append(floor)
                for man in out_tasks:
                    if man == floor:
                        moving.append(man)
                        people -= 1
                for man in moving:
                    out_tasks.remove(man)
                moving = []
                
            # TODO: add entry condition and condition for stop
            if floor in in_tasks:
                
                if result[-1] != floor:
                    if out_tasks:
                        if (speed == 1 and max(self.queues[floor]) > floor) or (speed == -1 and min(self.queues[floor]) < floor):
                            result.append(floor)     
                    if not out_tasks:        
                        if (
                            (speed == 1 and (max(self.queues[floor]) >= floor or max(in_tasks) == floor)) 
                            or (speed == -1 and (min(self.queues[floor]) <= floor or min(in_tasks) == floor))
                            ):
                            result.append(floor)
                        
                           
                for man in self.queues[floor]:
                    if people < self.capacity:
                        if out_tasks:
                            if (
                                ((speed == 1 and man > floor) or (speed == -1 and man < floor)) 
                                or ((man-floor > 0 and out_tasks[-1]-floor > 0) or man-floor < 0 and out_tasks[-1]-floor < 0)
                                ):
                                moving.append(man)
                                people += 1
                                out_tasks.append(man)
                        if not out_tasks:        
                            if (speed == 1 and (man > floor or floor == max(in_tasks)) or (speed == -1 and (man < floor or floor == min(in_tasks)))):
                                moving.append(man)
                                people += 1
                                out_tasks.append(man)
                                
                for man in moving:
                    self.queues[floor].remove(man)
                moving = []
                if not self.queues[floor]:
                    in_tasks.remove(floor)
                
            # print(f'f: {floor}, p: {people}, s: {speed}, in: {in_tasks}, out: {out_tasks}, r: {result}')
            
            # changing direction and move on
            if in_tasks or out_tasks:
                if out_tasks:
                    if (speed == 1 and max(out_tasks) < floor) or (speed == -1 and min(out_tasks) > floor):
                        speed *= -1
                if not out_tasks:
                    if (speed == 1 and max(in_tasks) < floor) or (speed == -1 and min(in_tasks) > floor):                          
                        speed *= -1
                # move
                floor += speed
            
        if result[-1] != 0:
            result.append(0)
        return result
      
___________________________________________________
from typing import Tuple, List


class Lift(object):
    queues: List[List[int]]
    capacity: int
    dir: int
    floor: int
    content: List[int]
    isFinished: int
    stopLog: List[int]

    def __init__(self, queues, capacity):
        self.queues = list([list(f) for f in queues])
        self.capacity = capacity
        self.dir = 1
        self.floor = -1
        self.content = []
        self.isWorking = True
        self.stopLog = [0]

    def findNextReq(self):
        floorsNum = len(self.queues)
        i = self.floor + self.dir
        while (0 <= i) and (i < floorsNum):
            isNext = any([self.isPassApproved(p - i) for p in self.queues[i]])
            if isNext:
                return i
            i += self.dir
        return None

    def nextStop(self):
        nextS = []

        if self.content:
            nextS.append(min(self.content) if self.dir == 1 else max(self.content))

        nextReq = self.findNextReq()
        if nextReq is not None:
            nextS.append(nextReq)

        if nextS:
            self.floor = min(nextS) if self.dir == 1 else max(nextS)
            return

        self.floor = len(self.queues) if self.dir == 1 else -1
        self.dir *= -1
        nextReq = self.findNextReq()
        if nextReq is not None:
            self.floor = nextReq
            return

        self.floor = len(self.queues) if self.dir == 1 else -1
        self.dir *= -1
        nextReq = self.findNextReq()
        if nextReq is not None:
            self.floor = nextReq
            return

        self.floor = 0
        self.isWorking = False

    def unloadLoad(self):
        newContent = []
        for p in self.content:
            if p == self.floor:
                self.queues[self.floor].append(p)
            else:
                newContent.append(p)
        self.content = newContent

        freeSpaces = self.capacity - len(self.content)
        if freeSpaces <= 0:
            return

        newQueue = []
        for p in self.queues[self.floor]:
            if (freeSpaces > 0) and (self.isPassApproved(p - self.floor)):
                self.content.append(p)
                freeSpaces -= 1
            else:
                newQueue.append(p)
        self.queues[self.floor] = newQueue

        self.content.sort()

    def isPassApproved(self, floorDelta) -> bool:
        res = (floorDelta * self.dir) > 0
        return res

    def run(self):
        while True:
            self.nextStop()
            if self.stopLog[-1] != self.floor:
                self.stopLog.append(self.floor)
            if not self.isWorking:
                break
            self.unloadLoad()


class Dinglemouse(object):
    queues: Tuple[Tuple[int]]
    capacity: int

    def __init__(self, queues, capacity):
        self.queues = queues
        self.capacity = capacity

    def theLift(self):
        lift = Lift(self.queues, self.capacity)
        lift.run()

        return lift.stopLog

___________________________________________________
class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.level = 0
        self.max_level = len(queues)
        self.queues = list(list(q) for q in queues)
        self.lift = []
        self.dir = 1
        self.capacity = capacity

    def theLift(self):
        stops = [0]
        while any(len(q) > 0 for q in self.queues):
            while (self.level < self.max_level and self.dir > 0) or (self.level >= 0 and self.dir < 0):
                if len(self.lift) > 0 and any(x == self.level for x in self.lift):
                    if stops[-1] != self.level:
                        stops.append(self.level)
                        self.lift = [x for x in self.lift if x != self.level]
                if len(self.queues[self.level]) > 0 and any((x - self.level) * self.dir > 0 for x in self.queues[self.level]):
                    if stops[-1] != self.level:
                        stops.append(self.level)
                    if len(self.lift) < self.capacity:
                        rem = []
                        for x in self.queues[self.level]:
                            if (x - self.level) * self.dir > 0 and len(self.lift) < self.capacity:
                                self.lift.append(x)
                            else:
                                rem.append(x)
                        self.queues[self.level] = rem[:]
                self.level += self.dir
            self.dir *= -1
            self.level += self.dir 
        if stops[-1] != 0:
            stops.append(0)
        return stops
      
___________________________________________________
class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.q = self.convertTupleToListBecauseItsJustFrickingEasierMan(queues)
        self.floors = len(queues)
        self.floor = 0
        self.going_up = True
        self.capacity = capacity
        self.load = []
        self.visited = []
        
    def theLift(self):
        print("Max lift capacity:", self.capacity)
        operating = True
        while operating:
        
            print(self.q)
            print("Current Floor:", self.floor)
            self.visited.append(self.floor)

            # passengers get off
            for i in reversed(range(len(self.load))):
                if self.load[i] == self.floor:
                    self.load.pop(i)
                    print("passenger getting off")
                    
            # change direction
            if self.floor == self.floors-1: self.going_up = False
            elif self.floor == 0: self.going_up = True
            
            if self.going_up and not self.tasksAbove():
                self.going_up = False
                print("Changing direction to down")
            elif not self.going_up and not self.tasksBelow():
                self.going_up = True
                print("Chaning direction to up")

            # take on new passengers
            new_passengers = []
            for i, passenger in enumerate(self.q[self.floor]):
                if len(self.load) + len(new_passengers) == self.capacity: break
                if (passenger-self.floor)>0 and self.going_up or (passenger-self.floor)<0 and not self.going_up:
                    new_passengers.append(i)
                    print("New passenger, going to:", passenger)
            for i in reversed(new_passengers):
                self.load.append( self.q[self.floor].pop(i) )
            print("passengers:", self.load)
            
            # finish condition
            waiting = 0
            for floor in self.q:
                waiting += len(floor)
            if len(self.load) == 0 and waiting == 0:
                operating = False
                if self.floor != 0:
                    self.floor = 0
                    self.visited.append(0)
            else:
                self.floor = self.getNextFloor()

        print("VISITED:", self.visited)
        return self.visited
    
    def getNextFloor(self):
        if self.going_up:
            next_floor = self.floors-1
            #print("seeing where people want to go ----")
            for i in range(self.floor+1, self.floors): # check for passengers ahead (going in same direction)
                for person in self.q[i]:
                    if (person-i) > 0:
                        next_floor = i
                        break
                if next_floor != self.floors-1: break
            else: # if found no passengers above who want to go up
                if len(self.load) == 0:
                    for i in reversed(range(self.floor+1, self.floors)):
                        if len(self.q[i]) > 0: # get highest person who wants to go down
                            print("found highest person who wants to go down:", i)
                            next_floor = i
                            break
            for p in self.load: # check where next load passenger wants to stop
                if p < next_floor:
                    next_floor = p
        
        else: # going down
            next_floor = 0
            for i in reversed(range(0, self.floor)):
                for p in self.q[i]:
                    if (p-i) < 0:
                        next_floor = i
                        break
                if next_floor != 0: break
            else: # nobody below going down
                if len(self.load) == 0: # nobody on board
                    for i in range(0, self.floor):
                        if len(self.q[i]) > 0:
                            next_floor = i
                            break
            for p in self.load:
                if p > next_floor:
                    next_floor = p
        return next_floor
        
    def tasksAbove(self):
        for p in self.load: # for person in load
            if p > self.floor:
                return True
        for p in self.q[self.floor]: # for person on current floor (below doors open)
            if p > self.floor:
                return True
        for i in range(self.floor+1, self.floors): # check for people above
            if len(self.q[i]) > 0:
                return True
        return False
    
    def tasksBelow(self):
        for p in self.load:
            if p < self.floor:
                return True
        for p in self.q[self.floor]:
            if p < self.floor:
                return True
        for i in range(0, self.floor):
            if len(self.q[i]) > 0:
                return True
        return False
    
    def convertTupleToListBecauseItsJustFrickingEasierMan(self, q):
        building = []
        for floor in q:
            passengers = []
            for passenger in floor:
                passengers.append(passenger)
            building.append(passengers)
        return building
    
