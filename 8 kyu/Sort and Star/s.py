57cfdf34902f6ba3d300001e


def two_sort(lst):
    return '***'.join(min(lst))
___________________________
def two_sort(arr):
    return '***'.join(sorted(arr)[0])
___________________________
def two_sort(array):
    return '***'.join(min(array))
___________________________
def two_sort(a):
    a = sorted(a)
    result = "***".join(a[0])
    return result
___________________________
def two_sort(array):
    return '***'.join(sorted(array)[0])
___________________________
def two_sort(a):
    a = sorted(a)
    result = a[0]
    result = result.replace("", "***")
    return result [3:-3]
___________________________
two_sort = lambda a: "***".join(sorted(a)[0])
___________________________
two_sort = lambda _: '***'.join(sorted(_)[0])
___________________________
def two_sort(array):
    array = sorted(array)[0]
    return ''.join(([i+('***') for i in array]))[:-3]
___________________________
def two_sort(array):
    q = ""
    alf_1_word = sorted(array)[0]
    for i in alf_1_word:
        q += i + "***"

    return q[:-3]
___________________________
def two_sort(array):
    new_arr = sorted(array)
    joined = "***".join(new_arr[0])
    return joined
___________________________
def two_sort(array):
    res = 'z'
    for i in array:
        if i < res:
            res = i
    res2 = '***'.join(res)
    return res2
___________________________
def two_sort(array):
    ret = ""
    for c in list(sorted(array)[0]):
        ret += c + "***"
    return ret[:-3]
___________________________
def two_sort(array):
    array.sort()
    new_word = ""

    for letter in array[0][0:]:
        if letter in array[0:]:
            new_word += letter
            break
        else:
            new_word += letter[:1] + "***"

    return new_word [:-3]
___________________________
def two_sort(array):
    array.sort()
    result = array[0]
    return "***".join(result)
___________________________
def two_sort(array):
    array.sort()
    result = array[0]
    return "***".join(result)
