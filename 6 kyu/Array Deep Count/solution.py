def deep_count(a):
    count = 0
    for i in a:
        count += 1
        if isinstance (i, list):
            count += deep_count(i)
    return count
