var theLift = function(queues, capacity) {
  var dir = 1;
  var floor = -1;
  var basket = [];
  var history = [];
  var addHistory = floor => history.slice(-1)[0] != floor && history.push(floor);

  while (queues.some(q => q.length) || basket.length) {
    floor += dir;
    q = queues[floor];

    if (floor == queues.length - 1 || (floor == 0 && dir == -1)) {
      dir *= -1; //switch direction
    }

    var goingThisWay = p => dir * p >= dir * floor;
    if (q.some(goingThisWay) || basket.includes(floor)) {
      addHistory(floor);
    }

    basket = basket.filter(p => p != floor);

    for (var i = 0; i < q.length; i++) {
      if (basket.length == capacity) {
        break;
      }

      if (goingThisWay(q[i])) {
        addHistory(floor);
        basket.push(q.splice(i, 1)[0]);
        i--;
      }
    }
  }

  addHistory(0);
  history[0] != 0 && history.unshift(0);

  return history;
}

___________________________________________________
function theLift(queues, capacity) {
  //Lift starts on floor 0, and goes up until it reaches a floor with someone wanting to go up.
  //Everyone who can fit gets on, carries on up
  //At every floor it passes, if someone is wanting to go in the same direction, it stops and transfers happen
  //This carries on until it gets to the top
  //Then it goes back down doing exactly the same thing
  //Repeat this until everyone is both off the lift and not waiting anymore
  const lift = [];
  const maxFloors = queues.length - 1;
  let goingUp = true;
  let currentFloor = 0;
  let isFinished = false;
  const floorsVisited = [0];
  while (!isFinished) {
    changeDirection();
    checkCurrentFloor();
    moveFloors();
    anyoneRemaining();
  }
  function checkCurrentFloor() {
    //People have got off
    if (lift.includes(currentFloor) || checkWaiting()) {
      if (floorsVisited[floorsVisited.length - 1] !== currentFloor) {
        floorsVisited.push(currentFloor);
      }
      while (lift.includes(currentFloor)) {
        let index = lift.indexOf(currentFloor);
        lift.splice(index, 1);
      }
    }
    //People get on
    for (let i = 0; i < queues[currentFloor].length; i++) {
      let person = queues[currentFloor][i];
      if (person - currentFloor > 0 === goingUp && lift.length < capacity) {
        lift.push(person);
        queues[currentFloor].splice(i, 1);
        i--;
      }
    }
  }
  function moveFloors() {
    //Move +-1 depenigng on going up
    currentFloor = goingUp ? currentFloor + 1 : currentFloor - 1;
  }
  function changeDirection() {
    //If at top or bottom, set goingUp to appropriate
    if (currentFloor === 0) goingUp = true;
    if (currentFloor === maxFloors) goingUp = false;
  }
  function anyoneRemaining() {
    let peopleRemaining = false;
    //Check lift and floors to see if anyone is remaining
    queues.forEach((floor) => {
      if (floor.length > 0) peopleRemaining = true;
    });
    if (lift.length > 0) peopleRemaining = true;
    //If no one remaining, set isFinished to true and add 0 floor to final array
    if (!peopleRemaining) {
      isFinished = true;
      if (floorsVisited[floorsVisited.length - 1] !== 0) {
        floorsVisited.push(0);
      }
    }
  }
  function checkWaiting() {
    if (queues[currentFloor].length === 0) return false;
    let isTrue = false;
    queues[currentFloor].forEach((wait) => {
      if (wait - currentFloor > 0 === goingUp) isTrue = true;
    });
    return isTrue;
  }
  return floorsVisited;
}

___________________________________________________
var theLift = function(queues, capacity) {
    const stops = [0];
    let lift = [];
    let numberOfPeopleInLift = 0;
    let currentFloor = 0;
    let peopleWaiting = 0;
    let goingUp = true;
    let goingDown = false;
    let counterFloorsWaiting;
    let nextStop;
    let k = 0;

    console.log(queues);

    // working - checked
    queues.forEach(floor => {
        if (floor.length > 0) {
            floor.forEach(person => {
                peopleWaiting++
            })
        }
    });

    

    // getting people from ground floor
    for (let i = 0; i < queues[currentFloor].length; i++) {
        if (queues[currentFloor][i] > currentFloor && lift.length < capacity) {
            lift.push(parseInt((queues[currentFloor].splice(queues[currentFloor].indexOf(queues[currentFloor][i]), 1)).toString()));
            i--;
        }
    }

    while(peopleWaiting !== 0) {

        // console.log(peopleWaiting);

        
        // going up behaviour
        if (goingUp) {
            // checking the next stop
            for (let i = currentFloor + 1; i < queues.length; i++) {
                if (queues[i].length > 0) {
                    nextStop = i;
                    queues[i].forEach(person => {
                        if (person > i) {
                            nextStop = i;
                            i = queues.length;
                        }
                    });
                    // if there is no people waiting upstairs, check if somebody wants to get off on higher floor
                } else if (queues[i].length === 0) {
                    lift.forEach(person => {
                        if (person > currentFloor) {
                            nextStop = person;
                        }
                    });
                }
            }
            // checking if somebody wants to get off before next stop
            for (let i = 0; i < lift.length; i++) {
                if (lift[i] > currentFloor) {
                    if (lift[i] < nextStop) {
                        nextStop = lift[i];
                    }
                }
            }

            // going to the next stop
            currentFloor = nextStop;
            stops.push(currentFloor);

            // get offs
            for (let i = 0; i < lift.length; i++) {
                if (lift[i] === currentFloor) {
                    lift.splice(lift.indexOf(lift[i]), 1);
                    i--;
                    peopleWaiting--;
                }
            }

            //  get ons
            for (let i = 0; i < queues[currentFloor].length; i++) {
                if (queues[currentFloor][i] > currentFloor && lift.length < capacity) {
                    lift.push(parseInt((queues[currentFloor].splice(queues[currentFloor].indexOf(queues[currentFloor][i]), 1)).toString()));
                    i--;
                }
            }

            // checking if there are people waiting on the higher floors
            counterFloorsWaiting = 0;
            for (let i = currentFloor + 1; i < queues.length; i++) {
                if (queues[i].length > 0) {
                    counterFloorsWaiting++;
                }
            }
            if (counterFloorsWaiting === 0) {
                goingUp = false;
                goingDown = true;

                // getting first people to run down
                for (let i = 0; i < queues[currentFloor].length; i++) {
                    if (queues[currentFloor][i] < currentFloor && lift.length < capacity) {
                        lift.push(parseInt((queues[currentFloor].splice(queues[currentFloor].indexOf(queues[currentFloor][i]), 1)).toString()));
                        i--;
                    }
                }
            }
            // and if there are people who want to get off on higher floor
            for (let i = 0; i < lift.length; i++) {
                if (lift[i] > currentFloor) {
                    goingUp = true;
                    goingDown = false;
                }
            }
        }


        //  going down behaviour
        if (goingDown) {
            // next step
            for (let i = currentFloor - 1; i >= 0; i--) {
                // console.log(currentFloor);
                // console.log(i);
                // console.log('working');
                if (queues[i].length > 0) {
                    nextStop = i;
                    queues[i].forEach(person => {
                        if (person < i) {
                            nextStop = i;
                            i = -1;
                        }
                    });
                    // if there is no people waiting downstairs, check if somebody wants to get off on lower floor
                } else if (queues[i].length === 0) {
                    // console.log('working2');
                    lift.forEach(person => {
                        if (person < currentFloor) {
                            nextStop = person;
                        }
                    });
                }
            }    
            // checking if somebody wants to get off before next stop
            // console.log('working3');
            for (let i = 0; i < lift.length; i++) {
                if (lift[i] < currentFloor) {
                    if (lift[i] > nextStop) {
                        nextStop = lift[i];
                    }
                }
            }

            // going to the next stop
            currentFloor = nextStop;
            if (stops[stops.length - 1] !== currentFloor) {
                stops.push(currentFloor);
            }

            // get offs
            for (let i = 0; i < lift.length; i++) {
                if (lift[i] === currentFloor) {
                    lift.splice(lift.indexOf(lift[i]), 1);
                    i--;
                    peopleWaiting--;
                }
            }

            //  get ons
            // console.log('working4');
            // console.log(queues[currentFloor].length);
            // console.log(currentFloor);
            // console.log(lift);

            for (let i = 0; i < queues[currentFloor].length; i++) {
                // console.log('working5');
                if (queues[currentFloor][i] < currentFloor && lift.length < capacity) {
                    lift.push(parseInt((queues[currentFloor].splice(queues[currentFloor].indexOf(queues[currentFloor][i]), 1)).toString()));
                    i--;
                }
            }

            // checking if there are people waiting on the lower floors
            counterFloorsWaiting = 0;
            // console.log('working 7');
            for (let i = currentFloor - 1; i >= 0; i--) {
                // console.log('working 8');
                // console.log(i);
                if (queues[i].length > 0) {
                    // console.log('working 9');
                    counterFloorsWaiting++;
                }
                // console.log('working 10');
            }
            if (counterFloorsWaiting === 0) {
                goingUp = true;
                goingDown = false;

                // getting first people to run up
                for (let i = 0; i < queues[currentFloor].length; i++) {
                    if (queues[currentFloor][i] > currentFloor && lift.length < capacity) {
                        lift.push(parseInt((queues[currentFloor].splice(queues[currentFloor].indexOf(queues[currentFloor][i]), 1)).toString()));
                        i--;
                    }
                }
            }

            // and if there are people who want to get off on lower floor
            for (let i = 0; i < lift.length; i++) {
                if (lift[i] < currentFloor) {
                    goingUp = false;
                    goingDown = true;
                }
            }
        }

        // checks

        console.log(currentFloor);
        console.log(lift);
        console.log(queues);


    }

if (stops[stops.length - 1] !== 0) stops.push(0);
return stops;

}
