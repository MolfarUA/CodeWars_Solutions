def warn_the_sheep (queue):
    if queue [-1] == "wolf":
        return "Pls go away and stop eating my sheep"
    else:
        for i, ele in enumerate (queue[::-1]):
            if ele == "wolf":
                print ('Oi! Sheep number {}! You are about to be eaten by a wolf!'.format (str(i)))
                return 'Oi! Sheep number {}! You are about to be eaten by a wolf!'.format (str(i))
##################
def warn_the_sheep(queue):
    n = len(queue) - queue.index('wolf') - 1
    return f'Oi! Sheep number {n}! You are about to be eaten by a wolf!' if n else 'Pls go away and stop eating my sheep'
#################
def warn_the_sheep(queue):
    i = queue[::-1].index('wolf')
    if i == 0:
        return 'Pls go away and stop eating my sheep'
    return f'Oi! Sheep number {i}! You are about to be eaten by a wolf!'
##############
def warn_the_sheep(queue):
    queue = reverse(queue)
    message_one = 'Pls go away and stop eating my sheep'
    message_two = 'Oi! Sheep number 1! You are about to be eaten by a wolf!'
    wolf = 'wolf'
    out_count = 0
    sheep_count = 0
    queue_len = length(queue)
    wolf_len = length(wolf)
    while out_count < queue_len:
        in_count = 0
        while in_count < wolf_len:
            if queue[out_count][in_count] != wolf[in_count]:
                break
            in_count += 1
            if in_count == wolf_len - 1:
                if sheep_count == 0:
                    return message_one
                else:
                    return ('Oi! Sheep number ' + num_to_str(sheep_count) + 
                            '! You are about to be eaten by a wolf!')
        sheep_count += 1
        out_count += 1
    
def reverse(arr):
    arr_l = length(arr)
    r_arr = [0] * arr_l
    count = 0
    while count < arr_l:
        r_arr[count] = arr[arr_l - 1 - count]
        count += 1
    return r_arr
    
def length(arr):
    count = 0
    try:
        while True:
            arr[count]
            count += 1
    except:
        return count
    
def num_to_str(num):
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    str_num = ''
    while num > 0:
        str_num = nums[num % 10] + str_num
        num = (num - (num % 10)) // 10
    return str_num
####################################
def warn_the_sheep(queue):   
    return ["Oi! Sheep number %s! You are about to be eaten by a wolf!" % queue[::-1].index('wolf'),
            "Pls go away and stop eating my sheep"]['wolf' in queue[-1]]
##########################
def warn_the_sheep(queue):
    if queue.index('wolf') == len(queue)-1:
        return "Pls go away and stop eating my sheep"
    else:
        N = len(queue)-queue.index('wolf')-1
        return "Oi! Sheep number {0}! You are about to be eaten by a wolf!".format(N)
########################
def warn_the_sheep(queue):
    x = 0
    for i in queue:
        x = x +1
        if i == 'wolf':
            b = len(queue) - x
            if b == 0:
                return 'Pls go away and stop eating my sheep'
            else:
                return "Oi! Sheep number {}! You are about to be eaten by a wolf!".format(b)
#####################
def warn_the_sheep(queue):
    if queue[-1] == 'wolf':
        return 'Pls go away and stop eating my sheep'
    number_of_the_sheep_which_is_about_to_die = len(queue)-queue.index('wolf')-1
    return f'Oi! Sheep number {number_of_the_sheep_which_is_about_to_die}! You are about to be eaten by a wolf!'
##################
def warn_the_sheep(queue):    
    queue.reverse()
    wolfnum = queue.index("wolf")
    if wolfnum == 0:
        return "Pls go away and stop eating my sheep"
    else:
        return "Oi! Sheep number {0}! You are about to be eaten by a wolf!".format(wolfnum)
#################
warn_the_sheep = lambda queue: 'Oi! Sheep number ' + str(len(queue) - queue.index('wolf') - 1) + '! You are about to be eaten by a wolf!' if queue[-1] == 'sheep' else 'Pls go away and stop eating my sheep'
