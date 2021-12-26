import numpy as np

def rotation(arr, ans):
    for item in arr[0]:
        ans.append(item)
    arr = np.rot90(arr[1:])
    return arr, ans

def snail(snail_map):
    if snail_map == [[]]:
        return []
    the_ans = list()
    snail_map = np.array(snail_map)
    for i in range(len(snail_map) + len(snail_map - 1)):
        snail_map, the_ans = rotation(snail_map, the_ans)
    return the_ans
  
####################
def snail(array):
    ret = []
    if array and array[0]:
        size = len(array)
        for n in xrange((size + 1) // 2):
            for x in xrange(n, size - n):
                ret.append(array[n][x])
            for y in xrange(1 + n, size - n):
                ret.append(array[y][-1 - n])
            for x in xrange(2 + n, size - n + 1):
                ret.append(array[-1 - n][-x])
            for y in xrange(2 + n, size - n):
                ret.append(array[-y][n])
    return ret
  
#################
import numpy as np

def snail(array):
    m = []
    array = np.array(array)
    while len(array) > 0:
        m += array[0].tolist()
        array = np.rot90(array[1:])
    return m
  
###############
def snail(snail_map):
    output=[]
    i=0
    size =len(snail_map[0])
    while True:
        
        #top row up until any elements counted
        for j in range(len(snail_map[0])):
            output.append(snail_map[0][j])
        del snail_map[i]
        
        #check if done
        if len(output) == size**2:
            break

        #check if done
        if len(output) == size**2:
            break
            
        #add elements down the right side of the array
        for j in range(len(snail_map)):
            output.append(snail_map[j].pop())

        #check if done
        if len(output) == size**2:
            break
            
        #add bottom row in reverse
        for j in range(len(snail_map[-1])):
            output.append(snail_map[-1].pop())
        del snail_map[-1]
        
        #check if done
        if len(output) == size**2:
            break
        
        #add elements up the left side up to the row that was already counted
        for j in range(1, len(snail_map)+1):
            output.append(snail_map[-1*j].pop(0))
        
        #check if done
        if len(output) == size**2:
            break
            
    return output
  
################
def snail(asd):
    result = []
    if asd==[[]]:
        return result
    else:
        n= len(asd)
        start = 0
        end = n
        step = int(n/2)
        
        # while len(result) < n*n:
        for j in range(step):
            c = 0
            for i in range(start, end, 1):
                result.append(asd[c+j][i])
            c = i
            for i in range(start+1, end, 1):
                result.append(asd[i][c])
            c = i
            for i in range(end-1, start, -1):
                result.append(asd[c][i-1])
            c= i-1
            for i in range(end-1, start+1, -1):
                result.append(asd[i-1][c])
            start += 1
            end -= 1
        if n%2 == 0:
            return(result)
        else:
            result.append(asd[step][step])
            return(result)
          
###########
import itertools

def snail(snail_map):
    
    final = []
    
    lastRow = (len(snail_map) - 1)
    lastCol = (len(snail_map) - 1)
    #create 02200 pattern
    toggleRow = [0, lastRow]
    toggleCol = [lastCol, 0]
    
    rowIndex = 0
    colIndex = 0
    
    def getColumn(index):
        if colIndex == 0:
            for col in snail_map:
                final.append(col[index])
        else:
            for col in reversed(snail_map):
                final.append(col[index])
    
    def delCol(index):
        for col in snail_map:
            del col[index]
            
    for i in range((len(snail_map)*2)-1):
        if (i%2 == 0):
            #add a row to final list
            if rowIndex == 0:
                final += snail_map[toggleRow[rowIndex]]
            else: 
                final += snail_map[toggleRow[rowIndex]][::-1]
            #remove the row that have been added
            del snail_map[toggleRow[rowIndex]]
            #toggle rowIndex between 0 and 1 
            rowIndex ^= 1
            #reduce index that should be 
            toggleRow[1] = toggleRow[1]-1
            
        else :
            getColumn(toggleCol[colIndex])
            delCol(toggleCol[colIndex])
            colIndex ^= 1
            toggleCol[0] = toggleCol[0]-1
    return final
  
################
def snail(snail_map):
    array = []
    while len(snail_map) > 0:
        if len(snail_map[0])==0:
            break
        else:
            for num in snail_map[0]:
                array.append(num)   
            del snail_map[0]
        if len(snail_map) == 0:
            break
        else:    
            for num in range(len(snail_map)):
                array.append(snail_map[num][-1])
                del snail_map[num][-1]
            for num in snail_map[-1][::-1]:
                array.append(num)
            del snail_map[-1]
            for num in range(len(snail_map)):
                array.append(snail_map[-1-num][0])
                del snail_map[-1-num][0]
        
    return array
  
################
def snail(snail_map):
    if not snail_map:
        return []
    if len(snail_map)==1:
        return snail_map[0]
    result =[]
    #go right
    result += snail_map[0]
    #go down
    for i in range (len(snail_map)-2):
        result.append(snail_map[i+1][-1])
    #go left
    result += reversed(snail_map [-1])
    #go up
    for i in range (len(snail_map)-2):
        result.append(snail_map[-i-2][0])
    newmap = []
    for row in snail_map[1:-1]:
        newmap.append(row[1:-1])
    result += snail(newmap)
    return result
  
#############
def snail(snail_map):
    ans = []
    while snail_map:
        for el in snail_map[0]:
            ans.append(el)
        for i in range(1, len(snail_map)):
            ans.append(snail_map[i][-1])
        for i in range(len(snail_map[-1])-2, -1, -1):
            ans.append(snail_map[-1][i])
        for i in range(len(snail_map)-2, 0, -1):
            ans.append(snail_map[i][0])
        if snail_map:
            snail_map.pop(0)
        if snail_map:
            snail_map.pop(-1)

        for e in snail_map:
            if snail_map:
                e.pop(0)
            if snail_map:
                e.pop(-1)

    return ans
