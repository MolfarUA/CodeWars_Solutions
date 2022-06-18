57eb8fcdf670e99d9b000272


import string

def high(x):
    scores = []
    letters = [i for i in string. ascii_lowercase]
    words = x.split(' ')
    current = 0
    for word in words:
        for letter in word:
            current += (letters.index(letter) + 1)
        scores.append(current)
        current = 0

    highest = scores.index(max(scores))

    return words[highest]
###############
def high(x):
    return max(x.split(), key=lambda k: sum(ord(c) - 96 for c in k))
############
def high(x):
    words=x.split(' ')
    list = []
    for i in words:
        scores = [sum([ord(char) - 96 for char in i])]
        list.append(scores)
    return words[list.index(max(list))]
#############
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def high(s):
    words = s.split()
    word = find_max_score(words)
    return word[0][0]
#     return word


def find_max_score(words):
    values_dict = dict()
    for word in words:
        sum = 0
        for char in word:
            sum += alphabet.index(char) + 1
        values_dict[word] = sum
    return sorted(values_dict.items(), key=lambda item: item[1], reverse=True)
################
def high(x):
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    word = ""
    highest = 0
    for w in x.split(" "):
        count = 0
        for c in list(w):
            count += alph.index(c)+1
        
        if count>highest:
            highest = count
            word = w
    return word
############################
alphabet: str = 'abcdefghijklmnopqrstuvwxyz'

def high(x):
    final_word: tuple = ('', 0) # current word and score
    for word in x.split():
        score: int = 0
        for char in word: # calculate score
            score += alphabet.find(char) + 1
        if score > final_word[1]: # if score greater then final_word
            final_word = (word, score)
    return final_word[0]
################
def high(x):
    mydict = {}
    words = x.split()
    for word in words:
        sum_total = 0
        for char in word:
            sum_total += ord(char) - 96
        mydict[word] = sum_total
    return sorted(mydict, key=mydict.get, reverse=True)[0]
########################
def high(x):
    # Code here
    word = x.split()
    sco = [sum(ord(j)-96 for j in k)for k in word]
    return word[sco.index(max(sco))]
###########################
def high(x):
    # Code here
    x_list = x.split(' ')
    x_dict = {}
    for n,word in enumerate(x_list,1):
        sco = 0
        for letter in word:
            sco += ord(letter)-96
        x_dict[(n,word)] = sco
    sco_list = sorted(x_dict,key=lambda x:x_dict[x],reverse=True)
    n = 0
    for j in range(len(sco_list)-1):
        if x_dict[sco_list[n]] == x_dict[sco_list[n+1]]:
            if sco_list[n][0]<sco_list[n+1][0]:
                n = n
                break
            else:
                n += 1
    return sco_list[n][-1]
###############################
import string

def high(x):
    high_score = 0
    current_score = 0
    highest_word = ""
    current_word = ""
    for i in x:
        if i == " ":
            if current_score > high_score:
                highest_word = current_word
                high_score = current_score
                current_score = 0
            current_word = ""
            current_score = 0
        else:
            current_word += i
            current_score += string.ascii_lowercase.index(i)+1
    if current_score > high_score:
        highest_word = current_word
        high_score = current_score
    return highest_word
###########################
def high(x):
    dict = {
        "a" : 1,
        "b" : 2,
        "c" : 3,
        "d" : 4,
        "e" : 5,
        "f" : 6,
        "g" : 7,
        "h" : 8,
        "i" : 9,
        "j" : 10,
        "k" : 11,
        "l" : 12,
        "m" : 13,
        "n" : 14,
        "o" : 15,
        "p" : 16,
        "q" : 17,
        "r" : 18,
        "s" : 19,
        "t" : 20,
        "u" : 21,
        "v" : 22,
        "w" : 23,
        "x" : 24,
        "y" : 25,
        "z" : 26
     }
    score, high_score = 0, 0
    word, high_word = "", ""
    for char in range(len(x)):
        if x[char] != " ":
            score += dict[x[char]]
            word += x[char]
            if score > high_score:
                high_score = score
                high_word = word
        else:
            word = ""
            score = 0
    return(high_word)
###################################
def high(x):
    d=dict(zip('abcdefghijklmnopqrstuvwxyz',range(1,27)))
    l=x.split()
    l.sort(reverse=True,key=lambda x: sum([d[i] for i in x]))
    return l[0]
#############################
def high(x):
    wordspower = []
    currentpower = 0
    maxpower = 0
    number = 0
    for word in x.split():
        for letter in word:
            currentpower += ord(letter) - 96
        wordspower.append(currentpower)
        currentpower = 0
    for i in range(len(wordspower)):
        if wordspower[i] > maxpower:
            maxpower = wordspower[i]
            number = i
    return x.split()[number]
###########################
def high(wordlist):
    char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
    word_array = wordlist.split(' ')
    word_value = []

    for word in word_array:
        summ = 0

        for letter in word:
            summ += char.index(letter) + 1

        word_value.append(summ)

    word_value_copy = []

    for _ in word_value:
        word_value_copy.append(_)

    word_value_copy_sorted = sorted(word_value_copy)

    word_idx = word_value_copy_sorted[-1]
    word_idx = word_value.index(word_idx)
    word = word_array[word_idx]

    return word
#####################
def high(x):    
    def compute_score(w):
        return sum(ord(c) - 96 for c in w.lower())
    
    max_score = max(compute_score(w) for w in x.split(" "))
    
    for w in x.split(" "):
        if compute_score(w) == max_score:
            return w
###################
def high(x):
  res = []
  list=x.split()
  for i in list:
    res.append(sum([ord(j)-96 for j in i]))
  return list[(res.index(max(res)))]
#####################
import string

def high(x):
    summ = 0
    s_dict = {}
    l_lst = []
    s_lst = x.split(" ")
    print(s_lst)
    for i in range(0,len(string.ascii_lowercase)):
        s_dict.update({f'{[i for i in string.ascii_lowercase][i]}' : [y for y in range(1, len(string.ascii_lowercase) + 1)][i]})
    for word in s_lst:
        l_lst.append([l for l in word])
    for w in range(len(l_lst)):
        for l in l_lst[w]:
            # print(l, s_dict.get(l))
            summ = summ + s_dict.get(l)
        l_lst[w] = summ
        summ = 0
    return s_lst[l_lst.index(max(l_lst))]
#####################
def high(string):
    words = string.split(' ')

    def score(word):
        a, c = 'abcdefghijklmnopqrstuvwxyz', []
        [c.append((i+1) * word.count(a[i])) for i in range(len(a)) if a[i] in word]
        return sum(c)

    words.sort(key=score, reverse=True)
    return words[0]
#####################33
import string

def high(x):
    words = x.lower().split(" ")
    alphabet = string.ascii_lowercase
    all_words_with_sum = dict()
    for word in words:
        words_sum = sum(alphabet.index(char)+1 for char in word)
        if words_sum in all_words_with_sum:
            temp_list = all_words_with_sum[words_sum]
            temp_list.append(word)
        else:
            all_words_with_sum[words_sum] = [word]

    max_value = max(all_words_with_sum)
    result_index = None
    for word in all_words_with_sum[max_value]:
        word_index = words.index(word)
        if (not result_index and result_index!=0) or word_index <= result_index:
            result_index = word_index

    return x.split(" ")[result_index]
_____________________________________________
def high(x):
    x = x.split(" ");
    a = ' abcdefghijklmnopqrstuvwxyz';
    y = [];
    for i in range(len(x)):
        z = 0;
        for j in range(len(x[i])):
            z += a.find(x[i][j]);
        y.append(z)
    v = 0
    for i in range(len(y)):
        if y[i] > v :
            v = y[i]
    for i in range(len(y)):
        if y[i] == v:
            return x[i]
_____________________________________________
def high(x):
    x_split = x.split()
    l = []
    count = 0
    sum = []
    for i in x:
        l.append(ord(i)-96)
    l.append(-64)
    for i in l:
        if i == -64:
            count += 0
            sum.append(count)
            count = 0
        else:
            count += i
    longest = sum.index(max(sum))
    return x_split[longest]
