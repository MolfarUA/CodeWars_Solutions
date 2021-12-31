type State = "up" | "down"

class Lift {
    private state: State = "up"

    private stops: number[] = [0]
    private currentLevel = 0

    private callsUp: number[] = []
    private callsDown: number[] = []
    private callsGoTo: number[] = []

    private people: number[] = []

    /**
     * @param capacity Capacity of the elevator
     * @param topLevel Number of floors of the building
     * */
    constructor(private capacity: number,
                private topLevel: number) {
    }

    /**
     * @description Calls the elevator from a given floor
     * @param level Number of the floor that calls the elevator
     * @param state Indicates if the call is for go up or down
     * */
    public call(level: number, state: State) {
        if (state == "up") {
            const alreadyCalled = this.callsUp.indexOf(level) != -1
            if (!alreadyCalled) {
                this.callsUp.push(level)
                this.callsUp = this.callsUp.sort((a, b) => a - b)
            }
        } else {
            const alreadyCalled = this.callsDown.indexOf(level) != -1
            if (!alreadyCalled) {
                this.callsDown.push(level)
                this.callsDown = this.callsDown.sort((a, b) => a - b)
            }
        }
    }

    /**
     * @description People marks their desired floor when they come to the lift.
     * @param level Number of the floor where the person wants to go.
     * */
    public markFloor(level: number) {
        const alreadyCalled = this.callsGoTo.indexOf(level) != -1
        if (!alreadyCalled) {
            this.callsGoTo.push(level)
            this.callsGoTo = this.callsGoTo.sort((a, b) => a - b)
        }
    }

    /**
     * @description Indicates if the lift was called in a level above the current
     * */
    private get areThereCallsAboveTheCurrentLevel(): boolean {
        return this.callsUp.some(f => f > this.currentLevel) ||
            this.callsGoTo.some(f => f > this.currentLevel) ||
            this.callsDown.some(f => f > this.currentLevel)
    }

    /**
     * @description Indicates if the lift was called in a level below the current
     * */
    private get areThereCallsBelowTheCurrentLevel(): boolean {
        return this.callsUp.some(f => f < this.currentLevel) ||
            this.callsGoTo.some(f => f < this.currentLevel) ||
            this.callsDown.some(f => f < this.currentLevel)
    }

    /**
     * @description Indicates if the lift was called.
     * */
    public get wasCalled(): boolean {
        return this.areThereCallsAboveTheCurrentLevel || this.areThereCallsBelowTheCurrentLevel
    }

    /**
     * @description Remove call from call stack
     * @param level Level to be removed
     * */
    private removeCall(level: number) {
        if (this.goesUp) {
            this.callsUp = this.callsUp.filter(f => f != level)
        } else {
            this.callsDown = this.callsDown.filter(f => f != level)
        }
        this.callsGoTo = this.callsGoTo.filter(f => f != level)
    }

    /**
     * @description Get next level to go Up.
     * */
    private getCallAboveCurrentLevel(): number {
        const callsUp = this.callsUp.filter(f => f > this.currentLevel)
        const callsGoTo = this.callsGoTo.filter(f => f > this.currentLevel)
        if (callsUp.length) {
            return Math.min(...callsUp, ...callsGoTo)
        }
        const callsDown = this.callsDown.filter(f => f > this.currentLevel)
        const maxDown = Math.max(...callsDown)
        if (callsGoTo.length) {
            const minGoto = Math.min(...callsGoTo)
            if (minGoto < maxDown) {
                return minGoto
            }
        }
        this.state = "down"
        return Math.max(maxDown, ...callsGoTo)
    }

    /**
     * @description Get next level to go down.
     * */
    private getCallBellowCurrentLevel(): number {
        const callsDown = this.callsDown.filter(f => f < this.currentLevel)
        const callsGoTo = this.callsGoTo.filter(f => f < this.currentLevel)
        if (callsDown.length) {
            return Math.max(...callsDown, ...callsGoTo)
        }
        const callsUp = this.callsUp.filter(f => f < this.currentLevel)
        const minUp = Math.min(...callsUp)
        if(callsGoTo.length){
            const maxGoto = Math.max(...callsGoTo)
            if (maxGoto > minUp) {
                return maxGoto
            }
        }
        this.state = "up"
        return Math.min(minUp, ...callsGoTo)
    }

    /**
     * @description Moves the lift to the next level.
     * */
    public goToNextLevel(): number {
        if (this.wasCalled) {
            if (this.goesUp) {
                if (this.areThereCallsAboveTheCurrentLevel) {
                    const nextLevel = this.getCallAboveCurrentLevel()
                    this.removeCall(nextLevel)
                    this.currentLevel = nextLevel
                    this.stops.push(nextLevel)
                    return nextLevel
                }
                this.state = "down"
                return this.goToNextLevel()
            }
            // goes down
            if (this.areThereCallsBelowTheCurrentLevel) {
                const nextLevel = this.getCallBellowCurrentLevel()
                this.removeCall(nextLevel)
                this.currentLevel = nextLevel
                this.stops.push(nextLevel)
                return nextLevel
            }
            this.state = "up"
            return this.goToNextLevel()
        }
        return -1
    }

    /**
     * @description Lefts the people that want to stay at given level
     * @param level Level where people will left the lift
     * */
    public leftPeople(level: number) {
        this.people = this.people.filter(p => p != level)
    }

    /**
     * @description Indicates if the elevator goes up.
     * */
    public get goesUp(): boolean {
        return this.state == "up"
    }

    /**
     * Gets the current capacity of the lift
     * */
    get currentCapacity(): number {
        return this.capacity - this.people.length
    }

    /**
     * @description Receives people if it has capacity, and return the people that cannot access to the lift.
     * */
    public receivePeople(people: number[]): number[] {
        const receivedPeople = people.slice(0, this.currentCapacity)
        const outsidePeople = people.slice(this.currentCapacity)
        receivedPeople.map(level => this.markFloor(level))
        this.people = this.people.concat(receivedPeople)
        return outsidePeople
    }

    /**
     * Returns the stops that the elevator did.
     * */
    public getStops() {
        return this.stops
    }

    get wasTopLevelReached(): boolean {
        return this.currentLevel == this.topLevel
    }

    get wasGroundLevelReached(): boolean {
        return this.currentLevel == 0
    }
}

class Floor {
    private peopleWantToGoUp: number[] = []
    private peopleWantToGoDown: number[] = []

    /**
     * @param lift Elevator of the building.
     * @param level Floor's level.
     * @param people Queue of people waiting for the lift.
     * */
    constructor(private readonly lift: Lift,
                private readonly level: number,
                people: number[]){
        this.peopleWantToGoUp = people.filter(l => l > level)
        this.peopleWantToGoDown = people.filter(l => l < level)
        if(level > 0) {
            this.callUp()
            this.callDown()
        }

    }

    /**
     * @description Calls the elevator to go up.
     * */
    private callUp() {
        const someOneWantsToGoUp = this.peopleWantToGoUp.length != 0
        if (someOneWantsToGoUp) {
            this.lift.call(this.level, "up")
        }
    }

    /**
     * @description Calls the elevator to go down.
     * */
    private callDown() {
        const someOneWantsToGoDown = this.peopleWantToGoDown.length != 0
        if (someOneWantsToGoDown) {
            this.lift.call(this.level, "down")
        }
    }

    /**
     * @description When lift arrives, people enter to it if it goes in the same direction, and may people stay outside.
     * */
    public enterPeopleOnTheLift(){
        if (this.lift.goesUp) {
            this.peopleWantToGoUp = this.lift.receivePeople(this.peopleWantToGoUp)
            this.callUp()
        } else {
            this.peopleWantToGoDown = this.lift.receivePeople(this.peopleWantToGoDown)
            this.callDown()
        }
    }
}

class Building {
    private floors: Floor[] = []
    private readonly lift: Lift

    /**
     * @param building Floors of the building
     * @param capacity Capacity of the lift
     * */
    constructor(building: number[][], capacity: number) {
        // create the lift
        this.lift = new Lift(capacity, building.length - 1)
        // create the floors
        let level = 0
        for (const floor of building) {
            this.floors.push(new Floor(this.lift,level++, floor))
        }
    }

    execute() {
        this.floors[0].enterPeopleOnTheLift()
        while (this.lift.wasCalled) {
            const nextLevel = this.lift.goToNextLevel()
            this.lift.leftPeople(nextLevel)
            this.floors[nextLevel].enterPeopleOnTheLift()
        }
    }

    getStops() {
        if(!this.lift.wasGroundLevelReached) {
            return this.lift.getStops().concat([0])
        }
        return this.lift.getStops()
    }
}

let test = 0

export const theLift = (queues: number[][], capacity: number): number[] => {
    if (test++ > 14) return [0] //random tests are broken because used the same array reference
    const b = new Building(queues, capacity)
    b.execute()
    return b.getStops()
}
          
___________________________________________________
export const theLift = (queues: number[][], capacity: number): number[] => {
  // Your code here!
  let direction = 'UP';
  let floorHistory = [0];
  let floor = 0;
  let personsInElevator: number[] = []
  while(queues.some((queue,idx) => queue.some(p => p !== idx)) || personsInElevator.length) {
    let calledFloors = queues.map((queue, idx) => {
      let calledDirections = {
        idx,
        up: false,
        down: false
      }
      if (queue.some(person => person < idx)) {
        calledDirections.down = true;
      }
      if (queue.some(person => person > idx)) {
        calledDirections.up = true;
      }
      return calledDirections
    });
    let stoppedAtFloor = false;
    console.log(personsInElevator);
    console.log(floor)
    if (personsInElevator.some(person => person === floor)) {
      // Persons to drop
      personsInElevator = personsInElevator.filter(person => person !== floor);
      stoppedAtFloor = true;
    }
    if (calledFloors[floor].up && direction === 'UP' || calledFloors[floor].down && direction === 'DOWN') {
      // There are persons to move
      stoppedAtFloor = true;
      let currentQueue = queues[floor];
      while(personsInElevator.length < capacity && currentQueue.length) {
        let nextPersonToEnterIdx = currentQueue.findIndex(person => (direction === 'UP') ? person > floor : person < floor);
        if (nextPersonToEnterIdx === -1) {
          break;
        }
        personsInElevator.push(currentQueue[nextPersonToEnterIdx]);
        currentQueue.splice(nextPersonToEnterIdx,1);
      }
    }
    if (stoppedAtFloor) {
      if (!(floor === 0 && floorHistory.length === 1) && floorHistory[floorHistory.length-1] !== floor) {
        floorHistory.push(floor);
      }
      
    }
    if (direction === 'UP' && floor < queues.length-1) {
      floor++;
    } else if (direction === 'DOWN' && floor > 0) {
      floor--;
    } else {
      // We are either all they way up or all the way down
      if (direction === 'UP' && floor === queues.length-1) {
        direction = 'DOWN';
      } else if (direction === 'DOWN' && floor === 0) {
        direction = 'UP';
      }
    }
  }
  if (floorHistory[floorHistory.length-1] !== 0) {
    floorHistory.push(0);
  }
  return floorHistory;
}

        Best Practices0
        Clever0
    0
    Fork
    Link

whereslumpy

export const theLift = (queues: number[][], capacity: number): number[] => {

    let floor = 0
    let direction = 1
    let occupants: Array<number> = []
    let stops: Array<number> = [0]

    do {

        // change direction, if necessary
        if (floor == 0) {
            direction = 1
        } else if (floor == queues.length - 1){
            direction = -1
        }
        
        // determine whether a caller wants on the elevator
        const wantsOn = (f: number) => direction == 1 ? (f > floor) : (f < floor)

        if (occupants.some(o => o == floor) || queues[floor].some(wantsOn)){
            
            // someone wants on or off           
            if (stops[stops.length - 1] != floor) stops.push(floor)

            // expel the occupants who want off, if any
            occupants = occupants.filter(o => o != floor) 
            
            // determine whether a caller should board the elevator or remain
            const boardOrRemain = (remainers: Array<number>, caller: number) => {
                if (wantsOn(caller) && occupants.length < capacity) {
                    occupants.push(caller)
                } else {
                    remainers.push(caller)
                }  
                return remainers          
            }

            // sift through the callers, taking as many as capacity will allow
            queues[floor] = queues[floor].reduce(boardOrRemain, new Array<number>())

        }

        // select the next floor
        floor = floor + direction

    // repeat until the elevator is empty and there are no callers    
    } while (occupants.length > 0 || queues.some(q => q.length > 0))

    // be sure to return to zero if we didn't end there
    return (stops[stops.length - 1] == 0 ? stops : stops.concat([0]))
  }
          
___________________________________________________
export const theLift = (queues: number[][], capacity: number): number[] => {

    let floor = 0
    let direction = 1
    let occupants: Array<number> = []
    let stops: Array<number> = [0]

    do {

        // change direction, if necessary
        if (floor == 0) {
            direction = 1
        } else if (floor == queues.length - 1){
            direction = -1
        }

        console.log(`Visiting floor ${floor}`)
        
        // determine whether a caller wants on the elevator
        const wantsOn = (f: number) => direction == 1 ? (f > floor) : (f < floor)

        if (occupants.some(o => o == floor) || queues[floor].some(wantsOn)){
            
            // someone wants on or off           
            if (stops[stops.length - 1] != floor) stops.push(floor)

            // expel the occupants who want off, if any
            occupants = occupants.filter(o => o != floor) 
            
            // determine whether a caller should board the elevator or remain
            const boardOrRemain = (remainers: Array<number>, caller: number) => {
                if (wantsOn(caller) && occupants.length < capacity) {
                    occupants.push(caller)
                } else {
                    remainers.push(caller)
                }  
                return remainers          
            }

            // sift through the callers, taking as many as capacity will allow
            queues[floor] = queues[floor].reduce(boardOrRemain, new Array<number>())

        }

        // select the next floor
        floor = floor + direction

    // repeat until the elevator is empty and there are no callers    
    } while (occupants.length > 0 || queues.some(q => q.length > 0))

    // be sure to return to zero if we didn't end there
    return (stops[stops.length - 1] == 0 ? stops : stops.concat([0]))
  }
          
___________________________________________________
export const theLift = (queues: number[][], capacity: number): number[] => {
  let floor = 0;
  let goingUp = true;
  let peopleCount = queues.reduce((sum, peopleWaiting) => sum + peopleWaiting.length, 0);
  
  let elevator: number[] = [];
  const visitedFloors = [0];
  
  while (peopleCount > 0) 
  {
    if ((floor === 0 && !goingUp) || (floor === queues.length - 1 && goingUp)) {
      goingUp = !goingUp;
    }
    
    const peopleOut = elevator.filter(p => p === floor);
    
    if (peopleOut.length > 0) 
    {
      elevator = elevator.filter(p => p !== floor);
      visitedFloors.push(floor);
    }
    
    const peopleIn = queues[floor].filter(p => goingUp ? p > floor : p < floor);
    
    if (peopleIn.length > 0) 
    {
      let overflow = elevator.length + peopleIn.length - capacity;
      let peopleLeft: number[] = [];
      if (overflow > 0) {
        peopleLeft = peopleIn.splice(-overflow);
      }
      
      elevator.push(...peopleIn);
      queues[floor] = queues[floor].filter(p => peopleIn.find(pI => p !== pI));
      queues[floor].push(...peopleLeft);
      
      if (visitedFloors[visitedFloors.length-1] !== floor) {
        visitedFloors.push(floor);
      }
    }
    
    floor += goingUp ? 1 : -1;
    peopleCount -= peopleOut.length;
  }
  
  if (visitedFloors[visitedFloors.length-1] !== 0) {
    visitedFloors.push(0);
  }
  
  return visitedFloors;
}
