56c5847f27be2c3db20009c3


fruit = {1:'kiwi',2:'pear',3:'kiwi',4:'banana',5:'melon',6:'banana',7:'melon',
         8:'pineapple',9:'apple',10:'pineapple',11:'cucumber',12:'pineapple',
         13:'cucumber',14:'orange',15:'grape',16:'orange',17:'grape',18:'apple',
         19:'grape',20:'cherry',21:'pear',22:'cherry',23:'pear',24:'kiwi',
         25:'banana',26:'kiwi',27:'apple',28:'melon',29:'banana',30:'melon',
         31:'pineapple',32:'melon',33:'pineapple',34:'cucumber',35:'orange',
         36:'apple',37:'orange',38:'grape',39:'orange',40:'grape',41:'cherry',
         42:'pear',43:'cherry',44:'pear',45:'apple',46:'pear',47:'kiwi',
         48:'banana',49:'kiwi',50:'banana',51:'melon',52:'pineapple',53:'melon',
         54:'apple',55:'cucumber',56:'pineapple',57:'cucumber',58:'orange',
         59:'cucumber',60:'orange',61:'grape',62:'cherry',63:'apple',
         64:'cherry',65:'pear',66:'cherry',67:'pear',68:'kiwi',69:'pear',
         70:'kiwi', 71:'banana',72:'apple',73:'banana',74:'melon',
         75:'pineapple',76:'melon',77:'pineapple',78:'cucumber',79:'pineapple',
         80:'cucumber',81:'apple',82:'grape',83:'orange',84:'grape',85:'cherry',
         86:'grape',87:'cherry',88:'pear',89:'cherry',90:'apple',91:'kiwi',
         92:'banana',93:'kiwi',94:'banana',95:'melon',96:'banana',97:'melon',
         98:'pineapple',99:'apple',100:'pineapple'}


def subtract_sum(n):
  n -= (sum([int(i) for i in str(n)]))
  while not n in fruit:
    n -= (sum([int(i) for i in str(n)]))
  return fruit[n]
_______________________________________
def subtract_sum(number):
    return 'apple' #fruit name like "apple"
_______________________________________
def subtract_sum(num):
    if num <= 100:
        return get_fruit_name(num - digits_sum(num))
    else:
        while num > 100:
            num = num - digits_sum(num)
            print(num)
        return get_fruit_name(num)

def get_fruit_name(num):
    if num in [1, 3, 24, 26, 47, 49, 68, 70, 91, 93]:
        return "kiwi"
    elif num in [2, 21, 23, 42, 44, 46, 65, 67, 69, 88]:
        return "pear"
    elif num in [4, 6, 25, 29, 48, 50, 71, 73, 92, 94, 96]:
        return "banana"
    elif num in [5, 7, 28, 30, 32, 51, 53, 74, 76, 95, 97]:
        return "melon"
    elif num in [8, 10, 12, 31, 33, 52, 56, 75, 77, 79, 98, 100]:
        return "pineapple"
    elif num in [9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99]: #таблица умножения 9-ти
        return "apple"
    elif num in [11, 13, 34, 55, 57, 59, 78, 80]:
        return "cucumber"
    elif num in [14, 16, 35, 37, 39, 58, 60, 83]:
        return "orange"
    elif num in [15, 17, 19, 38, 40, 61, 82, 84, 86]:
        return "grape"
    elif num in [20, 22, 41, 43, 62, 64, 66, 85, 87, 89]:
        return "cherry"

def digits_sum(num):
    sum = 0
    while num / 10 != 0:
        sum += int(num % 10)
        num /= 10
    return int(sum)
_______________________________________
fruits = {
    1 : "kiwi", 2 : "pear", 3 : "kiwi", 4 : "banana", 5 : "melon", 6 : "banana", 7 : "melon", 8 : "pineapple", 9 : "apple", 10 : "pineapple",
    11 : "cucumber", 12 : "pineapple", 13 : "cucumber", 14 : "orange", 15 : "grape", 16 : "orange", 17 : "grape", 18 : "apple", 19 : "grape", 20 : "cherry",
    21 : "pear", 22 : "cherry", 23 : "pear", 24 : "kiwi", 25 : "banana", 26 : "kiwi", 27 : "apple", 28 : "melon", 29 : "banana", 30 : "melon",
    31 : "pineapple", 32 : "melon", 33 : "pineapple", 34 : "cucumber", 35 : "orange", 36 : "apple", 37 : "orange", 38 : "grape", 39 : "orange", 40 : "grape",
    41 : "cherry", 42 : "pear", 43 : "cherry", 44 : "pear", 45 : "apple", 46 : "pear", 47 : "kiwi", 48 : "banana", 49 : "kiwi", 50 : "banana",
    51 : "melon", 52 : "pineapple", 53 : "melon", 54 : "apple", 55 : "cucumber", 56 : "pineapple", 57 : "cucumber", 58 : "orange", 59 : "cucumber", 60 : "orange",
    61 : "grape", 62 : "cherry", 63 : "apple", 64 : "cherry", 65 : "pear", 66 : "cherry", 67 : "pear", 68 : "kiwi", 69 : "pear", 70 : "kiwi",
    71 : "banana", 72 : "apple", 73 : "banana", 74 : "melon", 75 : "pineapple", 76 : "melon", 77 : "pineapple", 78 : "cucumber", 79 : "pineapple", 80 : "cucumber",
    81 : "apple", 82 : "grape", 83 : "orange", 84 : "grape", 85 : "cherry", 86 : "grape", 87 : "cherry", 88 : "pear", 89 : "cherry", 90 : "apple",
    91 : "kiwi", 92 : "banana", 93 : "kiwi", 94 : "banana", 95 : "melon", 96 : "banana", 97 : "melon", 98 : "pineapple", 99 : "apple", 100 : "pineapple",
}

def subtract_sum(number : int) -> str:
    while True:
        n = sum([ int(i) for i in str(number) ])
        number = number - n
        if number in fruits:
            break

    return fruits[number]
_______________________________________
def subtract_sum(n):
    fruits = {'kiwi': [1, 3, 24, 26, 47, 49, 68, 70, 91, 93],
    'pear': [2, 21, 23, 42, 44, 46, 65, 67, 69, 88],
    'banana': [4, 6, 25, 29, 48, 50, 71, 73, 92, 94, 96],
    'melon': [5, 7, 28, 30, 32, 51, 53, 74, 76, 95, 97],
    'pineapple': [8, 10, 12, 31, 33, 52, 56, 75, 77, 79, 98, 100],
    'apple':[9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99],
    'cucumber':[11, 13, 34, 55, 57, 59, 78, 80],
    'orange':[14, 16, 35, 37, 39, 58, 60, 83],
    'grape':[15, 17, 19, 38, 40, 61, 82, 84, 86],
    'cherry':[20, 22, 41, 43, 62, 64, 66, 85, 87, 89]
}

    while True:
        sum = 0
        for digit in str(n):
            sum += int(digit)
        n = n - sum
        if 1 <= n <= 100:
            break

    if n in fruits['kiwi']:
        fruit = 'kiwi' 
    elif n in fruits['pear']:
        fruit = 'pear' 
    elif n in fruits['banana']:
        fruit = 'banana'
    elif n in fruits['melon']:
        fruit = 'melon'
    elif n in fruits['pineapple']:
        fruit = 'pineapple'
    elif n in fruits['apple']:
        fruit = 'apple'
    elif n in fruits['cucumber']:
        fruit = 'cucumber'
    elif n in fruits['orange']:
        fruit = 'orange'
    elif n in fruits['grape']:
        fruit = 'grape'
    elif n in fruits['cherry']:
        fruit = 'cherry'

    return fruit
_______________________________________
def subtract_sum(number):
    fruit = {
        1:"kiwi",
        2:"pear",
        3:"kiwi",
        4:"banana",
        5:"melon",
        6:"banana",
        7:"melon",
        8:"pineapple",
        9:"apple",
        10:"pineapple",
        11:"cucumber",
        12:"pineapple",
        13:"cucumber",
        14:"orange",
        15:"grape",
        16:"orange",
        17:"grape",
        18:"apple",
        19:"grape",
        20:"cherry",
        21:"pear",
        22:"cherry",
        23:"pear",
        24:"kiwi",
        25:"banana",
        26:"kiwi",
        27:"apple",
        28:"melon",
        29:"banana",
        30:"melon",
        31:"pineapple",
        32:"melon",
        33:"pineapple",
        34:"cucumber",
        35:"orange",
        36:"apple",
        37:"orange",
        38:"grape",
        39:"orange",
        40:"grape",
        41:"cherry",
        42:"pear",
        43:"cherry",
        44:"pear",
        45:"apple",
        46:"pear",
        47:"kiwi",
        48:"banana",
        49:"kiwi",
        50:"banana",
        51:"melon",
        52:"pineapple",
        53:"melon",
        54:"apple",
        55:"cucumber",
        56:"pineapple",
        57:"cucumber",
        58:"orange",
        59:"cucumber",
        60:"orange",
        61:"grape",
        62:"cherry",
        63:"apple",
        64:"cherry",
        65:"pear",
        66:"cherry",
        67:"pear",
        68:"kiwi",
        69:"pear",
        70:"kiwi",
        71:"banana",
        72:"apple",
        73:"banana",
        74:"melon",
        75:"pineapple",
        76:"melon",
        77:"pineapple",
        78:"cucumber",
        79:"pineapple",
        80:"cucumber",
        81:"apple",
        82:"grape",
        83:"orange",
        84:"grape",
        85:"cherry",
        86:"grape",
        87:"cherry",
        88:"pear",
        89:"cherry",
        90:"apple",
        91:"kiwi",
        92:"banana",
        93:"kiwi",
        94:"banana",
        95:"melon",
        96:"banana",
        97:"melon",
        98:"pineapple",
        99:"apple",
        100:"pineapple",
    }
    if number > 0 and number < 10:
        return fruit[number]

    if number >= 10 and number < 10000:
        while True:
            temp = 0
            temp += number % 10
            temp += (number // 1000) % 10
            temp += (number // 100) % 10
            temp += (number // 10) % 10
            number = number - temp
            if number <= 100:
                return fruit[number]

    return  # fruit name like "apple"
_______________________________________
def subtract_sum(number):
    ls = ['1-kiwi', '2-pear', '3-kiwi', '4-banana', '5-melon', '6-banana', '7-melon', '8-pineapple', '9-apple', '10-pineapple', '11-cucumber', '12-pineapple', '13-cucumber', '14-orange', '15-grape', '16-orange', '17-grape', '18-apple', '19-grape', '20-cherry', '21-pear', '22-cherry', '23-pear', '24-kiwi', '25-banana', '26-kiwi', '27-apple', '28-melon', '29-banana', '30-melon', '31-pineapple', '32-melon', '33-pineapple', '34-cucumber', '35-orange', '36-apple', '37-orange', '38-grape', '39-orange', '40-grape', '41-cherry', '42-pear', '43-cherry', '44-pear', '45-apple', '46-pear', '47-kiwi', '48-banana', '49-kiwi', '50-banana', '51-melon', '52-pineapple', '53-melon', '54-apple', '55-cucumber', '56-pineapple', '57-cucumber', '58-orange', '59-cucumber', '60-orange', '61-grape', '62-cherry', '63-apple', '64-cherry', '65-pear', '66-cherry', '67-pear', '68-kiwi', '69-pear', '70-kiwi', '71-banana', '72-apple', '73-banana', '74-melon', '75-pineapple', '76-melon', '77-pineapple', '78-cucumber', '79-pineapple', '80-cucumber', '81-apple', '82-grape', '83-orange', '84-grape', '85-cherry', '86-grape', '87-cherry', '88-pear', '89-cherry', '90-apple', '91-kiwi', '92-banana', '93-kiwi', '94-banana', '95-melon', '96-banana', '97-melon', '98-pineapple', '99-apple', '100-pineapple']
    while True:
        number -= sum(list(map(int, list(str(number)))))
        for x in ls:
            if str(number) in x:
                return x.split('-')[1]
