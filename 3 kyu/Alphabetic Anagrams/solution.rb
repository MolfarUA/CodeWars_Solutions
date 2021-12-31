FACTORIALS = (1..25).reduce([1]){|a, i| a << a.last*i}

def listPosition(word)
  return 1 if word.size == 1
  counts = word.chars.sort.tally
  counts.take_while{|char,_| char != word[0]}.sum{|char, _|
    counts.reduce(FACTORIALS[word.size-1]){|a, (k, v)| a / FACTORIALS[k==char ? v-1 : v]}
  } + listPosition(word[1..])
end

___________________________________________________
def listPosition(word)
  word=word.chars
  unique=word.uniq.sort
  aux= Array.new(unique.length,nil)
  unique.each_with_index do |el,i|
    aux[i]=word.count(el)
  end
  sum=1
  word.each_with_index do |letter,i|
    index=unique.find_index letter
    for j in 0..index-1
      if aux[j]>0
        perms=factorial(word.length-i-1)
        aux[j]-=1
        den=1
        for k in 0..aux.length-1
          den*=factorial(aux[k]) if aux[k]>0
        end
        aux[j]+=1
        sum+=perms/den
      end
    end
    aux[unique.find_index(letter)]-=1
  end
  sum
end
  
def factorial(n)
  x=1
  while n>1 do
    x*=n
    n-=1
  end
  x
end

___________________________________________________
def listPosition(word)
  word=word.chars
  puts word.length
  unique=word.uniq.sort
  aux= Array.new(unique.length,nil)
  unique.each_with_index do |el,i|
    aux[i]=word.count(el)
  end
  sum=1
  word.each_with_index do |letter,i|
    index=unique.find_index letter
    for j in 0..index-1
      if aux[j]>0
        perms=factorial(word.length-i-1)
        aux[j]-=1
        den=1
        for k in 0..aux.length-1
          den*=factorial(aux[k]) if aux[k]>0
        end
        aux[j]+=1
        sum+=perms/den
      end
    end
    aux[unique.find_index(letter)]-=1
  end
  sum
end
  
def factorial(n)
  x=1
  while n>1 do
    x*=n
    n-=1
  end
  x
end

___________________________________________________
def f n
  n < 2 ? 1 : (2..n).inject(1, :*)
end

def listPosition(word)
  a=word.chars.sort
  x=1
  word.chars.each do |c|
    i=a.index(c)
    x+=i*f(a.size-1)/(a.uniq.map{|c| f(a.count(c))}.inject(1, :*))
    a.slice!(i)
  end
  x
end

___________________________________________________
$factorial = [1] #in order to avoid recalculating it every time; knowing maxLength = 25
for i in 1..25
    $factorial.append($factorial[-1]*i)
end


def permut(sortedList)
    s = sortedList.size
    ret = $factorial[s]
    i0 = 0
    for i in 1..s
        if sortedList[i] != sortedList[i0]
            if i > i0+1
                ret /= $factorial[(i-i0)]
      end
            i0 = i
    end
  end
    if s > i0 +1
                ret /= $factorial[(s-i0)]
  end
    return ret
end



def listPosition(word)
    drow = word.split("")
    letters = drow.sort
    drow = drow.reverse() #in order to use Pop() at O(1)
    num = 1
    while letters.size > 1
        c = letters.count(drow[-1]) #in order to adjust (see below)
        i = letters.index(drow.pop())
        letters.delete_at(i)
        num += i*permut(letters)/c #the division by c is there to remove redundant combinations in the case the "current letter" appears elsewhere in the word
  end
    return num
end
