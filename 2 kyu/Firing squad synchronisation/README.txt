You have a squad of robots in a row. At some time, an order to fire is given to the first of these robots, and your goal is to make sure all of the robots will fire simultaneously.

To do that you will have to manage the communication between them, but they are very limited. The robots are basically cells of a 1D cellular automaton that can have different states, and at each time step they will simultaneously trasnsition to a new state. They have no memory and the only thing they know is their own current state and that of their two (or one) direct neighbours : the next state is a function of those three states.

You need to find a finite set of states and transition rules such that all of the robots switch to the firing state on the same time step. All robots follow the same set of rules, except for the first and the last one which each have their own rules (as they have a unique neighbour). Your solution will have to work for a squad of any size greater than or equal to 2, without changing the number of states or the rules.

You can choose what type of object will represent these states, as well the initial state (the same for all robots) and the state of the first robot after he receives the order to fire. They must be hashable types. The firing state is represented by the string 'fire'.

The variables initial_state and trigger_state should contain the objects of your choice to represent those states.

The three rule functions will be called to update the states of the robot. The arguments previous, target, and following will repectively be the state of the previous robot in the row, the state of the robot for which next state is computed, and the state of the next robot. These functions should return the updated state.

To ensure that you use a finite number of states, you will be limited to 50 states, which should be more than enough.
