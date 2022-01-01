def order(sentence):
    return " ".join(sorted(sentence.split(), key=lambda x: int(filter(str.isdigit, x))))
  
_____________________________________________
def order(words):
  return ' '.join(sorted(words.split(), key=lambda w:sorted(w)))

_____________________________________________
def order(sentence):
    if not sentence:
        return ""
    result = []    #the list that will eventually become our setence
      
    split_up = sentence.split() #the original sentence turned into a list
  
    for i in range(1,10):
        for item in split_up:
            if str(i) in item:
                 result.append(item)    #adds them in numerical order since it cycles through i first
  
    return " ".join(result)
  
_____________________________________________
def order(sentence):
    a= sentence.split(" ")
    ans = []
    num = 1
    while num <= len(a) and len(sentence) >0:
        for i in a:
            if str(i).find(str(num)) != -1:
                ans.append(i)
                num += 1
                break

    return " ".join(ans)
  
_____________________________________________
def order(sentence):
    s = sentence.split()
    if len(s) == 0:
        return ""
    numbers = [i for i in range(1,10)]
    ordered_s = []
      
    for i in numbers:
        for j in s:
            if str(i) in j:
                ordered_s.append(j)
    ordered_sentence = ' '.join(ordered_s)
    return ordered_sentence  
  
_____________________________________________
def order(sentence):
    d = {}
    words = sentence.split()
    for word in words:
        for l in word:
            if l.isdigit():
                d[int(l)] = word + ' '
                break
    sentence = ""
    for a in range(len(d)):
        sentence += d[(a + 1)]
    return sentence[:-1]
  
_____________________________________________
def order(sentence):
    import re
    return '' if not sentence else ' '.join(sorted(sentence.split(' '), key=lambda x: re.findall('\d', x)[0]))
  
_____________________________________________
def order(sentence):
    l = sentence.split()
    d = dict()

    for i in l:
        d[(''.join(x for x in i if x.isdigit()))] = i

    return ' '.join(v[1] for v in sorted(d.items()))
  
_____________________________________________
def order(sentence):
    if len(sentence)==0:
        output=""
    else:
        sentence_list=sentence.split(' ')
        output=""
        n=1
        while (len(output)-1) != len(sentence):
            for word in sentence_list:
                if str(n)  in word:
                    output=output + word +' '
                    n+=1
    output=output[0:-1]
    return output
  
_____________________________________________
def order(sentence):
  sent_list = sentence.split()
  nums = []
  dic = {}
  ordered_sent = []
  for word in sent_list:
      for char in word:
          if char.isnumeric():
               nums.append(int(char))
  for idx in range(len(nums)):
    dic[nums[idx]] = sent_list[idx]
  for i in range(1,len(nums)+1):
    ordered_sent.append(dic[i])
  return " ".join(ordered_sent)

_____________________________________________
def order(sentence):
    if sentence == '':
        return sentence
    else:
        all_words = sentence.split()
        helper = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        output = ''
        index = 0
        for item in helper:
            if index < len(all_words):
                for word in all_words:
                    if item in word:
                        output += word + ' '
            else:
                break
        return output.rstrip()
