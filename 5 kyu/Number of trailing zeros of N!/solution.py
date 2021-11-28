def zeros(n):
    temp = 5
    count = 0
    while (n / temp>= 1):
        count += int(n / temp) 
        temp *= 5
    return count
