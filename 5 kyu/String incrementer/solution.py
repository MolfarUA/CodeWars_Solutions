def increment_string(strng):
    if len(strng) < 1:
        return '1'

    numbers = ''
    zeros = ''

    if len(strng) == 1 and strng.isnumeric():
        return str(int(strng) + 1)


    for i in range(len(strng)-1, 0, -1):
        if strng[i].isnumeric():
            numbers += strng[i]
        else:
            break

    if len(numbers) < 1:
        return strng + '1'

    numbers = numbers[::-1]

    for z in numbers:
        if z == '0':
            zeros += '0'
        else:
            break

    if len(zeros):
        result = numbers.replace('0', '', len(zeros))
    else:
        result = numbers

    if len(result) < 1:
        return strng[0:i+1] + zeros[0:-1] + '1'

    end = (int(result) + 1)

    if strng.isnumeric():
        if len(numbers) == len(zeros):
            return strng[0:i] + zeros[0:-1] + '1'
        elif result.endswith('9') and result.startswith('9'):
            return strng[0:i] + zeros[0:-1] + str(end)
        else:
            return strng[0:i] + zeros + str(end)
    else:
        if len(numbers) == len(zeros):
            return strng[0:i+1] + zeros[0:-1] + '1'
        elif result.endswith('9') and result.startswith('9'):
            return strng[0:i+1] + zeros[0:-1] + str(end)
        else:
            if len(strng) - len(numbers) == 1:
                return strng[0] + zeros + str(end)
            else:
                return strng[0:i+1] + zeros + str(end)
