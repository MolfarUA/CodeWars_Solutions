def solution(number):
    numbers = []
    for n in range(number):
        if n % 3 == 0 or n % 5 == 0:
            numbers.append(n)
    return sum(numbers)
