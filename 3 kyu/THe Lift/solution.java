import java.util.*;
import java.util.stream.*;

public class Dinglemouse {

    public static int[] theLift(final int[][] queues, final int capacity) {
        List<Integer> lift = new ArrayList<>();
        List<Integer> visitedFloors = new ArrayList<>();
        visitedFloors.add(0, 0);
      
        boolean isMovingUp = true;
        int currentFloor = 0;
        int peopleCount = 0;
        int maxFloor = maxFloor(queues);
        int minFloor = 0;

        int[] nonEmptyFloors = {0};
        for (int[] floor : queues) {
            if (floor.length > 0) {
                nonEmptyFloors[0]++;
            }
        }

        while (nonEmptyFloors[0] > 0 || !lift.isEmpty()) {
            peopleCount = peopleGetOut(lift, visitedFloors, currentFloor, peopleCount);
            peopleCount = peopleComeIn(queues, lift, visitedFloors, currentFloor, capacity, peopleCount,
                    nonEmptyFloors, isMovingUp ? Comparator.naturalOrder() : Comparator.reverseOrder());

            if (isMovingUp && currentFloor == maxFloor) {
                isMovingUp = false;
                minFloor = minFloor(queues);
                continue;
            } else if (!isMovingUp && currentFloor == minFloor) {
                isMovingUp = true;
                maxFloor = maxFloor(queues);
                continue;
            }

            currentFloor = isMovingUp ? currentFloor + 1 : currentFloor - 1;
        }

        if (visitedFloors.get(visitedFloors.size() - 1) != 0) {
            visitedFloors.add(0);
        }

        return visitedFloors.stream().mapToInt(Integer::intValue).toArray();
    }

    private static int peopleComeIn(int[][] queues, List<Integer> lift, List<Integer> visitedFloors, int currentFloor,
                                    int capacity, int peopleCount, int[] nonEmptyFloors,
                                    Comparator<Integer> comparator) {
        if (peopleCount < capacity) {
            int emptyCounter = 0;
            int peoplePrev = peopleCount;
            for (int i = 0, queueLength = queues[currentFloor].length; i < queueLength; i++) {
                if (queues[currentFloor][i] == -1) {
                    emptyCounter++;
                } else if (peopleCount == capacity) {
                    break;
                } else if (comparator.compare(queues[currentFloor][i], currentFloor) > 0) {
                    peopleCount++;
                    lift.add(queues[currentFloor][i]);
                    queues[currentFloor][i] = -1;
                    emptyCounter++;
                }
            }

            if (emptyCounter > 0 && emptyCounter == queues[currentFloor].length) {
                queues[currentFloor] = new int[0];
                nonEmptyFloors[0]--;
            }

            if (peoplePrev < peopleCount && visitedFloors.get(visitedFloors.size() - 1) != currentFloor) {
                visitedFloors.add(currentFloor);
            }
        } else if (peopleCount == capacity && queues[currentFloor].length > 0) {
            boolean buttonWasPressed = false;
            for (int floorWish : queues[currentFloor]) {
                if (floorWish == -1) continue;
                buttonWasPressed |= comparator.compare(floorWish, currentFloor) > 0;
            }

            if (visitedFloors.get(visitedFloors.size() - 1) != currentFloor && buttonWasPressed) {
                visitedFloors.add(currentFloor);
            }
        }

        return peopleCount;
    }

    private static int peopleGetOut(List<Integer> lift, List<Integer> visitedFloors, int currentFloor, int peopleCount) {
        List<Integer> found = new ArrayList<>();
        for (Integer floorWish : lift) {
            if (floorWish == currentFloor) {
                found.add(floorWish);
                peopleCount--;
            }
        }

        if (!found.isEmpty()) {
            if (visitedFloors.get(visitedFloors.size() - 1) != currentFloor) {
                visitedFloors.add(currentFloor);
            }

            lift.removeAll(found);
        }

        return peopleCount;
    }

    private static int maxFloor(int[][] queues) {
        List<Integer> list = IntStream.range(0, queues.length).boxed().collect(Collectors.toList());
        list.addAll(Arrays.stream(queues).flatMapToInt(IntStream::of).boxed().collect(Collectors.toList()));
        return list.stream().max(Comparator.naturalOrder()).orElse(queues.length);
    }

    private static int minFloor(int[][] queues) {
        List<Integer> list = IntStream.range(0, queues.length).boxed().collect(Collectors.toList());
        list.addAll(Arrays.stream(queues).flatMapToInt(IntStream::of).boxed().collect(Collectors.toList()));
        return list.stream().filter(i -> i >= 0).min(Comparator.naturalOrder()).orElse(0);
    }
}

___________________________________________________
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import java.util.*;

public class Dinglemouse {
  
    public static int[] theLift(final int[][] queues, final int capacity) {
        Lift lift = new Lift(capacity);
        LiftService liftService = new LiftService(lift);
        liftService.setWaitingPassengers(queues);
        if (liftService.waitingPassengers.isEmpty()) {
            return new int[]{0};
        }
        while (!liftService.isAllPassengersDeliveredAndLiftStoppedAtBasement()) {
            liftService.handleNextFloor();
        }
        liftService.closeLogs();
        return liftService.getFloorsLog().stream().mapToInt(Integer::intValue).toArray();
    }

    public enum Direction {
        UP, DOWN
    }

    private static class Passenger {
        private int order;
        private int fromFloor;
        private int toFloor;
        private Direction direction;

        public Passenger(int order, int fromFloor, int toFloor) {
            this.order = order;
            this.fromFloor = fromFloor;
            this.toFloor = toFloor;
            direction = toFloor > fromFloor ? Direction.UP : Direction.DOWN;
        }

        public int getOrder() {
            return order;
        }

        public void setOrder(int order) {
            this.order = order;
        }

        public int getFromFloor() {
            return fromFloor;
        }

        public void setFromFloor(int fromFloor) {
            this.fromFloor = fromFloor;
        }

        public int getToFloor() {
            return toFloor;
        }

        public void setToFloor(int toFloor) {
            this.toFloor = toFloor;
        }

        public Direction getDirection() {
            return direction;
        }

        public void setDirection(Direction direction) {
            this.direction = direction;
        }
    }

    private static class Lift {

        private int capacity;
        private int currentFloor = 0;
        private List<Passenger> ridingPassengers;
        private Direction direction = Direction.UP;

        public Lift(int capacity) {
            this.capacity = capacity;
            ridingPassengers = new ArrayList<>();
        }

        public void swapDirection() {
            if (direction == Direction.UP) {
                direction = Direction.DOWN;
            } else {
                direction = Direction.UP;
            }
        }

        public List<Integer> listDestinationFloors() {
            return ridingPassengers.isEmpty()
                    ? List.of()
                    : ridingPassengers.stream()
                            .map(Passenger::getToFloor)
                            .distinct()
                            .collect(Collectors.toList());
        }

        public void inputPassengers(List<Passenger> passengers) {
            ridingPassengers.addAll(passengers);
        }

        public boolean isHavePassengersToExit(int floor) {
            return ridingPassengers.stream().anyMatch(passenger -> passenger.getToFloor() == floor);
        }

        public boolean isEmpty() {
            return ridingPassengers.isEmpty();
        }

        public int getVacantSpots() {
            return capacity - ridingPassengers.size();
        }

        public void pushOutPassengers(int floor) {
            ridingPassengers = ridingPassengers.stream()
                    .filter(passenger -> passenger.getToFloor() != floor)
                    .collect(Collectors.toList());
        }

        public int getCapacity() {
            return capacity;
        }

        public void setCapacity(int capacity) {
            this.capacity = capacity;
        }

        public int getCurrentFloor() {
            return currentFloor;
        }

        public void setCurrentFloor(int currentFloor) {
            this.currentFloor = currentFloor;
        }

        public List<Passenger> getRidingPassengers() {
            return ridingPassengers;
        }

        public void setRidingPassengers(List<Passenger> ridingPassengers) {
            this.ridingPassengers = ridingPassengers;
        }

        public Direction getDirection() {
            return direction;
        }

        public void setDirection(Direction direction) {
            this.direction = direction;
        }
    }

    private static class LiftService {

        private Map<Direction, List<Integer>> floorPressedButtons;
        private List<Passenger> waitingPassengers;
        private Lift lift;
        private int maxFloor;
        private List<Integer> floorsLog;

        public LiftService(Lift lift) {
            this.waitingPassengers = new ArrayList<>();
            floorPressedButtons = new HashMap<>();
            floorsLog = new ArrayList<>();
            this.lift = lift;
        }

        private void handleNextFloor() {
            logStopAtFloor(lift.getCurrentFloor());
            handleLiftStop(lift.getCurrentFloor());
            lift.setCurrentFloor(getNextFloorNumber());
        }

        private void handleLiftStop(int floor) {
            if (lift.isHavePassengersToExit(floor)) {
                lift.pushOutPassengers(floor);
            }
            if (floorsLog.size() > 1 && (lift.getCurrentFloor() == maxFloor || lift.getCurrentFloor() == 0)) {
                lift.swapDirection();
            }
            loadPassengersToLift(floor);
        }

        private void loadPassengersToLift(int floor) {
            int vacantSpots = lift.getVacantSpots();
            List<Passenger> waitingToBoardPassengers = listWaitingToBoardPassengers(floor);
            if (vacantSpots > 0 && !waitingToBoardPassengers.isEmpty()) {
                List<Passenger> leftPassengers = new ArrayList<>();
                if (vacantSpots > waitingToBoardPassengers.size()) {
                    leftPassengers = waitingToBoardPassengers;
                } else {
                    for (int i = 0; i < vacantSpots; i++) {
                        leftPassengers.add(waitingToBoardPassengers.get(i));
                    }
                }
                List<Integer> leftPassengersOrders = leftPassengers.stream()
                        .map(Passenger::getOrder)
                        .collect(Collectors.toList());
                waitingPassengers = waitingPassengers.stream()
                        .filter(passenger ->
                                !(passenger.getFromFloor() ==
                                        floor && leftPassengersOrders.contains(passenger.getOrder())))
                        .collect(Collectors.toList());
                lift.inputPassengers(leftPassengers);
            }
        }

        private List<Passenger> listWaitingToBoardPassengers(int floor) {
            return waitingPassengers
                    .stream()
                    .filter(passenger -> passenger.getFromFloor() == floor)
                    .filter(passenger -> floor == 0 || floor == maxFloor || passenger.getDirection() == lift.getDirection())
                    .sorted(Comparator.comparing(Passenger::getOrder))
                    .collect(Collectors.toList());
        }

        public boolean isAllPassengersDeliveredAndLiftStoppedAtBasement() {
            return waitingPassengers.isEmpty() && lift.isEmpty() && lift.getCurrentFloor() == 0;
        }

        public void setWaitingPassengers(int[][] passengersAsArray) {
            maxFloor = passengersAsArray.length - 1;
            IntStream.range(0, passengersAsArray.length).forEach(fromFloor -> {
                int[] passengersFromFloor = passengersAsArray[fromFloor];
                System.out.println(Arrays.toString(passengersAsArray[fromFloor]));
                if (passengersFromFloor.length > 0) {
                    IntStream.range(0, passengersFromFloor.length)
                            .forEach(passengerOrder -> {
                                int toFloor = passengersFromFloor[passengerOrder];
                                if (toFloor > maxFloor) {
                                    maxFloor = toFloor;
                                }
                                waitingPassengers.add(new Passenger(passengerOrder, fromFloor, toFloor));
                            });
                }
            });
        }

        public int getNextFloorNumber() {
            if (waitingPassengers.isEmpty() && lift.getRidingPassengers().isEmpty()) {
                return 0;
            }
            List<Integer> destinationFloorsFromLift = lift.listDestinationFloors()
                    .stream()
                    .filter(floor -> lift.getDirection() == Direction.UP
                            ? floor > lift.getCurrentFloor()
                            : floor < lift.getCurrentFloor())
                    .collect(Collectors.toList());
            Map<Direction, List<Integer>> destinationFloorsFromBuildingMap = recalculateFloorPressedButtons();
            List<Integer> destinationFloorsFromBuilding = new ArrayList<>();
            if (destinationFloorsFromBuildingMap.containsKey(lift.getDirection())) {
                destinationFloorsFromBuilding.addAll(destinationFloorsFromBuildingMap.get(lift.getDirection()));
            }
            if (isEdgeFloorPassengerWaiting(lift.getDirection())) {
                destinationFloorsFromBuilding.add(lift.getDirection() == Direction.UP ? maxFloor : 0);
            }
            destinationFloorsFromBuilding = destinationFloorsFromBuilding.stream()
                    .filter(floor -> lift.getDirection() == Direction.UP
                            ? floor > lift.getCurrentFloor()
                            : floor < lift.getCurrentFloor())
                    .collect(Collectors.toList());

            //no one in lift and in building on current direction
            if (destinationFloorsFromLift.isEmpty() && destinationFloorsFromBuilding.isEmpty()) {
                lift.swapDirection();
                List<Integer> floors = recalculateFloorPressedButtons().get(lift.getDirection());
                if (floors == null) {
                    floors = new ArrayList<>();
                }
                if (isEdgeFloorPassengerWaiting(lift.getDirection())) {
                    floors.add(lift.getDirection() == Direction.UP ? maxFloor : 0);
                }
                if (floors.isEmpty()) {
                    lift.swapDirection();
                    floors = recalculateFloorPressedButtons().get(lift.getDirection());
                }
                return lift.getDirection() == Direction.UP
                        ? Collections.min(floors)
                        : Collections.max(floors);
            //someone in lift
            } else if (!destinationFloorsFromLift.isEmpty() && destinationFloorsFromBuilding.isEmpty()) {
                return lift.getDirection() == Direction.UP
                        ? Collections.min(destinationFloorsFromLift)
                        : Collections.max(destinationFloorsFromLift);
            //no one in lift but there is someone at building
            } else if (destinationFloorsFromLift.isEmpty()) {
                return lift.getDirection() == Direction.UP
                        ? Collections.min(destinationFloorsFromBuilding)
                        : Collections.max(destinationFloorsFromBuilding);
              //someone in lift and in building
            } else {
                List<Integer> list = Stream.concat(
                            destinationFloorsFromLift.stream(),
                            destinationFloorsFromBuilding.stream())
                        .distinct()
                        .collect(Collectors.toList());
                return lift.getDirection() == Direction.UP
                        ? Collections.min(list)
                        : Collections.max(list);
            }
        }

        public void closeLogs() {
            if (floorsLog.get(floorsLog.size() - 1) != 0) {
                floorsLog.add(0);
            }
            List<Integer> sanitizedLogs = new ArrayList<>();
            for (int i = 0; i < floorsLog.size(); i++) {
                if (i + 1 < getFloorsLog().size()) {
                    if (floorsLog.get(i).intValue() != floorsLog.get(i + 1).intValue()) {
                        sanitizedLogs.add(floorsLog.get(i));
                    }
                } else {
                    sanitizedLogs.add(floorsLog.get(i));
                }
            }
            floorsLog = sanitizedLogs;
        }

        private boolean isEdgeFloorPassengerWaiting(Direction direction) {
            return direction == Direction.UP
                    ? waitingPassengers.stream().anyMatch(passenger -> passenger.getFromFloor() == maxFloor)
                    : waitingPassengers.stream().anyMatch(passenger -> passenger.getFromFloor() == 0);
        }

        public Map<Direction, List<Integer>> recalculateFloorPressedButtons() {
            floorPressedButtons = new HashMap<>();
            List<Integer> upPressedButton = listFloorWithPressedButtons(Direction.UP);
            List<Integer> downPressedButton = listFloorWithPressedButtons(Direction.DOWN);
            if (!upPressedButton.isEmpty()) {
                floorPressedButtons.put(Direction.UP, upPressedButton);
            }
            if (!downPressedButton.isEmpty()) {
                floorPressedButtons.put(Direction.DOWN, downPressedButton);
            }
            return floorPressedButtons;
        }

        private List<Integer> listFloorWithPressedButtons(Direction direction) {
            return waitingPassengers.stream()
                    .filter(passenger -> passenger.getDirection() == direction)
                    .map(Passenger::getFromFloor)
                    .distinct()
                    .collect(Collectors.toList());
        }

        public void logStopAtFloor(int floor) {
            floorsLog.add(floor);
        }

        public List<Integer> getFloorsLog() {
            return floorsLog;
        }

        public void setFloorsLog(List<Integer> floorsLog) {
            this.floorsLog = floorsLog;
        }
    }

}

___________________________________________________
import java.util.*;
import java.util.stream.Collectors;
public class Dinglemouse {

    public static int[] theLift(final int[][] queues, final int capacity) {
        if(queueIsEmpty(queues)){return new int[]{0}; }
        List<Integer> theLift  = new ArrayList<>(capacity);
        List<Integer> theLiftStopRecord  = new ArrayList<>();
        Boolean  isUp =Boolean.TRUE;
        int curFloor = 0;
        while (true){
               if(theLift.isEmpty()&&queueIsEmpty(queues)) {
                if(curFloor!=0){theLiftStopRecord.add(0);}
                break;
                }
               if(canStopLift(queues,curFloor,theLift,isUp)) { doTakeLift(queues,capacity,curFloor,theLift,theLiftStopRecord,isUp);}
               if(isUp){
                   if(canChangeDirection(queues,curFloor,theLift,isUp)){

                       isUp=false;
                       continue;
                   }
                   curFloor++;
                }
               else  {
                   if(canChangeDirection(queues,curFloor,theLift,isUp)){

                       isUp=true;
                       continue;
                   }
                   curFloor--;
               }

        }
        //Your code here
        return  theLiftStopRecord.stream().mapToInt(Integer::valueOf).toArray();
    }

    public static  boolean canChangeDirection(int [][]queues ,int curFloor,List<Integer> theLift,Boolean isUp){

        if(theLift.size()!=0){return false;}
        if(isUp&&curFloor==queues.length-1) return  true;
        int laster=curFloor;
        if(isUp) {
            for (int i = curFloor, len = queues.length; i < len; i++) {
                int finalI = i;
                if (Arrays.stream(queues[i]).anyMatch(t -> t > finalI)) return false;
                if(queues[i].length>0) {laster=i;}
            }
        }
        else{
            for (int j = curFloor; j >=0 ; j--) {
                int finalJ = j;
                if (Arrays.stream(queues[j]).anyMatch(t -> t < finalJ)) return false;
                if(queues[j].length>0) {laster=j;}
            }
        }
        return laster==curFloor;
    }

    public static boolean queueIsEmpty(int [][] queue){
        for (int [] t:queue) {
            if(t.length>0) return  false;
        }
        return  true;
    }

    public  static  boolean canStopLift(final int[][] queues,int curFloor,List<Integer> theLift,Boolean isUp){
        if( theLift.contains(curFloor)) return  true;
        if( isUp  &&  Arrays.stream(queues[curFloor]).anyMatch(t->t>curFloor)) return  true;
        if(!isUp && Arrays.stream(queues[curFloor]).anyMatch(t->t<curFloor) ) return  true;
        return  curFloor==0;
    }

    public static void doTakeLift(final int[][] queues, final int capacity,int curFloor,List<Integer> theLift,List<Integer> theLiftStopRecord,Boolean isUp){
                 theLift.removeIf(t->t==curFloor);
                  if(theLiftStopRecord.size()==0 || theLiftStopRecord.get(theLiftStopRecord.size()-1) != curFloor) {
                      theLiftStopRecord.add(curFloor);
                  }
                     for (int i = 0,len=queues[curFloor].length; i <len ; i++) {
                         if(isUp && theLift.size()<capacity && queues[curFloor][i]> curFloor){
                             theLift.add(queues[curFloor][i]);
                             queues[curFloor][i] = -1;
                         }
                         if(!isUp&& theLift.size()<capacity&& queues[curFloor][i]< curFloor ){
                             theLift.add(queues[curFloor][i]);
                             queues[curFloor][i] = -1;
                         }
                 }
                 queues[curFloor] = Arrays.stream(queues[curFloor]).filter(t->t!=-1).toArray();

    }


}
