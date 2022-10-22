54521e9ec8e60bc4de000d6c


def maxSequence(arr):
    max,curr=0,0
    for x in arr:
        curr+=x
        if curr<0:curr=0
        if curr>max:max=curr
    return max
_____________________________
def maxSequence(arr):
    maxl = 0
    maxg = 0
    for n in arr:
        maxl = max(0, maxl + n)
        maxg = max(maxg, maxl)
    return maxg
_____________________________
def maxSequence(arr):
    lowest = ans = total = 0
    for i in arr:
        total += i
        lowest = min(lowest, total)
        ans = max(ans, total - lowest)
    return ans
_____________________________
def max_sequence(arr):
    
    if not arr:
        return 0
    
    m = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i - 1] > 0:
            arr[i] = arr[i] + arr[i - 1]
    return max(max(arr), 0)
_____________________________
def max_sequence(arr):
    tsum, sum_ = 0, 0
    for v in arr:
        sum_ += v
        if sum_ > tsum:
            tsum = sum_
        if sum_ < 0:
            sum_ = 0
    return tsum
_____________________________
def max_sequence(arr):
    tsum, sum_ = 0, 0
    for v in arr:
        sum_ += v
        if sum_ > tsum:
            tsum = sum_
        if sum_ < 0:
            sum_ = 0
    if sum_ > tsum:
        tsum = sum_
    return tsum
_____________________________
from sys import maxsize
def max_sequence(arr):
    max_so_far = -maxsize - 1
    max_ending_here = 0
    
    if not arr:
        return 0
    if all(x<0 for x in arr):
        return 0

    for i in range(0, len(arr)):
        max_ending_here = max_ending_here + arr[i]
        if (max_so_far < max_ending_here):
            max_so_far = max_ending_here

        if max_ending_here < 0:
            max_ending_here = 0
    return max_so_far
_____________________________
def max_sequence(arr):
    max_sum = 0
    current_sum = 0

    max_start = 0
    max_end = 0
    current_start = 0
    current_end = 0

    for i in range(len(arr)):
        current_sum = current_sum + arr[i]
        current_end = i
        if current_sum < 0:
            current_sum = 0
            # Start a new sequence from next element
            current_start = current_end + 1

        if max_sum < current_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = current_end
    return max_sum
_____________________________
def max_sequence(arr):
    current_max = 0
    all_max = 0
    for n in arr:
        current_max = max(0, current_max + n)
        all_max = max(all_max, current_max)
    return all_max
_____________________________
def max_sequence(arr):
    if len(arr) == 0:
        return 0
    if sorted(arr)[0] >= 0:
        return sum(arr)
    if sorted(arr)[-1] <0:
        return 0
    counter = 0
    total = 0
    for num in arr:
        counter += num
        if counter <= 0:
            counter = 0
            continue
        if counter > total:
            total = counter
    return total
