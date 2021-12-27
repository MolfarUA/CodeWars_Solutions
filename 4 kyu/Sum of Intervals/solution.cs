using System;
using System.Linq;

public class Intervals
{
  public static int SumIntervals((int, int)[] intervals)
  {
    return intervals
      .SelectMany(i => Enumerable.Range(i.Item1, i.Item2 - i.Item1))
      .Distinct()
      .Count();
  }
}

_______________________
using System;
using System.Linq;

public class Intervals
{
    public static int SumIntervals((int, int)[] intervals)
    {
        var orderedInterval = from interval in intervals
                              orderby interval.Item1, interval.Item2
                              select interval;
                              
        int sum = 0;
        int begin = Int32.MinValue;
        int end = Int32.MinValue;
        foreach(var item in orderedInterval)
        {
            bool newBegin = item.Item1 > end;
            if (newBegin) 
            {
              sum += end - begin;
              begin = item.Item1;
            }
            
            end = item.Item2 > end ? item.Item2 : end;
        }
        sum += end - begin;
        return sum;
    }
}

_____________________________
using System;
public class Intervals
{
    public static int SumIntervals((int, int)[] intervals)
    {
        Array.Sort(intervals, (x,y) => x.Item1 - y.Item1);
        int max = int.MinValue;
        int total = 0;
        foreach (var interval in intervals) 
        {
            max = Math.Max(max, interval.Item1);
            total += Math.Max(0, interval.Item2 - max);
            max = Math.Max(max, interval.Item2);
        }
        return total;
    }
}

______________________________
using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;

public class Intervals
{
    public static int SumIntervals((int, int)[] intervals)
    {
      List<int> resArr = new List<int>();
      for (int i = 0; i < intervals.Length; i++)
      {
        for (int j = intervals[i].Item1 + 1; j <= intervals[i].Item2; j++)
        {
          resArr.Add(j);
        }
      }
      return resArr.Distinct().Count();
    }
}

________________________
using System;
using System.Linq;

public class Intervals
{
    public static int SumIntervals((int min, int max)[] intervals)
    {
        var prevMax = int.MinValue;
        
        return intervals
            .OrderBy(x => x.min)
            .ThenBy(x => x.max)
            .Aggregate(0, (acc, x) => acc += prevMax < x.max ? - Math.Max(x.min, prevMax) + (prevMax = x.max) : 0);
    }
}

_________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Intervals
{

    public class Interval
    {
        public int Start{get;set;}
        public int End{get;set;}
        public bool IsDirty {get;set;}
        public int Length => End - Start;
        
        public Interval(int start,int end)
        {
            Start = start;
            End = end;
        }
        
        public override bool Equals(Object int2)
        {       
          var other = int2 as Interval;
          if(other == null)
             return false;            
          return Start == other.Start && End == other.End;
        }
        
        public Interval Combine(Interval int2)
        {
          return new Interval(Math.Min(Start,int2.Start),Math.Max(End,int2.End));
        }
        
        public bool Overlaps(Interval other)
        {
          return (Start >= other.Start && End <= other.End) || (Start <= other.Start && End >= other.End)
          || (Start >= other.Start && Start <= other.End) || (Start <= other.Start && End >= other.Start);
        }
    }
    
    
    public static int SumIntervals((int, int)[] intervals)
    {
        var ints = new List<Interval>();     
        foreach(var interval in intervals)
          ints.Add(new Interval(interval.Item1,interval.Item2));
        
        
        var combines = new List<Interval>(); 
        bool hasOverlaps;       
        do {
            hasOverlaps = false;
            foreach(var int1 in ints)
            {    
                foreach(var int2 in ints)
                {               
                    if(int1.Equals(int2))
                      continue;                  
                    if(!int1.Overlaps(int2))
                      continue;
                      
                    combines.Add(int1.Combine(int2));
                    int1.IsDirty = true;
                    int2.IsDirty = true;
                    hasOverlaps = true;
                    goto End;
                }
            }
            
           End:
           ints.RemoveAll(x=>x.IsDirty);
           ints.AddRange(combines);  
           combines.Clear();
        }
        while(hasOverlaps);
        
        
        int lengthSum = 0;
        foreach(var int1 in ints)
            lengthSum += int1.Length;
            
        return lengthSum;        
    }
   
}
