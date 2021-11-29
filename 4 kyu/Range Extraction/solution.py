def solution(args):
    sol = ""
    i = 0
    while i < len(args): 
        j = i
        while j < len(args) - 1: 
            if args[j] + 1 != args [j+1]:
                break
            j += 1
        if j - i < 2:
            sol += str(args[i]) + ","
        else:
            sol += str(args[i])+ "-" + str(args[j]) + ","
            i = j
        i += 1
    return sol[:-1]
