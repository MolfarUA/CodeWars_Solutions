using System;
using System.Collections.Generic;
using System.Linq;
public class Dinglemouse
{
    public static int[] TheLift(int[][] queues, int capacity)
    {
      int numOfFloors = queues.Length;
      Queue<int>[] queueUp = new Queue<int>[numOfFloors];
      Queue<int>[] queueDown = new Queue<int>[numOfFloors];
      int[] passengersInQueue;
      List<int> lift = new List<int>();
      bool[] upButtons = new bool[numOfFloors];
      bool[] downButtons = new bool[numOfFloors];
      List<int> floorsLiftSpopped = new List<int>();
      for (int i = 0; i < numOfFloors; i++)
      {
          queueUp[i] = new Queue<int>();
          queueDown[i] = new Queue<int>();
          var passengersToUp = from int toFloor in queues[i]
                               where toFloor > i
                               select toFloor;
          if (passengersToUp.Count() > 0)
          {
              upButtons[i] = true;
              passengersInQueue = passengersToUp.ToArray();
              for (int j = 0; j < passengersToUp.Count(); j++)
              {
                  queueUp[i].Enqueue(passengersInQueue[j]);
              }
          }
          //-----------------------------------------------------
          var passengersToDown = from int toFloor in queues[i]
                                 where toFloor < i
                                 select toFloor;
          if (passengersToDown.Count() > 0)
          {
              downButtons[i] = true;
              passengersInQueue = passengersToDown.ToArray();
              for (int k = 0; k < passengersToDown.Count(); k++)
              {
                  queueDown[i].Enqueue(passengersInQueue[k]);
              }
          }
      }
      int floor = 0;
      bool liftUp = true;
      int passengersToEnter;
      while (true)
      {
          switch (liftUp)
          {
              case true:
                  lift.RemoveAll(x => x == floor);
                  passengersToEnter = queueUp[floor].Count() + lift.Count;
                  if (passengersToEnter <= capacity)
                  {
                      upButtons[floor] = false;
                      foreach (var passenger in queueUp[floor])
                      {
                          lift.Add(passenger);
                      }
                      queueUp[floor].Clear();
                  }
                  else
                  {
                      upButtons[floor] = true;
                      for (int i = lift.Count; i < capacity; i++)
                      {
                          lift.Add(queueUp[floor].Dequeue());
                      }
                  }
                  var pressedUpButtons = Array.IndexOf(upButtons, true, floor + 1);
                  if (pressedUpButtons != -1)
                  {
                      if (lift.Count != 0)
                      {
                          floorsLiftSpopped.Add(floor);
                          floor = Math.Min(lift.Min(), pressedUpButtons);
                      }
                      else
                      {
                          floorsLiftSpopped.Add(floor);
                          floor = pressedUpButtons;
                      }
                  }
                  else
                  {
                      if (lift.Count != 0)
                      {
                          floorsLiftSpopped.Add(floor);
                          floor = lift.Min();
                      }
                      else
                      {
                          int nextFloor = -1;
                          for (int j = numOfFloors - 1; j > floor; j--)
                          {
                              if (downButtons[j])
                              {
                                  nextFloor = j;
                                  break;
                              }
                          }
                          if (nextFloor == -1)
                          {
                              if (upButtons.All(x => x == false) && downButtons.All(x => x == false) && lift.Count == 0 && floor != 0)
                              {
                                  floorsLiftSpopped.Add(floor);
                                  floor = 0;
                                  floorsLiftSpopped.Add(floor);
                                  break;
                              }
                              else
                              {
                                  liftUp = false;
                              }
                          }
                          else
                          {

                              floorsLiftSpopped.Add(floor);

                              floor = nextFloor;
                              liftUp = false;
                          }
                      }
                  }
                  break;
              default:
                  lift.RemoveAll(x => x == floor);
                  passengersToEnter = queueDown[floor].Count + lift.Count;
                  if (passengersToEnter <= capacity)
                  {
                      downButtons[floor] = false;
                      foreach (var passenger in queueDown[floor])
                      {
                          lift.Add(passenger);
                      }
                      queueDown[floor].Clear();
                  }
                  else
                  {
                      downButtons[floor] = true;
                      for (int i = lift.Count; i < capacity; i++)
                      {
                          lift.Add(queueDown[floor].Dequeue());
                      }
                  }
                  int pressedDownButtons = -1;
                  for (int z = floor - 1; z >= 0; z--)
                  {
                      if (downButtons[z])
                      {
                          pressedDownButtons = z;
                          break;
                      }
                  }
                  if (pressedDownButtons != -1)
                  {
                      if (lift.Count != 0)
                      {
                          floorsLiftSpopped.Add(floor);
                          floor = Math.Max(lift.Max(), pressedDownButtons);
                      }
                      else
                      {
                          floorsLiftSpopped.Add(floor);
                          floor = pressedDownButtons;
                      }
                  }
                  else
                  {
                      if (lift.Count != 0)
                      {
                          floorsLiftSpopped.Add(floor);
                          floor = lift.Max();
                      }
                      else
                      {
                          int nextFloor = -1;
                          for (int j = 0; j < floor; j++)
                          {
                              if (upButtons[j])
                              {
                                  nextFloor = j;
                                  break;
                              }
                          }
                          if (nextFloor == -1)
                          {
                              if (upButtons.All(x => x == false) && downButtons.All(x => x == false) && lift.Count == 0 && floor != 0)
                              {
                                  floorsLiftSpopped.Add(floor);
                                  floor = 0;
                                  floorsLiftSpopped.Add(floor);
                                  break;
                              }
                              else
                              {
                                  liftUp = true;
                              }
                          }
                          else
                          {
                              floorsLiftSpopped.Add(floor);
                              floor = nextFloor;
                              liftUp = true;
                          }
                      }
                  }
                  break;
          }
          if (upButtons.All(x => x == false) && downButtons.All(x => x == false) && lift.Count == 0 && floor == 0)
          {
              if (floorsLiftSpopped.Count == 0 || floorsLiftSpopped.Last() != 0)
              {
                  floorsLiftSpopped.Add(0);
              }
              break;
          }
      }
      return floorsLiftSpopped.ToArray();
    }
}

___________________________________________________
using System;
using System.Collections.Generic;
public class Dinglemouse
{
    public static int[] TheLift(int[][] queues, int capacity)
    {
        
        List<int> floors = new List<int>();
        List<int> lift = new List<int>();
        string direction = "up";
        int floor = 0;
      
        int count = 0;
        int z = 0;
        foreach(int[] queue in queues){
          //Console.WriteLine($"{z} {String.Join(",", queue)}");
          if(queue.Length != 0){
            count++;
          }
          z++;
        }
        //Console.WriteLine($"capacity: {capacity}");
      
        if(count == 0){
          return new int[]{0};
        }
      
        int j = 0;
        while (!(count == 0 && lift.Count == 0)){
          //Console.WriteLine("============================");
          //Console.WriteLine($"count = {count}");
          //Console.WriteLine($"lift contains {lift.Count}");
          //Console.WriteLine($"floor: {floor}");
          //Console.WriteLine(direction);
          //Console.WriteLine("queue:");
          //Console.WriteLine($"{String.Join(",", queues[floor])}");
          //Console.WriteLine("lift:");
          //Console.WriteLine($"{String.Join(",", lift.ToArray())}");
          //Console.WriteLine("floors count:");
          //Console.WriteLine($"{String.Join(",", floors.ToArray())}\n");
          bool check = false;
          if(direction == "up" && floor == queues.Length-1){
            direction = "down";
          }
          else if (direction == "down" && floor == 0){
            direction = "up";
          }
          
          //get off lift
          if (lift.Count > 0){
            //Console.WriteLine("jwebfuewbguoqebgoqebqen");
            int i = 0;
            while(i < lift.Count){
              if (lift[i] == floor){
                check = true;
                //Console.WriteLine($"removed {lift[i]}");
                lift.RemoveAt(i);
                continue;
              }
              else{
                i++;
              }
            }
          }
          
          //skip empty floor
          if (queues[floor].Length == 0){
            //Console.WriteLine($"check = {check}");
            if (check == true){
              floors.Add(floor);
            }
            if (direction == "up"){
              floor++;
            }
            else if (direction == "down"){
              floor--;
            }
            continue;
          }
          
          
          
          
          //get as many people as possible
          
          if(direction == "up"){
            for(int i = 0; i < queues[floor].Length; i++){
              if (queues[floor][i]>floor && lift.Count < capacity && queues[floor][i]>=0){
                check = true;
                //Console.WriteLine($"added {queues[floor][i]}");
                lift.Add(queues[floor][i]);
                queues[floor][i] = -1;
              }
              else if (queues[floor][i]>floor && lift.Count >= capacity && queues[floor][i]>=0){
                check = true;
              }
            }
          }
          
          else if(direction == "down"){
            for(int i = 0; i < queues[floor].Length; i++){
              if (queues[floor][i]<floor && lift.Count < capacity && queues[floor][i]>=0){
                check = true;
                //Console.WriteLine($"added {queues[floor][i]}");
                lift.Add(queues[floor][i]);
                queues[floor][i] = -1;
              }
              else if (queues[floor][i]<floor && lift.Count >= capacity && queues[floor][i]>=0){
                check = true;
              }
            }
          }
          
          //Console.WriteLine($"check = {check}");
          if (check == true){
            floors.Add(floor);
          }
          
          
          if (direction == "up"){
            floor++;
          }
          else{
            floor--;
          }
          
          count = 0;
          foreach(int[] queue in queues){
            foreach(int person in queue){
              if (person > -1){
                count++;
                break;
              }
            }
          }
          j++;
          
          if (floors.Count >= 2){
            if (floors[floors.Count-1] == floors[floors.Count-2]){
              floors.RemoveAt(floors.Count-1);
            }
          }
          
        }
        if (floors[floors.Count-1] != 0){
          floors.Add(0);
        }
        if (floors[0] != 0){
          floors.Insert(0, 0);
        }
      
        //Console.WriteLine($"final = {String.Join(",", floors.ToArray())}");
        return floors.ToArray();
    }
}

___________________________________________________
using System;
using System.Collections.Generic;

public class Dinglemouse
{
  public static int[] TheLift(int[][] queues, int capacity)
        {
            for(int i = 0; i < queues.GetLength(0); i++)
            {
                for(int j = 0; j < queues[i].GetLength(0); j++)
                {
                    Console.Write("{0} ", queues[i][j]);
                }
                Console.WriteLine($"| {i}");
            }
            List<int> passengersList = new List<int>();
            List<int> stopsList = new List<int>();
            List<int> passengersOnTheFlor = new List<int>();
            stopsList.Add(0);
            bool passengerOut;
            int maxFlor = queues.GetLength(0);
            while (IsAnyPassengers(queues))
            {
                if (MoveDown(queues, stopsList, passengersList))
                {
                    for (int i = maxFlor - 1; i >= 0; i--)
                    {
                        if (IsButtonDownON(queues[i], i) || passengersList.IndexOf(i) != -1)
                        {
                            Console.WriteLine("Adding flor " + i);
                            if (stopsList[stopsList.Count - 1] != i)
                                stopsList.Add(i);
                            do
                            {
                                passengerOut = passengersList.Remove(i);
                            } while (passengerOut);

                            passengersOnTheFlor = GetInPassengersDown(queues[i], i, capacity, ref passengersList);
                            if (passengersOnTheFlor.Count != 0)
                            {
                                queues[i] = new int[passengersOnTheFlor.Count];
                                passengersOnTheFlor.CopyTo(queues[i]);
                            }
                            else
                                queues[i] = new int[0] { };
                        }
                    }
                }
                else
                {
                    for (int i = 0; i < maxFlor; i++)
                    {
                        if (IsButtonUpON(queues[i], i) || passengersList.IndexOf(i) != -1)
                        {
                            if(stopsList[stopsList.Count - 1] != i)
                                stopsList.Add(i);
                            do
                            {
                                passengerOut = passengersList.Remove(i);
                            } while (passengerOut);

                            passengersOnTheFlor = GetInPassengersUp(queues[i], i, capacity, ref passengersList);
                            if (passengersOnTheFlor.Count != 0)
                            {
                                queues[i] = new int[passengersOnTheFlor.Count];
                                passengersOnTheFlor.CopyTo(queues[i]);
                            }
                            else
                                queues[i] = new int[0] { };
                        }
                    }
                }
            }
            if(stopsList[stopsList.Count - 1] != 0)
                stopsList.Add(0);
            return stopsList.ToArray();
        }

        public static bool IsAnyPassengers(int[][] queues)
        {
            for(int i = 0; i < queues.GetLength(0); i++)
            {
                if (queues[i].Length != 0)
                    return true;
            }
            return false;
        }

        public static bool IsButtonDownON(int[] queue, int flor)
        {
            if (queue.Length == 0)
                return false;
            foreach(int person in queue)
            {
                if (person < flor)
                    return true;
            }
            return false;
        }

        public static bool IsButtonUpON(int[] queue, int flor)
        {
            if (queue.Length == 0)
                return false;
            foreach (int person in queue)
            {
                if (person > flor)
                    return true;
            }
            return false;
        }

        public static List<int> GetInPassengersDown(int[] queue, int flor, int capacity, 
            ref List<int> passangersList)
        {
            List<int> queueAfterLift = new List<int>();
            for(int k = 0; k < queue.Length; k++)
            {
                if (queue[k] < flor && passangersList.Count < capacity)
                    passangersList.Add((int)queue.GetValue(k));
                else
                    queueAfterLift.Add((int)queue.GetValue(k));
            }
            return queueAfterLift;
        }

        public static List<int> GetInPassengersUp(int[] queue, int flor, int capacity,
            ref List<int> passangersList)
        {
            List<int> queueAfterLift = new List<int>();
            for (int k = 0; k < queue.Length; k++)
            {
                if (queue[k] > flor && passangersList.Count < capacity)
                    passangersList.Add((int)queue.GetValue(k));
                else
                    queueAfterLift.Add((int)queue.GetValue(k));
            }
            return queueAfterLift;
        }

        public static bool MoveDown(int[][] queues, List<int> stopsList, List<int> passengersList)
        {
            int flor = stopsList[stopsList.Count - 1];
            Console.WriteLine("Passengers capacity " + passengersList.Count);
            if (passengersList.Count != 0)
            {
                if (passengersList[0] < flor)
                    return true;
                else
                    return false;
            }

            if (stopsList.Count > 1 && flor < stopsList[stopsList.Count - 2])
            {
                for (int i = flor; i >= 0; i--)
                {
                    if (IsButtonDownON(queues[i], i))
                        return true;
                }
                for (int i = 0; i < queues.GetLength(0); i++)
                {
                    if (IsButtonUpON(queues[i], i))
                        return false;
                }
                return true;
            }
            else
            {
                for (int i = flor; i < queues.GetLength(0); i++)
                {
                    if (IsButtonUpON(queues[i], i))
                        return false;
                }
                for (int i = queues.GetLength(0) - 1; i >= 0; i--)
                {
                    if (IsButtonDownON(queues[i], i))
                        return true;
                }
                return false;
            }
        }
}
