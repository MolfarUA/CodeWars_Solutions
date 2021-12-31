#include <vector>
#include <deque>
#include <algorithm>

std::vector<int> the_lift(const std::vector<std::vector<int>> &queues, int capacity) {
  using namespace std;
  
  int N = queues.size();

  vector<deque<int>> wantUp, wantDown;
  vector<int> button;
  vector<int> seq;
  int liftCount;
    
  auto getOn = [&](int fl, bool goUp)
  {
    if(goUp)
    {
      bool wantOn = !wantUp[fl].empty();
      while(!wantUp[fl].empty() && liftCount < capacity)
      {
        ++button[wantUp[fl].front()];
        ++liftCount;
        wantUp[fl].pop_front();
      }
      return wantOn;
    }
    else
    {
      bool wantOn = !wantDown[fl].empty();
      while(!wantDown[fl].empty() && liftCount < capacity)
      {
        ++button[wantDown[fl].front()];
        ++liftCount;
        wantDown[fl].pop_front();
      }
      return wantOn;
    }
  };
  
  auto emptyTarget = [&](int fl, bool& goUp)
  {
    if(goUp)
    {
      for(; fl < N - 1; ++fl)
        if(!wantUp[fl].empty())
          return fl;
      goUp = false;
      for(; fl > 0; --fl)
        if(!wantDown[fl].empty())
          return fl;
      goUp = true;
      for(; fl < N - 1; ++fl)
        if(!wantUp[fl].empty())
          return fl;
      return -1;
    }
    else
    {
      for(; fl > 0; --fl)
        if(!wantDown[fl].empty())
          return fl;
      goUp = true;
      for(; fl < N - 1; ++fl)
        if(!wantUp[fl].empty())
          return fl;
      goUp = false;
      for(; fl > 0; --fl)
        if(!wantDown[fl].empty())
          return fl;
      return -1;
    }
  };
  
  wantUp.resize(N);
  wantDown.resize(N);
  for(int fl = 0; fl < N; fl++)
  {
    for(int dest : queues[fl])
    {
      if(dest > fl)
        wantUp[fl].push_back(dest);
      else
        wantDown[fl].push_back(dest);
    }
  }
  
  int curr = 0;
  int next = 0;
  bool goUp = true;
  button.resize(N);
  
  liftCount = 0;
  seq.push_back(0);
  while((next = emptyTarget(curr, goUp)) != -1)
  {
    curr = next;
    if(seq.back() != curr) seq.push_back(curr);
    getOn(curr, goUp);
    while(liftCount > 0)
    {
      bool stopped = false;
      if(goUp) ++curr; else --curr;
      if(button[curr] > 0)
      {
        liftCount -= button[curr];
        button[curr] = 0;
        stopped = true;
      }
      stopped |= getOn(curr, goUp);
      if(stopped) seq.push_back(curr);
    }
  }
  
  if(curr != 0) seq.push_back(0);
  return seq;
}

___________________________________________________
#include <vector>
#include <algorithm>

bool HasPassengers(const std::vector<std::vector<int>> &queues, const std::vector<int> passengers) {
  bool flag = false;
  for (auto it : queues) if (it.size() != 0) flag = true;
  if (flag || passengers.size() != 0) return true;
  return false;
}

std::vector<int> the_lift(const std::vector<std::vector<int>> &queues, int capacity) {
  bool flag = false;
  std::vector<int> passengers = {};
  std::vector<int> to_remove;
  int current_floor = 0;
  std::vector<std::vector<int>> _queues = queues;
  std::vector<int> result = { 0 };
  int size;
  
  while (HasPassengers(_queues, passengers)) {
    if (current_floor == 0 || current_floor == _queues.size() - 1) flag = !flag;

    size = passengers.size();
    passengers.erase(std::remove(passengers.begin(), passengers.end(), current_floor), passengers.end());
    if (passengers.size() != size) result.push_back(current_floor);

    to_remove = {};
    for (auto it = _queues[current_floor].begin(); it != _queues[current_floor].end(); it++) {
      if (flag && *it - current_floor > 0) {
        if (result.back() != current_floor) result.push_back(current_floor);
        if (passengers.size() < capacity) {
          to_remove.push_back(it - _queues[current_floor].begin());
          passengers.push_back(*it);
        } 
      }
      else if (!flag && *it - current_floor < 0) {
        if (result.back() != current_floor) result.push_back(current_floor);
        if (passengers.size() < capacity) {
          to_remove.push_back(it - _queues[current_floor].begin());
          passengers.push_back(*it);
        } 
      }
    }

    for (auto it : to_remove) _queues[current_floor][it] = -1;
    _queues[current_floor].erase(std::remove(_queues[current_floor].begin(), _queues[current_floor].end(), -1), _queues[current_floor].end());

    flag ? current_floor++ : current_floor--;
  }
  if (result.back() != 0) result.push_back(0);
  return result;
}

___________________________________________________
#include <vector>

std::vector<int> the_lift(std::vector<std::vector<int>> &queues, int capacity) {
 
  //defining variables used in the loops at their starting values
  int level = 0; //current level of the lift, starts on 0
  int dir = 1; //direction of travel (1=up, -1=down), added to level to move between floors
  bool start = true;
  std::vector<int> visits; //list of visited floors, starts empty
  std::vector<int> inside; // list of people in the lift
  
  //loop continuously between levels, until broken when task is completed
  while(1){
    //on each level assume the lift will not stop
    bool stop = false;
    //check if we are on ground or top floor, if we are, reverse direction
    if ((level == 0 || level == queues.size() - 1) && start == false){
        dir = -1* dir;
    }
    //check if people want to get out, if so, remove them from the lift, and set stop to true
    for (auto it = inside.begin(); it != inside.end(); ++it){
      if (*it == level){
        inside.erase(it);
        it--;
        stop = true;
      }
    }
    
    //check if people want to get on in the current direction
    //if they do, add to lift, remove from queue, and set stop to true
    for (auto it = queues[level].begin(); it != queues[level].end(); ++it){
      if((dir == 1 && *it > level)||(dir == -1 && *it < level)){
        stop = true;
        if (inside.size() < capacity){
          inside.push_back(*it);
          queues[level].erase(it);
          it--;
        }
      }
    }
    //if this is the first loop, add current level to the list of visited floors
    if(start == true){
      start = false;
      visits.push_back(level);
    }
    //if lift has stopped, add current level to list of visited floors
    else if(stop ==true && visits.back()!= level){
      visits.push_back(level);
    }
    //check if the queues are empty
    bool queuesEmpty = true;
    for (auto it = queues.begin(); it != queues.end(); ++it){
        if(it->empty() == false){
            queuesEmpty = false;
            break;
        }
    }
    
    //if queues are empty and no one is on the lift, break the loop
    if(queuesEmpty == true && inside.empty() == true){
        break;
    }
    // add the direction to the current level to go up/down 1 floor
    level += dir;
  }
  
  //if the lift is not already on floor 0, return to floor 0
  if(level != 0){
      visits.push_back(0);
  }
  return visits;
}

___________________________________________________
#include <vector>

std::vector<int> the_lift(const std::vector<std::vector<int>> &queues, int capacity) {
 
  //defining variables used in the loops at their starting values
  std::vector<std::vector<int>> queuesList = queues;
  int level = 0; //current level of the lift, starts on 0
  int dir = -1; //starts at -1 (down) as it will be reversed at the start as we start on 0
  bool start = true;
  std::vector<int> visits; //list of visited floors, starts empty
  std::vector<int> inside; // list of people in the lift
  
  //loop continuously between levels, until broken when task is completed
  while(1){
    //on each level assume the lift will not stop
    bool stop = false;
    //check if we are on ground or top floor, if we are, reverse direction
    if (level == 0 || level == queuesList.size() - 1){
        dir = -1* dir;
    }
    //check if people want to get out, if so, remove them from the lift, and set stop to true
    for (auto it = inside.begin(); it != inside.end(); ++it){
      if (*it == level){
        inside.erase(it);
        it--;
        stop = true;
      }
    }
    
    //check if people want to get on in the current direction
    //if they do, add to lift, remove from queue, and set stop to true
    for (auto it = queuesList[level].begin(); it != queuesList[level].end(); ++it){
      if((dir == 1 && *it > level)||(dir == -1 && *it < level)){
        stop = true;
        if (inside.size() < capacity){
          inside.push_back(*it);
          queuesList[level].erase(it);
          it--;
        }
      }
    }
    //if this is the first loop, add current level to the list of visited floors
    if(start == true){
      start = false;
      visits.push_back(level);
    }
    //if lift has stopped, add current level to list of visited floors
    else if(stop ==true && visits.back()!= level){
      visits.push_back(level);
    }
    //check if the queues are empty
    bool queuesEmpty = true;
    for (auto it = queuesList.begin(); it != queuesList.end(); ++it){
        if(it->empty() == false){
            queuesEmpty = false;
            break;
        }
    }
    
    //if queues are empty and no one is on the lift, break the loop
    if(queuesEmpty == true && inside.empty() == true){
        break;
    }
    // add the direction to the current level to go up/down 1 floor
    level += dir;
  }
  
  //if the lift is not already on floor 0, return to floor 0
  if(level != 0){
      visits.push_back(0);
  }
  return visits;
}

___________________________________________________
#include <vector>

std::vector<int> the_lift(const std::vector<std::vector<int>> &queues, int capacity) {
 
  std::vector<std::vector<int>> queuesList = queues;
  
  int level = 0;
  int dir = -1;
  bool start = true;
  std::vector<int> visits;
  std::vector<int> inside;
  //std::vector<int>::iterator it;
    
    std::cout << queuesList.size() << std::endl;
  
  while(1){
    bool stop = false;
    if (level == 0 || level == queuesList.size() - 1){
        dir = -1* dir;
    }
    for (auto it = inside.begin(); it != inside.end(); ++it){
      if (*it == level){
        inside.erase(it);
        it--;
        stop = true;
      }
    }
    
    for (auto it = queuesList[level].begin(); it != queuesList[level].end(); ++it){
      if((dir == 1 && *it > level)||(dir == -1 && *it < level)){
        stop = true;
        if (inside.size() < capacity){
          inside.push_back(*it);
          queuesList[level].erase(it);
          it--;
        }
      }
    }
    if(start == true){
      start = false;
      visits.push_back(level);
    }
    else if(stop ==true && visits.back()!= level){
      visits.push_back(level);
    }
    bool queuesEmpty = true;
    for (auto it = queuesList.begin(); it != queuesList.end(); ++it){
        if(it->empty() == false){
            queuesEmpty = false;
            break;
        }
    }

    if(queuesEmpty == true && inside.empty() == true){
        break;
    }

    level += dir;
  }
  
  if(level != 0){
      visits.push_back(0);
  }
  return visits;
}
