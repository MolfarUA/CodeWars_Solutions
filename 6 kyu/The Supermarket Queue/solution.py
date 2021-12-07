def queue_time(customers, n):
    tills = [0]*n
    for i in customers:
      tills[0] += i
      tills.sort()
    return max(tills)
############
def queue_time(customers, n):
    l=[0]*n
    for i in customers:
        l[l.index(min(l))]+=i
    return max(l)
###########
import heapq

def queue_time(customers, n):
    heap = [0] * n
    for time in customers:
        heapq.heapreplace(heap, heap[0] + time)
    return max(heap)
#############
def queue_time(customers, n):
    qn = [0] * n
    for c in customers:
        qn = sorted(qn)
        qn[0] += c
    return max(qn)
##############
def queue_time(customers, n):
    time = 0
    c = customers[:(n-1)] + [0]
    for customer in customers[(n-1):]:
        if 0 not in c:
            m = min(c)
            c = list(map(lambda x: x - m, c))
            time += m
        c.remove(0)
        c.append(customer)
    return time + max(c)
###########
def queue_time(customers, n):
    low_num = 0
    low_num_ind = 0
    checkout = []
    
    if not len(customers):
        return 0
    if n == 1:
        return sum(customers)
    if len(customers) <= n:
        return max(customers)
    
    for ind, val in enumerate(customers):
        if ind < n:
            checkout.append(val)
        else:
            for ind2, val2 in enumerate(checkout):
                if not low_num or low_num > val2:
                    low_num = val2
                    low_num_ind = ind2
            checkout[low_num_ind] += val
            low_num = 0
            low_num_ind = 0
    return max(checkout)
##########################
def queue_time(queue, tills):

    till_qus = []
    min_lst = []

    if queue == []:
        return 0
    elif len(queue) < tills :
        return max(queue)

    while len(queue) !=0:

        while len(till_qus) < tills:
            if queue == []:
                break
            till_qus.append(queue.pop(0))

#         print(f"current Queues in each till: {till_qus}")
        
        mn = min(till_qus)

#         print(f"Minimum of till queue {mn}")

        min_lst.append(mn)
        till_qus = list(filter(lambda val : val != mn, till_qus))
        till_qus = list(map(lambda val : val - mn, till_qus))

#         print(f"Till Queue at end of loop {till_qus}")


#         print(f"Minimum list {min_lst}")
    
    return sum(min_lst) + (max(till_qus) if len(till_qus) > 0 else 0)
######################################################################
def queue_time(customers, n):
    t = 0
    while len(customers) > 0:
        m = min(customers[:n])
        t += m
        customers[:n] = [x - m for x in customers[:n] if x - m > 0]
    return t
#############
def queue_time(customers, n):
    import numpy as np
    customers = np.asarray(customers, dtype=int)
    time = 0
    while len(customers) > n:
        queue_time = np.min(customers[0:n])
        time += queue_time
        customers[0:n] = [x-queue_time for x in customers[0:n]]
        customers = [x for x in customers if x > 0]
    if len(customers) > 0:
        time += max(customers)
    return time
##############
def queue_time(customers, n):
    tills = {i: [] for i in range(1, n+1)}
    if customers:
        while len(customers) > 0:
            customer = customers.pop(0)
            next_till = min([(sum(total), till) for till, total in tills.items()])[1]
            tills[next_till].append(customer)
        total_time = max([(sum(total), till) for till, total in tills.items()])[0]
        return total_time
    return 0
############
def queue_time(customers, n):
    # TODO
    time_count = {}
    customer_count = len(customers)
    pelanggan = customers

    if customer_count < 1:
        return 0
    else:
        finish_count = False
        kaunter = {}
        for ix in range(n):
            kaunter[ix] = 0
            time_count[ix] = 0

        while finish_count == False:

            for ix in range(n):
                # check if kaunter is 0
                if kaunter[ix] == 0:
                    # get new customer if available
                    if len(pelanggan) > 0:
                        kaunter[ix] = pelanggan.pop(0)
                        # print(kaunter)
                else:
                    # reduce count

                    kaunter[ix] = kaunter[ix] - 1
                    time_count[ix] = time_count[ix] + 1
                    if kaunter[ix] == 0:
                        if len(pelanggan) > 0:
                            kaunter[ix] = pelanggan.pop(0)
                    # print(time_count)
            # print(kaunter)

            if sum(kaunter.values()) == 0 and len(pelanggan) == 0:
                # no more customer to count
                finish_count = True

    # return True
    return max(time_count.values())
#######################################
def queue_time(customers, n):
    
    caisse=[]
    tps=0

    
    for i in range(n):
        caisse+=[0]

    print('cust init',customers)
    print('caisse init',caisse)

    while customers!=[] or caisse!=[]:

        for i in range(len(caisse)):
            if caisse[i]==0 and customers!=[]:
                caisse[i]=customers.pop(0)
        
        if max(caisse)==0:
            return tps

        tps+=1

        for j in range(len(caisse)):
            if caisse[j]!=0:
                caisse[j]=caisse[j]-1 
#############
def queue_time(customers, n):
    if customers:
        for e in customers[n:]:
            customers[customers.index(min(customers[:n]))] += e
        return max(customers)

    else:
        return 0
