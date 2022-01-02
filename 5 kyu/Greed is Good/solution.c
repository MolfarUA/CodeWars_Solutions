int score(const int dice[5]) {
    int count[7] = {0, 0, 0, 0, 0, 0, 0};
    for( int i = 0; i < 5; i++ ) {
        count[dice[i]]++;
    }
    
    int score = 0;
    // Three 1's => 1000 points
    score += 1000 * (count[1] / 3);
    // Three 6's =>  600 points
    score += 600 * (count[6] / 3);
    // Three 5's =>  500 points
    score += 500 * (count[5] / 3);
    // Three 4's =>  400 points
    score += 400 * (count[4] / 3);
    // Three 3's =>  300 points
    score += 300 * (count[3] / 3);
    // Three 2's =>  200 points
    score += 200 * (count[2] / 3);
    // One   1   =>  100 points
    score += 100 * (count[1] % 3);
    // One   5   =>   50 point
    score += 50 * (count[5] % 3);
    
    return score;
}
_____________________________________________
int score(const int dice[5])
{
  int count[6] = { 0 };
  int i;
  int score = 0;

  for (i = 0; i < 5; i++)
  {
    count[dice[i]-1]++;
  }

  for (i = 0; i < 6; i++)
  {
    if (count[i] >= 3)
    {
      switch (i)
      {
      case 0:
        score += 1000;
        break;
      default:
        score += (i + 1) * 100;
      }
      count[i] -= 3;
    }
    if (i == 0)
      score += count[i] * 100;
    else if (i == 4)
      score += count[i] * 50;
  }

  return score;
}
_____________________________________________
#include <stdio.h>

#define N_SIDES 6
#define N_ROLLS 5

static int trip_reward[N_SIDES] = {
  1000,
  200,
  300,
  400,
  500,
  600
};

static int singles_reward[N_SIDES] = {
  100,
  0,
  0,
  0,
  50,
  0
};

int score(const int dice[N_ROLLS]) {
  int i;
  int trips;
  int score = 0;
  int totals[N_SIDES] = {0};
  
  for (i=0;i<N_ROLLS;i++) {
    if (dice[i] > N_SIDES)
      continue; // never trust input... and segfaults are bad
    totals[dice[i]-1]++;
  }
  for (i=0;i<N_SIDES;i++) {
    score += (totals[i] / 3) * trip_reward[i];
    score += (totals[i] % 3) * singles_reward[i];
  }
  return score;
}
_____________________________________________
int score(const int dice[5]) {
  int score = 0, count[6] = {0};
  for (int i=0; i<5; i++) count[dice[i]-1]++;
  for (int i=0; i<6; i++) if (count[i] >= 3) score += (i==0)? 1000 : 100 * (i + 1);
  return score + 100 * (count[0] % 3) + 50 * (count[4] % 3);
}
