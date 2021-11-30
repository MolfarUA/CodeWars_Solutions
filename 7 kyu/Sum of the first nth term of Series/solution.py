def series_sum (n):
    y = 1
    sum_numbers = 0
    for x in range (1, n+1):
        sum_numbers += 1/y
        y += 3
    return (format(sum_numbers, '.2f'))
