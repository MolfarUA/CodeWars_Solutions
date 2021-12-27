def sum_of_intervals(inl):
    set1=set()
    for (i,j) in inl:
        k=i
        while k<j:
            set1.add(k)
            k=k+1
    return (len(set1))
  
___________________
def sum_of_intervals(intervals):
    result = set()
    for start, stop in intervals:
        for x in range(start, stop):
            result.add(x)
            
    return len(result)
  
__________________
def sum_of_intervals(intervals):
    s, top = 0, float("-inf")
    for a,b in sorted(intervals):
        if top < a: top    = a
        if top < b: s, top = s+b-top, b
    return s
  
_____________________
def sum_of_intervals(intervals):
    return len(set([n for (a, b) in intervals for n in [i for i in range(a, b)]]))
  
_______________
def sum_of_intervals(intervals): 
    s = []
    for i in intervals:
        s += list(range(i[0],i[1]))
    return len(set(s))
  
______________________
def sum_of_intervals(intervals):
    elems = set()
    for interval in intervals:
        for i in range(interval[0], interval[1]):
            elems.add(i)
    return len(elems)
  
___________________
def fusion_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    final_interval = [list(intervals[0])]
    for interval in intervals:
        last_interval = final_interval[-1]
        is_min_contained_in_prev_interval = interval[0] <= last_interval[1]
        if is_min_contained_in_prev_interval:
            last_interval[1] = last_interval[1] if last_interval[1] > interval[1] else interval[1]
        else:
            final_interval.append(list(interval))

    return final_interval

def sum_of_intervals(intervals):
    return sum(interval[1] - interval[0] for interval in fusion_intervals(intervals))
  
____________________________________________
def sum_of_intervals(intervals):
    out_list = []
    for inter in intervals:
        out_list.append(list(range(inter[0],inter[1])))
    
    out_num = []
    for out_interval in out_list:
        for num in out_interval:
            out_num.append(num)
    
    return len(set(out_num))
  
____________________________
def sum_of_intervals(intervals):
    res = []
    for i in intervals:
        for j in range(i[0] + 1, i[1] + 1):
            if j not in res:
                res.append(j)
    return len(res)
  
_________________________
def sum_of_intervals(intervals):
    maximum, minimum = intervals[0][1], intervals[0][0]
    for boundaries in intervals[1:]:
        if boundaries[1] > maximum: maximum = boundaries[1]
        if boundaries[0] < minimum: minimum = boundaries[0]

    lst = [0 for _ in range(maximum - minimum)]
    for boundaries in intervals:
        for index in range(boundaries[0] - minimum, boundaries[1] - minimum):
            lst[index] = 1
    
    amount = sum(lst)
    
    return amount
