int sumOfIntervals(List<List<int>> intervals) {
  Set<int> nums = Set();
  for (final interval in intervals) {
    nums.addAll(List.generate(interval[1] - interval[0], (i) => interval[0] + i));
  }
  return nums.length;
}
___________________
int sumOfIntervals(List<List<int>> intervals) 
{
  intervals.sort((a, b) => a[0] - b[0]);
  
  for(int i = 0; i < intervals.length - 1; ++i) 
  {
    if (intervals[i][1] < intervals[i + 1][0]) continue;
    if (intervals[i][1] >= intervals[i + 1][1]) intervals[i + 1][1] = intervals[i][1];
      
    intervals[i + 1][0] = intervals[i][0];
    intervals[i][0] = intervals[i][1] = 0;
  }
  
  return intervals.fold(0, (sum, e) => sum + e[1] - e[0]);
}
____________________________
int sumOfIntervals(List<List<int>> intervals) => intervals.expand((x) => List<int>.generate(x[1] - x[0], (i) => i + x[0])).toSet().length;
_________________________
int sumOfIntervals(List<List<int>> inter) {
  return inter.fold<Set<int>>({}, (acc, value) {
    for (var i = value.first; i < value.last; i++) acc.add(i);
    return acc;
  }).length;
}
_____________________
int sumOfIntervals(List<List<int>> intervals) {
  List<List<int>> list = [];

  intervals.sort((a, b) {
    if(a[0] != b[0]) {
      if(a[0] > b[0]) return 1;
      return -1;   
    } else {  
     if(a[1] > b[1]) return 1;
        return -1;       
      }
  });

  int sum = 0;

  int start = intervals[0][0], end = intervals[0][1];

  for (int i = 1, len = intervals.length; i < len; i++) {
    if (intervals[i][0] <= end) {
      end = max(end, intervals[i][1]);
    } else {
      sum += end - start;
      start = intervals[i][0];
      end = intervals[i][1];
    }
  }

  sum += end - start;
  return sum;

}

int max(a,b) => a > b ? a : b;
__________________________-
int sumOfIntervals(List<List<int>> intervals) {
  List<int> list = [];
  for (List<int> item in intervals) {
    for (int i = item[0]; i < item[1]; i++) {
      if (!list.contains(i)) list.add(i);
    }
  }
  return list.length;
}
_____________________________
int sumOfIntervals(List<List<int>> intervals) {
  intervals.sort((a, b) => a[0] - b[0]);
  for(var i = 1; i < intervals.length; i++) {
    if (intervals[i][1] <= intervals[i - 1][1]) { 
      intervals[i] = intervals[i - 1];
      intervals[i - 1] = [0, 0];      
    } else if (intervals[i][0] <= intervals[i - 1][1]) {
      intervals[i] = [intervals[i - 1][0], intervals[i][1]];
      intervals[i - 1] = [0, 0];   
    }
  }
  return intervals.fold(0, (p, e) => p + e[1] - e[0]);
}
