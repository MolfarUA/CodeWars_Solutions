53573877d5493b4d6e00050c


def capital(capitals):
    return [f"The capital of {c.get('state') or c['country']} is {c['capital']}" for c in capitals]
_________________________
def capital(capitals): 
    ans = []
    for each in capitals:
        a = each.get('state', '')
        b = each.get('country', '')
        c = each.get('capital')
        ans.append('The capital of {}{} is {}'.format(a,b,c))
    return ans
_________________________
def capital(capitals):
    return ["The capital of {} is {}".format(*x.values()) for x in capitals]
_________________________
def capital(capitals): 
    return [f"The capital of {d['state'] if 'state' in d else d['country'] } is {d['capital']}" for d in capitals]
_________________________
def capital(capitals):
        return list(map(lambda val: 'The capital of ' + (val.get('state') or val.get('country')) + ' is ' + val["capital"],
                    capitals))
_________________________
def capital(capitals): 
    return [f"The capital of {s.get('state') or s.get('country')} is {s.get('capital')}" for s in capitals]
_________________________
def capital(capitals): 
    return [f"The capital of {e.get('state') or e.get('country')} is {e['capital']}" for e in capitals]
_________________________
def capital(capitals): 
    list1 = []
    for i in capitals:
        a = list(i.values())
        print(a)
        list1.append("The capital of " + a[0] + " is " + a[1])
    return list1
_________________________
def capital(capitals): 
    res = []

    for e in capitals:
        c = e['capital']
        if 'state' in e:
            k = 'state'
        elif 'country' in e:
            k = 'country'
        else:
            break
        p = e[k]
        st = "The capital of " + p + " is " + c
        res.append(st)

    return res
_________________________
def capital(capitals): 
    return ["The capital of {} is {}".format(c.get('state', '') or c.get('country', ''), c.get('capital', '')) for c in capitals]
