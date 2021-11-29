def square_digits(num):
    temp = ""
    for i in str(num):
        temp += str(int(i) ** 2)

    return int(temp)


print(square_digits(9119))
