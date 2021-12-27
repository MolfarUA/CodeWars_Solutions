export function sumOfIntervals(intervals: [number, number][]) {
  const ranges = new Set<number>();
  intervals.forEach(([start, end]) => {
    for (let i = start; i < end; i++) ranges.add(i);
  });
  return ranges.size;
}
                                
_______________________
export function sumOfIntervals(intervals: [number, number][]): number {
  let sortedIntervals = intervals.sort((first,second) => first[0] - second[0]);
  let currentInterval = sortedIntervals[0];
  let result = 0;
  for (let index = 1; index < sortedIntervals.length; index++) {
    if (sortedIntervals[index][0] <= currentInterval[1]) {
      currentInterval[1] = Math.max(sortedIntervals[index][1], currentInterval[1]);
    }
    else {
      result += currentInterval[1] - currentInterval[0];
      currentInterval = sortedIntervals[index];
    }
  }
  return result + currentInterval[1] - currentInterval[0];
}
    
___________________
export function sumOfIntervals(intervals: [number, number][]) {
  const sorted = intervals.sort(([pa,pb],[a,b]) => (pa - a));
  let pa:number, pb: number;
  return sorted.reduce((sum, [a, b]) => {
    if(pa && a < pb) {
      if(b > pb) {
        sum += b - pb;
        pb = b;
      }
    } else {
      [pa, pb] = [a, b];
      sum += b - a;
    }
    return sum;
  }, 0);
}
    
___________________________
function isIntervalsConnected(int1: [number, number], int2: [number, number]): boolean {
  const [int1Start, int1End] = int1;
  const [int2Start, int2End] = int2;

  return (
    (int1Start <= int2Start && int2Start <= int1End) ||
    (int1Start <= int2End && int2End <= int1End)
  );
}

function mergeIntervals(int1: [number, number], int2: [number, number]): [number, number] {
  return [Math.min(int1[0], int2[0]), Math.max(int1[1], int2[1])];
}

function tryMergeInterval(intervals: [number, number][]): boolean {
  let isMergedSmth = false;

  for (let i = 0; i < intervals.length; i++) {
    for (let j = 0; j < intervals.length; j++) {
      if (i === j) continue;

      if (isIntervalsConnected(intervals[i], intervals[j])) {
        intervals[Math.min(i, j)] = mergeIntervals(intervals[i], intervals[j]);
        intervals.splice(Math.max(i, j), 1);
        isMergedSmth = true;
        break;
      }
    }
  }

  return isMergedSmth;
}

export function sumOfIntervals(intervals: [number, number][]): number {
  const mergedIntervals = [...intervals];

  while (tryMergeInterval(mergedIntervals)) {}

  return mergedIntervals.reduce((a, b) => a + Math.abs(b[1] - b[0]), 0);
}
    
____________________________
export function sumOfIntervals(intervals: [number, number][]) {
  const unique: number[] = []
  
  intervals.forEach(([start, end] )=> {
    for(let i = start; i < end; i++){
      if(unique.indexOf(i) === -1){
        unique.push(i)
      }
    }
  })
  
  return unique.length;
}
                               
______________________________
export function sumOfIntervals(intervals: [number, number][]) {

  const sortedIntervals = intervals.sort((a, b) => a[0] - b[0]);
  
  let newIntervals: any = [];
  sortedIntervals.forEach((interval, index) => {
    if (index === 0) {
      newIntervals.push(interval);
    }
    const lastValue = newIntervals.length - 1;
    if (interval[0] <= newIntervals[lastValue][1]) {
      if (interval[1] > newIntervals[lastValue][1]) {
        newIntervals[lastValue] = [newIntervals[lastValue][0], interval[1]];
      }
    } else {
      newIntervals.push(interval);
    }
  });

  const result = newIntervals.reduce((acc: number, cur: [number, number]) => acc + cur[1] - cur[0], 0);
  return result;
  }

sumOfIntervals([
  [1, 3],
  [4, 8],
  [0, 3]
]);
