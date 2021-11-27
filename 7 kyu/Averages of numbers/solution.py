def averages(arr):
    averages = []

    if arr:
        for i in range(1, len(arr)):
            average = (arr[i - 1] + arr[i]) / 2
            averages.append(average)

    return averages
