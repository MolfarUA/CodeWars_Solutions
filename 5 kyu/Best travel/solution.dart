import 'dart:math';

int chooseBestSum(int t, int k, List<int> ls) {
  int result = combinations(t, k, ls, 0);
  return result > 0 ? result : -1;
}

int combinations(int t, int k, List<int> ls, int i) {
  if (k == 0 && t >= 0)
  {
    return 0;
  }
  else if (k < 0 || i >= ls.length)
  {
    return -9007199254740991;
  }
  else
  {
    return max(combinations(t, k, ls, i + 1), ls[i] + combinations(t - ls[i], k - 1, ls, i + 1));
  }
}
_______________________________________
import 'dart:math';
int chooseBestSum(int t, int k, List<int> ls) {
    try{
        if (k == 1) {
          return ls.where((v) => v <= t).toList()?.reduce(max);
        } else {
          return List.generate(ls.length - 1, (index) { int bs = chooseBestSum(t - ls[index], k -1, ls.sublist(index + 1));
                                                       return bs > 0? ls[index] + bs :-1;}).where((v) => v <= t).toList().reduce(max);
        }
      } catch(e) {
        return -1;
    }
}

_______________________________________
import 'dart:math' as math;
int aux(int t, int k, List<int> ls, int frm) {
    if (k == 0)
        if (t >= 0) return 0; else return t;
    else
        if (t < k) return -1;           
    int best = -1; int tmpBest;
    for (int i = frm; i < ls.length; i++) {
        tmpBest = aux(t - ls[i], k - 1, ls, i + 1);
        if (tmpBest >= 0)
            best = math.max(best, ls[i] + tmpBest);
    }
    return best;
}
int chooseBestSum(int t, int k, List<int> ls) {
    return aux(t, k, ls, 0);
}
_______________________________________
int chooseBestSum(int d, int t, List<int> lst) {  
  if (t > lst.length) {
    return -1;
  }
  
  List<int> pos = List.generate(t, (i) => lst.length - t + i);
  
  int sum = d + 1;
  int mx = 0;
  
  while (true) {
    sum = pos.fold(0, (prev, curr) => prev + lst[curr]);    
    if (sum <= d && sum > mx) {
      mx = sum;
    }
    
    if (pos.last == pos.length - 1) {
      break;
    }
    
    if (pos[0] != 0) {
      pos[0]--;
    } else {
      for (int i = 0; i < pos.length; ++i) {
        if (pos[i] != i) {
          pos[i]--;
          for (int j = 0; j < i; ++j) {
            pos[j] = pos[i] - i + j;
          }
          break;
        }
      }
    }
  }
  
  if (mx > d || mx == 0) {
    return -1;
  }
  return mx;
}
_______________________________________
import 'dart:math';

int chooseBestSum(int t, int k, List<int> ls) {
  int allCombinations = pow(2, ls.length).toInt() - 1;
  List<int> mass = [];

  // iteration over all numbers
  for (int i = 0; i <= allCombinations; i++) {
    String binNum = i.toRadixString(2).padLeft(ls.length, '0');

    // selection of numbers with the desired number of units
    if ('1'.allMatches(binNum).length == k) {
      int maxDistance = 0;

      // iterate over each character '0' or '1' and sum
      for (int j = 0; j < binNum.length; j++) {
        if (binNum.split('')[j] == '1') maxDistance += ls[j];
      }
      mass.add(maxDistance);
    }
  }
  mass.sort((a,b) => b.compareTo(a));
  for (var m in mass) if (m <= t) return m;
  return -1;
}
